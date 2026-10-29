# my-skills

개인 에이전트 스킬(SKILL.md) 모음입니다. Claude Code, Codex 등 SKILL.md를 읽는 에이전트에서 쓸 수 있습니다.

## 스킬 목록

| 스킬 | 설명 |
|---|---|
| [minimax-h3-video-prompt](skills/minimax-h3-video-prompt/SKILL.md) | MiniMax H3(Hailuo 3) 영상 생성 프롬프트를 공식 가이드 형식(T2VA/I2VA/FL2VA/L2VA/Ref2VA)으로 작성 |
| [story-image-prompts](skills/story-image-prompts/SKILL.md) | 소설·대본을 분석해 일관성 있는 이미지 생성 프롬프트(영어+한국어)와 낭독 타임라인 작성 |
| [dnd-sleep-story](skills/dnd-sleep-story/SKILL.md) | 전통 D&D 세계관의 연재형 수면 이야기 대본(1편 약 20분) 작성 |
| [ltx25-video](skills/ltx25-video/SKILL.md) | LTX-2.5 영상 프롬프트를 공식 가이드 형식으로 쓰고 RunningHub API로 시작 이미지와 영상 생성 |
| [hanjungil-sageuk-shorts](skills/hanjungil-sageuk-shorts/SKILL.md) | 「같은 대사, 한중일 사극」 쇼츠 제작: 대본, 캐릭터 시트, LTX-2.5 컷, YuE2 BGM, ElevenLabs 나레이션, 레이아웃 합성 |
| [short-drama-skill-finder](skills/short-drama-skill-finder/SKILL.md) | AI 숏드라마·만쥐용 스킬 추천 ([원본](https://github.com/UnderleveledBuilder/awesome-short-drama-skills), CC0) |

### HyperFrames (HTML로 영상 만들기)

[heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)의 공개 스킬 21개를 그대로 복사했습니다 (Apache-2.0, [라이선스](licenses/hyperframes-LICENSE), 원본 커밋 `a8a8032`, 2026-10-20). 스킬끼리 서로 참조하므로 함께 설치하세요. 시작점은 `hyperframes`입니다.

| 분류 | 스킬 |
|---|---|
| 시작점 | [hyperframes](skills/hyperframes/SKILL.md) |
| 기본 | [hyperframes-core](skills/hyperframes-core/SKILL.md), [hyperframes-animation](skills/hyperframes-animation/SKILL.md), [hyperframes-keyframes](skills/hyperframes-keyframes/SKILL.md), [hyperframes-creative](skills/hyperframes-creative/SKILL.md), [hyperframes-audio](skills/hyperframes-audio/SKILL.md) |
| 도구 | [hyperframes-cli](skills/hyperframes-cli/SKILL.md), [hyperframes-studio](skills/hyperframes-studio/SKILL.md), [hyperframes-registry](skills/hyperframes-registry/SKILL.md), [media-use](skills/media-use/SKILL.md), [figma](skills/figma/SKILL.md), [remotion-to-hyperframes](skills/remotion-to-hyperframes/SKILL.md) |
| 영상 유형 | [general-video](skills/general-video/SKILL.md), [motion-graphics](skills/motion-graphics/SKILL.md), [slideshow](skills/slideshow/SKILL.md), [faceless-explainer](skills/faceless-explainer/SKILL.md), [product-launch-video](skills/product-launch-video/SKILL.md), [music-to-video](skills/music-to-video/SKILL.md), [pr-to-video](skills/pr-to-video/SKILL.md), [talking-head-recut](skills/talking-head-recut/SKILL.md), [embedded-captions](skills/embedded-captions/SKILL.md) |

최신 버전은 원본에서 바로 설치할 수도 있습니다: `npx skills add heygen-com/hyperframes`

## 사용법

### 내 컴퓨터 / 프로젝트에 설치

```bash
# 목록에서 골라 설치 (프로젝트 폴더에서 실행하면 그 프로젝트에만 설치)
npx skills add scene1one1-one/my-skills

# 컴퓨터 전체에 설치
npx skills add scene1one1-one/my-skills -g
```

수동으로 넣으려면 원하는 스킬 폴더를 그대로 복사합니다.

- 프로젝트에만: `<프로젝트>/.claude/skills/<스킬 이름>/`
- 전체: `~/.claude/skills/<스킬 이름>/`

### claude.ai / Claude 앱

스킬 폴더(예: `skills/story-image-prompts`)를 zip으로 압축해 설정의 스킬 메뉴에서 업로드합니다.

## 스킬 추가하기

`skills/<스킬 이름>/SKILL.md` 형태로 폴더를 하나 만들고 커밋합니다. 참고 파일은 같은 폴더 안의 `references/`, `scripts/`, `assets/`에 둡니다.
