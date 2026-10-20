#!/usr/bin/env python3
"""낭독 대본의 글자 수로 구간별 낭독 시각, 파트 분할, 이미지 장면 수를 계산한다.

긴 글의 글자 수는 눈으로 세면 틀리기 쉬워서, 파트 경계와 장면 수를 정하기 전에
이 스크립트로 먼저 계산한다. 결과는 기본값이며 시각적 밀도에 따라 조정해도 된다.

사용 예
  python story_timing.py ep01_제목_대본.md --parts 5 --images 100 --out timeline.md
  python story_timing.py ep01_제목_대본.md --parts 5 --cut 15
  python story_timing.py ep01_제목_대본.md --images 100 --weights 1,1,1,1,1,1,1,1,1

대본 형식 (dnd-sleep-story 스킬의 출력)
  - 상단 헤더: 시리즈명, 회차와 제목, "예상 낭독 시간 ... 분당 N자 ... 공백 포함 M자"
  - 본문: 문단은 빈 줄로 구분, 장면 전환은 "· · ·" 한 줄
  - 본문 뒤: "---" 구분선이나 "에피소드 기록" 제목 아래는 낭독하지 않는 보관용이라 제외
"""
import argparse
import re
import sys
from pathlib import Path

SCENE_DIVIDER = re.compile(r'^\s*(?:[·•・∙*]\s*){3,}$')
BODY_END = re.compile(r'^\s*(?:-{3,}|_{3,})\s*$')
RECORD_HEADING = re.compile(r'^\s*#{1,6}\s*에피소드\s*기록')
SENTENCE = re.compile(r'.+?[.!?]+["”’」』)]*(?:\s+|$)', re.S)


def fmt_time(sec):
    sec = int(round(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'


def split_sentences(par):
    out, pos = [], 0
    for m in SENTENCE.finditer(par):
        out.append(m.group(0))
        pos = m.end()
    if pos < len(par):
        out.append(par[pos:])
    return out


def parse(text):
    lines = text.splitlines()

    # 헤더: "낭독 시간"이 적힌 줄까지
    header_end = -1
    for i, line in enumerate(lines[:12]):
        if '낭독 시간' in line:
            header_end = i
            break
    header = lines[: header_end + 1] if header_end >= 0 else []

    # 본문 끝: 구분선이나 에피소드 기록 제목
    end = len(lines)
    for i in range(header_end + 1, len(lines)):
        if BODY_END.match(lines[i]) or RECORD_HEADING.match(lines[i]):
            end = i
            break

    sections = [[]]
    for line in lines[header_end + 1: end]:
        if not line.strip():
            continue
        if SCENE_DIVIDER.match(line):
            if sections[-1]:
                sections.append([])
            continue
        sections[-1].append(line.strip())
    sections = [s for s in sections if s]
    return header, sections


def largest_remainder(total, weights):
    s = sum(weights)
    raw = [total * w / s for w in weights]
    base = [int(x) for x in raw]
    rest = total - sum(base)
    order = sorted(range(len(raw)), key=lambda i: raw[i] - base[i], reverse=True)
    for i in order[:rest]:
        base[i] += 1
    # 모든 구간에 최소 1장
    for i, b in enumerate(base):
        if b == 0:
            j = max(range(len(base)), key=lambda k: base[k])
            if base[j] > 1:
                base[j] -= 1
                base[i] = 1
    return base


def partition(values, k):
    """연속한 구간을 k개 묶음으로 나눈다. 가장 큰 묶음을 최소화하고 동률이면 편차가 작은 쪽."""
    n = len(values)
    k = min(k, n)
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    INF = (float('inf'), float('inf'))
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    cut = [[0] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = (0, 0)
    for j in range(1, k + 1):
        for i in range(j, n + 1):
            for t in range(j - 1, i):
                prev = dp[j - 1][t]
                if prev == INF:
                    continue
                seg = prefix[i] - prefix[t]
                cand = (max(prev[0], seg), prev[1] + seg * seg)
                if cand < dp[j][i]:
                    dp[j][i] = cand
                    cut[j][i] = t
    groups, i = [], n
    for j in range(k, 0, -1):
        t = cut[j][i]
        groups.append((t, i))
        i = t
    return list(reversed(groups))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path')
    ap.add_argument('--rate', type=float, help='분당 글자 수 (기본은 헤더 값, 없으면 360)')
    ap.add_argument('--parts', type=int, default=5)
    ap.add_argument('--images', type=int, help='전체 장면(이미지) 수')
    ap.add_argument('--cut', type=float, default=15.0, help='--images가 없을 때 컷 한 장의 기본 길이(초)')
    ap.add_argument('--weights', help='구간별 장면 수 가중치, 쉼표로 구분 (예: 1,1,1,0.7)')
    ap.add_argument('--out', help='결과를 저장할 마크다운 파일')
    args = ap.parse_args()

    text = Path(args.path).read_text(encoding='utf-8-sig')
    header, sections = parse(text)
    if not sections:
        sys.exit('본문을 찾지 못했습니다.')

    header_text = '\n'.join(header)
    m = re.search(r'분당\s*([\d,]+)\s*자', header_text)
    rate = args.rate or (float(m.group(1).replace(',', '')) if m else 360.0)
    rate_src = '지정값' if args.rate else ('헤더' if m else '기본값')
    m = re.search(r'공백\s*포함\s*([\d,]+)\s*자', header_text)
    stated = int(m.group(1).replace(',', '')) if m else None

    # 문단과 문장 단위 누적
    paragraphs = []  # dict: id, sec, start_chars, chars, text
    sentences = []
    cum = 0
    for si, sec in enumerate(sections, 1):
        for par in sec:
            pid = len(paragraphs) + 1
            paragraphs.append({'id': f'P{pid:02d}', 'sec': si, 'start': cum, 'chars': len(par), 'text': par})
            pos = cum
            for k, sent in enumerate(split_sentences(par), 1):
                sentences.append({'id': f'P{pid:02d}.{k}', 'start': pos, 'chars': len(sent), 'text': sent})
                pos += len(sent)
            cum += len(par)
    total_chars = cum
    nospace = sum(len(re.sub(r'\s', '', p['text'])) for p in paragraphs)
    total_sec = total_chars / rate * 60

    sec_chars = [sum(p['chars'] for p in paragraphs if p['sec'] == i) for i in range(1, len(sections) + 1)]
    n_img = args.images or max(len(sections), round(total_sec / args.cut))
    if args.weights:
        w = [float(x) for x in args.weights.split(',')]
        if len(w) != len(sections):
            sys.exit(f'--weights 개수({len(w)})가 구간 수({len(sections)})와 다릅니다.')
    else:
        w = [1.0] * len(sections)
    imgs = largest_remainder(n_img, [c * wi for c, wi in zip(sec_chars, w)])

    sec_start_chars, acc = [], 0
    for c in sec_chars:
        sec_start_chars.append(acc)
        acc += c
    scene_from, acc = [], 1
    for n in imgs:
        scene_from.append(acc)
        acc += n

    def first_words(t, n=16):
        t = t.replace('|', '/')
        return t[:n] + ('…' if len(t) > n else '')

    out = []
    out.append('# 낭독 타임라인\n')
    for h in header:
        if h.strip():
            out.append(f'- {h.strip()}')
    out.append('')
    out.append(f'- 기준: 분당 {rate:g}자 ({rate_src}), 본문 {total_chars:,}자(공백 포함) → 낭독 {fmt_time(total_sec)}')
    out.append(f'- 공백 제외 글자 수: {nospace:,}자')
    if stated:
        diff = (total_chars - stated) / stated * 100
        note = '일치' if abs(diff) < 0.5 else f'헤더 표기와 {diff:+.1f}% 차이'
        out.append(f'- 헤더 표기 글자 수: {stated:,}자 ({note})')
    out.append(f'- 장면 수: {n_img}장 (평균 {total_sec / n_img:.1f}초 / 장)')
    if args.weights:
        out.append(f'- 구간 가중치: {args.weights}')
    out.append(f'- 구간 {len(sections)}개, 문단 {len(paragraphs)}개, 문장 {len(sentences)}개\n')

    out.append('## 구간 표 (`· · ·` 단위)\n')
    out.append('| 구간 | 문단 | 글자 수 | 시작 | 끝 | 비중 | 장면 수 | 장면 번호 | 첫머리 |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    for i, sec in enumerate(sections):
        pids = [p['id'] for p in paragraphs if p['sec'] == i + 1]
        st = sec_start_chars[i] / rate * 60
        en = (sec_start_chars[i] + sec_chars[i]) / rate * 60
        out.append(
            f'| {i + 1} | {pids[0]}–{pids[-1]} | {sec_chars[i]:,} | {fmt_time(st)} | {fmt_time(en)} '
            f'| {sec_chars[i] / total_chars * 100:.0f}% | {imgs[i]} | S{scene_from[i]:03d}–S{scene_from[i] + imgs[i] - 1:03d} '
            f'| {first_words(sec[0])} |'
        )
    out.append('')

    groups = partition(imgs, args.parts)
    if len(groups) < args.parts:
        out.append(f'주의: 구간이 {len(sections)}개뿐이라 파트를 {len(groups)}개로 줄였습니다.\n')
    out.append(f'## 파트 분할 ({len(groups)}개, 구간 경계 기준)\n')
    out.append('| 파트 | 구간 | 글자 수 | 시작–끝 | 장면 수 | 장면 번호 |')
    out.append('|---|---|---|---|---|---|')
    for gi, (a, b) in enumerate(groups, 1):
        chars = sum(sec_chars[a:b])
        n = sum(imgs[a:b])
        st = sec_start_chars[a] / rate * 60
        en = (sec_start_chars[a] + chars) / rate * 60
        label = f'{a + 1}' if b - a == 1 else f'{a + 1}–{b}'
        out.append(
            f'| {gi} | {label} | {chars:,} | {fmt_time(st)}–{fmt_time(en)} | {n} '
            f'| S{scene_from[a]:03d}–S{scene_from[a] + n - 1:03d} |'
        )
    out.append('')

    out.append('## 문단 표\n')
    out.append('| ID | 구간 | 시작 | 글자 | 첫머리 |')
    out.append('|---|---|---|---|---|')
    for p in paragraphs:
        out.append(f"| {p['id']} | {p['sec']} | {fmt_time(p['start'] / rate * 60)} | {p['chars']} | {first_words(p['text'])} |")
    out.append('')

    out.append('## 문장 표 (정밀한 컷 위치 지정용)\n')
    out.append('| ID | 시작 | 글자 | 첫머리 |')
    out.append('|---|---|---|---|')
    for s in sentences:
        out.append(f"| {s['id']} | {fmt_time(s['start'] / rate * 60)} | {s['chars']} | {first_words(s['text'], 14)} |")
    out.append('')

    result = '\n'.join(out)
    if args.out:
        Path(args.out).write_text(result, encoding='utf-8')
        print(f'저장: {args.out}')
        # 요약만 화면에 출력
        head = result.split('## 문단 표')[0]
        print(head)
    else:
        print(result)


if __name__ == '__main__':
    main()
