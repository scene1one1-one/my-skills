# 프롬프트 템플릿

## 목차
1. 캐릭터 시트 프롬프트
2. 소품 시트 프롬프트
3. 배경 플레이트 프롬프트
4. 장면 프롬프트
5. 샷/구도 어휘
6. ChatGPT / Gemini 사용 팁
7. 도구별 변형
8. 작성 예시
9. 정지 이미지로 옮기는 법 (소리, 움직임, 시간, 대사)

ChatGPT·Gemini 이미지 모델은 키워드 나열보다 **자연스러운 문장**을 잘 이해한다. 아래 템플릿은 모두 문장형이다. `{...}`는 Bible의 해당 문구를 그대로 복사해 넣는 자리다.

---

## 1. 캐릭터 시트 프롬프트

일관성의 기준점이 되는 이미지. 인물마다 하나씩, 장면 생성 전에 먼저 만든다.

**EN**
```
A character reference sheet on a plain light-gray background. The same character shown in a front view, a side view, and a back view, standing in a neutral relaxed pose, plus three close-up face portraits showing a neutral, a smiling, and a worried expression. Character: {CHAR anchor}. Outfit: {COS anchor}. Even, flat lighting, full body visible in the three views, consistent proportions across all views. {STYLE LOCK}
```

**KO**
```
무지 밝은 회색 배경 위의 캐릭터 설정 시트. 같은 인물을 정면, 측면, 후면 전신으로 편안하게 선 자세로 보여주고, 무표정/미소/걱정스러운 표정의 얼굴 클로즈업 3개를 함께 배치한다. 인물: {CHAR 한국어 설명}. 의상: {COS 한국어 설명}. 고르고 평평한 조명, 세 전신 뷰의 비율 일관. {STYLE LOCK 한국어}
```

의상이 여러 벌이면 COS별로 시트를 따로 만들거나, "outfit change sheet: the same character wearing outfit A, B, C side by side" 형태로 한 장에 묶는다.

## 2. 소품 시트 프롬프트

**EN**
```
A prop reference sheet on a plain neutral background showing one object from three angles: front, side, and a close-up of its most distinctive detail. Object: {PROP anchor}. A human hand is shown holding it in one view to indicate its scale. Even soft lighting. {STYLE LOCK}
```

## 3. 배경 플레이트 프롬프트

인물이 없는 빈 장소. 이후 장면에서 구조를 유지하는 참조로 쓴다.

**EN**
```
An empty establishing shot of {LOC anchor}, no people. Camera positioned {view description, e.g. at the doorway looking toward the window}. {lighting sentence for time of day}. {STYLE LOCK}
```

시간대/날씨 변형은 lighting sentence만 바꾼다. 구조 문장은 건드리지 않는다.

## 4. 장면 프롬프트

**기본 구조 (이 순서 유지)**

1. 샷 종류 + 카메라 각도
2. 장소 (LOC anchor + 시간대/날씨 문장)
3. 인물 (각 인물마다: CHAR anchor + COS anchor + STATE + 이번 장면의 포즈/표정/행동)
4. 소품 (PROP anchor + 위치/사용 방식)
5. 분위기/조명
6. STYLE LOCK

**EN 템플릿**
```
{shot type}, {camera angle}. Setting: {LOC anchor}, {time/weather lighting}. {CHAR anchor} {COS anchor} {STATE if any}, {pose and action}, {visible expression}. {second character block if any, with position: "on the right"}. {PROP anchor} {how it appears in the scene}. Mood: {mood in visual terms}. {STYLE LOCK}
```

**KO 템플릿**
```
{샷 종류}, {카메라 각도}. 배경: {LOC 한국어}, {시간/날씨 조명}. {CHAR 한국어} {COS 한국어} {STATE}, {포즈와 행동}, {보이는 표정}. {두 번째 인물: 위치 포함}. {PROP 한국어} {장면 속 모습}. 분위기: {시각적 표현}. {STYLE LOCK 한국어}
```

**여러 인물이 나올 때**

- 인물마다 문단을 분리하고 "on the left / in the center / on the right"로 위치를 먼저 쓴다.
- 인물 사이 거리/시선 방향/접촉을 명시한다. (`standing two steps apart, facing each other`)
- 조연 단역은 Anchor 없이 `a distant crowd of villagers in muted clothes`처럼 일반 묘사로 처리해도 된다.

## 5. 샷/구도 어휘

| 목적 | 표현 |
|---|---|
| 장소 소개 | `wide establishing shot`, `aerial view` |
| 인물과 환경 관계 | `full-body shot`, `medium-wide shot` |
| 대화/행동 | `medium shot`, `over-the-shoulder shot` |
| 감정 | `close-up on the face`, `extreme close-up on the eyes` |
| 소품 강조 | `insert shot of the object in the hands` |
| 위압/왜소 | `low angle`, `high angle looking down` |
| 불안/긴장 | `slightly tilted frame`, `tight framing` |
| 고독 | `small figure in a vast empty space, wide framing` |

연속되는 장면에서는 샷 종류를 번갈아 주어 리듬을 만든다 (wide → medium → close-up).

## 6. ChatGPT / Gemini 사용 팁

사용자에게 3~5줄로 안내한다.

1. 시트 프롬프트로 인물·소품·배경 이미지를 먼저 생성하고, 마음에 드는 결과를 고른다.
2. 장면을 만들 때는 해당 장면에 나오는 시트 이미지를 **함께 첨부**하고 이렇게 시작한다: "첨부한 이미지의 인물·소품·배경 디자인을 그대로 유지하고, 아래 장면을 그려줘."
3. 같은 대화창에서 이어서 생성하면 앞 이미지를 참조하기 쉽다. 대화가 길어져 흔들리면 새 대화로 시작해 시트를 다시 첨부한다.
4. 결과가 일부만 어긋나면 처음부터 다시 만들기보다 "머리 길이만 시트와 똑같이 수정해줘"처럼 부분 수정을 요청한다.
5. 모델이 이미지에 글자를 넣으면 "글자 없이"를 끝에 한 번 더 강조한다.

## 7. 도구별 변형

사용자가 다른 도구를 쓸 때만 적용한다.

- **Midjourney**: 문장을 쉼표로 이어진 키워드형으로 압축하고 끝에 `--ar 16:9` 등 파라미터. 캐릭터 일관성은 시트 이미지를 `--cref`, 화풍은 `--sref`로 참조. Anchor 문구는 짧게 줄이되 모든 장면에서 동일하게 유지.
- **Stable Diffusion / Flux**: 태그형 프롬프트와 네거티브 프롬프트를 분리. Anchor는 태그 목록으로 변환하고, 고정 시드·LoRA·IP-Adapter 사용 안내를 덧붙인다.

## 8. 작성 예시

입력 이야기(요약): "비 오는 밤, 안경을 쓴 소녀 하윤이 낡은 놋쇠 손전등을 들고 버려진 등대에 들어선다. 꼭대기에서 늙은 등대지기가 말없이 램프를 닦고 있다."

**Bible 일부**

```
STYLE LOCK
EN: Soft watercolor children's book illustration, muted blue-gray and warm amber palette, gentle visible paper grain, 4:3 landscape, no text, no watermark.
KO: 부드러운 수채화 동화책 일러스트, 차분한 청회색과 따뜻한 호박색 팔레트, 은은한 종이 질감, 4:3 가로, 글자·워터마크 없음.

CHAR-하윤 — 주인공 (나이·머리 길이 추정)
EN anchor: A ten-year-old girl, small and slim, round face with rosy cheeks, large dark brown eyes, warm light-beige skin, black chin-length hair with a straight fringe, round red-framed glasses.
COS-A: a yellow rain poncho over a green knit sweater, gray shorts, red rubber boots.

CHAR-등대지기 — 조연
EN anchor: An elderly man, tall and thin, deeply lined weathered face, white bushy beard, small gray eyes, pale tanned skin, bald head covered by a navy wool cap.
COS-A: a thick cream fisherman's sweater with patched elbows and dark waterproof trousers.

PROP-손전등
EN anchor: A forearm-length antique brass flashlight, tarnished green at the seams, a small dent near the lens ring, a worn leather strap.

LOC-등대/내부
EN anchor: The inside of an old stone lighthouse, a narrow circular room with rough gray stone walls, a spiral iron staircase winding up along the wall to the right, a small arched window on the left wall, a wooden table with a rusty lantern near the stairs, puddles on the stone floor.
```

**Scene 1 — 등대 입구** (EN)

```
Medium-wide shot, eye-level, from inside the doorway looking in. Setting: The inside of an old stone lighthouse, a narrow circular room with rough gray stone walls, a spiral iron staircase winding up along the wall to the right, a small arched window on the left wall, a wooden table with a rusty lantern near the stairs, puddles on the stone floor. Night, heavy rain visible through the doorway behind her, cold blue light from outside. A ten-year-old girl, small and slim, round face with rosy cheeks, large dark brown eyes, warm light-beige skin, black chin-length hair with a straight fringe, round red-framed glasses, wearing a yellow rain poncho over a green knit sweater, gray shorts, red rubber boots, dripping wet, stands just inside the door, looking up the staircase with wide, nervous eyes. She holds a forearm-length antique brass flashlight, tarnished green at the seams, a small dent near the lens ring, a worn leather strap, its beam cutting across the stone wall. Mood: quiet, tense, curious. Soft watercolor children's book illustration, muted blue-gray and warm amber palette, gentle visible paper grain, 4:3 landscape, no text, no watermark.
```

(한국어 버전도 같은 구성으로 쓴다.)

---

## 9. 정지 이미지로 옮기는 법 (소리, 움직임, 시간, 대사)

낭독 대본과 소설의 서술에는 정지 이미지에 직접 담기지 않는 것이 많다. 그대로 프롬프트에 쓰면 모델이 무시하거나 엉뚱한 것을 그린다. 아래처럼 눈에 보이는 대응물로 바꿔서 쓴다.

| 원문에 있는 것 | 이미지에서 대신 그리는 것 |
|---|---|
| 소리 ("쿵, 하는 낮은 소리") | 소리가 남긴 결과. 피어오르는 먼지, 기울어진 물체, 소리에 멈춘 발걸음, 소리 쪽으로 돌아간 시선 |
| 일정하게 이어지는 소리 (걸레가 선반을 쓰는 박자) | 팔을 길게 한 번 뻗은 순간과 판에서 일어나는 먼지. 박자는 같은 구도의 연속 컷으로 리듬을 준다 |
| 냄새 (먼지 냄새, 짠 내) | 냄새를 실어 나르는 것. 먼지, 안개, 연기, 젖은 갈대 |
| 온기와 온도 | 색온도(호박빛), 난로 불빛이 얼굴 한쪽에 닿는 모습, 김 |
| 멈췄다 가는 움직임, 반복 | 한 컷에 하나의 순간. 멈춘 위치를 정해 그리고, 되풀이는 같은 구도의 컷을 2~3장으로 나눠 위치를 똑같이 유지한다. 잔상선이나 모션 블러는 쓰지 않는다 |
| 시간 경과 ("물이 장대 밑동을 한 뼘씩 드러낸다") | 같은 구도의 전후 쌍, 또는 장소 변형 태그(`/high-tide` → `/receding` → `/low-tide`). 변화량은 구체적으로 쓴다 |
| 시간 건너뜀 ("사흘째 새벽") | 새 설정 샷에 인물의 상태 태그(진흙, 먼지)를 붙인다 |
| 대사 | 말하는 순간 입을 크게 그리지 않는다. 말하는 인물의 시선과 손짓, 듣는 인물의 반응을 그린다. 두세 줄마다 어깨 너머 샷과 반대편 샷을 번갈아 쓴다. 말풍선과 글자는 넣지 않는다 |
| 마음, 내면 | 행동, 소품, 시선으로 옮긴다 (손이 멈춘다, 시선을 돌려 준다) |
| 글귀 (꼬리표, 액자, 편지) | 읽을 수 없는 필기로 그리고, 글귀는 오버레이 문구로 따로 적는다 |
| 정확한 개수 (상자 46개, 도장 31개) | 개수 대신 줄지어 늘어선 인상. 정확한 숫자는 오버레이나 자막으로 |
| 강한 빛 (등대 불빛) | `soft glow`, 은은한 빛무리 (이야기의 분위기에 맞게 강도를 정한다) |

### 단서 컷 예시

이야기의 인과가 눈에 보이는 디테일에 달려 있을 때는 그 디테일 하나를 화면의 주인공으로 삼는다.

원문 취지: 비어 있는 칸의 먼지 위에 손바닥만 한 네모꼴 자국이 선명하고, 판자 안쪽 모서리가 벽 쪽으로 손가락 한 마디만큼 내려앉아 그 아래로 틈이 벌어져 있다.

```
Close-up, slightly low angle, on the empty last compartment at the end of a wooden shelf that touches a rough stone wall. A clean palm-sized rectangle is outlined in the thick gray dust on the plank where an object once sat, its edges crisp. The plank's inner corner sags toward the wall by about a finger's width, opening a narrow dark gap beneath it. Warm lantern light rakes across the dust so the outline is clearly visible. No people. {LOC 분위기 문구} {STYLE LOCK}
```

### 소리를 결과로 옮기는 예시

원문 취지: 빗자루 끝에 둔하게 걸린 것이 틈 입구까지 굴러 나오고, 쿵 하는 낮은 소리가 난다.

```
Very low angle from floor level. A small dark-wood box rolls heavily out of a narrow gap between a shelf and a stone wall, caught by the end of a broom handle, a soft puff of dust lifting around it, cobwebs trailing from its twine. At the top edge of the frame a man's boot is frozen mid-step, as if he has just heard it. {PROP anchor} {STYLE LOCK}
```

### 되풀이되는 움직임 예시

원문 취지: 등대의 빛이 조금 가다 멈추기를 되풀이하고, 세 번 모두 같은 자리에서 멈춘다.

같은 구도의 와이드 샷을 3컷으로 만든다. 세 컷 모두 빛줄기가 같은 방향과 같은 각도에서 멈춰 있고, 달라지는 것은 물 위에 비친 빛의 반짝임 정도와 인물이 쥔 가방끈의 손 위치 정도로 아주 작게 한다. 변화가 크면 "같은 자리에서 멈춘다"는 의미가 사라진다.
