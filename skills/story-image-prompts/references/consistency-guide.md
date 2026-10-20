# 일관성 가이드 — Story Bible과 Anchor 문구

## 목차
1. Anchor 문구란
2. 인물 Anchor 작성법
3. 의상·상태 변화 관리
4. 소품 Anchor
5. 장소 Anchor
6. STYLE LOCK
7. 흔한 실패와 대응
8. Story Bible 출력 양식
9. 시리즈 Bible과 회차 Bible (연재물)

---

## 1. Anchor 문구란

Anchor는 "이 대상을 그릴 때는 항상 이 문장을 쓴다"고 확정한 영어 묘사 블록이다.

원칙 세 가지:

- **이름이 아니라 외형을 쓴다.** 모델은 "Seoyeon"이 누구인지 모른다. 이름은 Bible의 ID로만 쓰고, 프롬프트에는 외형 묘사가 들어간다.
- **글자 그대로 복사한다.** 장면마다 "a young woman with dark hair"처럼 줄이거나 "a girl with black hair"로 바꾸면 모델은 다른 사람을 그린다.
- **확정 후에는 고치지 않는다.** 바꿔야 한다면 Bible을 먼저 고치고 모든 장면에 반영한다.

## 2. 인물 Anchor 작성법

아래 항목을 이 순서로, 한 덩어리 문장(40~70단어)으로 쓴다. 순서가 고정되어 있어야 복사·비교가 쉽다.

1. 나이대 + 성별 + 체형/키 인상 (예: `a slim woman in her late twenties, average height`)
2. 얼굴형과 눈코입의 눈에 띄는 특징 (예: `oval face, sharp jawline, slightly upturned dark brown eyes, thin straight eyebrows`)
3. 피부톤 (예: `warm light-beige skin`)
4. 머리 — **색 + 길이 + 질감 + 스타일**을 모두 (예: `black shoulder-length straight hair with blunt bangs, tucked behind the left ear`)
5. 식별 특징 — 점, 흉터, 안경, 주근깨, 귀걸이 등 2개 이하 (예: `a small mole under the left eye, round tortoiseshell glasses`)
6. 기본 의상 → 별도 COSTUME 블록으로 분리 (3번 참고)

팁:

- 추상어(예쁜, 차가운 인상)는 모델마다 해석이 달라 흔들린다. 구체적 형태·색으로 쓴다.
- 식별 특징은 **멀리서도 보이는 것**을 우선한다. 안경, 머리색, 모자, 흉터 같은 것이 얼굴 디테일보다 일관성 유지에 강하다.
- 이야기에 나이만 있고 외형이 없으면 이야기의 시대·지역·분위기에 맞게 채우고 `(추정)`을 단다.
- 아이/노인은 나이대와 체형을 더 구체적으로 쓴다. (예: `a seven-year-old boy, small for his age, round cheeks`)
- 동물·크리처도 같은 방식으로 Anchor를 만든다. (종, 크기, 털/비늘 색과 무늬, 눈 색, 특징적 부위)

## 3. 의상·상태 변화 관리

의상은 인물 Anchor와 **분리**한다. 얼굴 Anchor는 고정하고 옷만 갈아입히기 위해서다.

- ID 규칙: `CHAR-서연/COS-A`(교복), `CHAR-서연/COS-B`(한복) …
- 각 COS 블록: 상의·하의·신발·겉옷·액세서리를 색과 소재까지 (예: `a navy wool coat with horn buttons, cream turtleneck, charcoal trousers, brown leather ankle boots`)
- 이야기 시간순으로 어느 장면에서 어떤 COS를 입는지 **의상 타임라인**을 Bible에 적는다.

상태 변화(부상, 더러워짐, 젖음, 낡음, 나이 듦)는 **STATE 태그**로 관리한다.

- 예: `STATE-rain`: `soaked through, hair plastered to forehead, dark wet patches on the coat`
- 예: `STATE-injured-left-arm`: `left forearm wrapped in a stained white bandage`
- 장면 프롬프트에서는 Anchor + COS + STATE를 이어 붙인다.
- 이야기상 되돌릴 수 없는 변화(잘린 머리, 흉터)는 그 시점부터 인물 Anchor 자체를 새 버전으로 만든다: `CHAR-서연 v2`. 이후 장면은 v2만 쓴다.

시간 경과(어린 시절 → 성인)는 같은 인물이라도 **별도 Anchor**(`CHAR-서연(child)`, `CHAR-서연(adult)`)로 만들고, 공통 식별 특징(점, 머리색 등)을 양쪽에 유지해 같은 사람으로 보이게 한다.

## 4. 소품 Anchor

반복 등장하거나 이야기에 중요한 소품만 만든다. 한 번 쓰고 마는 소품은 장면 프롬프트에서 즉석 서술한다.

- 형태, 크기(손 대비), 재질, 색, 낡은 정도, 독특한 무늬/글자 (예: `a palm-sized brass pocket watch with a cracked glass face and a leaf engraving on the lid, tarnished green at the edges`)
- 소품의 상태가 바뀌면(깨짐, 불탐) STATE 태그로 관리한다.
- 소품 크기는 항상 비교 대상과 함께 쓴다 (`palm-sized`, `as long as a forearm`). 모델이 크기를 마음대로 정하는 것을 막는다.

## 5. 장소 Anchor

반복 등장하는 장소는 **공간 구조**를 포함한다. 같은 방인데 창문 위치가 바뀌는 게 가장 흔한 실패다.

- 구조: 크기감, 창/문 위치(관찰자 기준 왼쪽/오른쪽/정면), 주요 가구 배치
- 재질·색: 바닥, 벽, 천장
- 고정 오브젝트: 항상 있는 물건 3~5개
- 변형: 시간대/날씨/계절은 별도 태그로 (`LOC-서재/night`, `LOC-서재/morning-fog`). 구조 문장은 그대로 두고 조명 문장만 교체한다.
- 카메라 방향이 달라지는 경우(반대편에서 본 방)는 "from the door looking toward the window" 식으로 시점을 명시한다.

## 6. STYLE LOCK

모든 프롬프트 맨 끝에 같은 문장으로 붙는 전체 스타일 블록.

포함 요소:

- 매체/화풍 (예: `soft watercolor children's book illustration`, `cinematic realistic photograph`, `Korean webtoon style, clean line art with cel shading`)
- 색감 팔레트 (예: `muted earth tones with warm amber highlights`)
- 조명 성향 (예: `soft diffused natural light`)
- 질감/마감 (예: `visible paper grain`)
- 화면비 (예: `16:9`) — 그림책이면 `4:3` 또는 `1:1` 등 용도에 맞게
- 금지 요소: `no text, no watermark, no captions`

사용자가 화풍을 지정하지 않았으면 이야기의 장르·분위기에 맞춰 하나를 제안하고 `(추정)`을 단다. 이후 변경하지 않는다.

영상의 용도(수면용 등)를 이유로 대비·조명·분위기를 미리 제한하지 않는다. 시청자는 어떤 상황에서든 볼 수 있다. 분위기는 이야기 자체의 결(예: 편안하고 따뜻한 이야기)에서 정한다.

## 7. 흔한 실패와 대응

| 증상 | 원인 | 대응 |
|---|---|---|
| 장면마다 얼굴이 다름 | Anchor 축약/변형, 참조 이미지 없음 | Anchor 글자 그대로 복사, 캐릭터 시트를 참조로 첨부 |
| 옷이 바뀜 | 의상이 Anchor에 섞여 있거나 생략됨 | COS 블록을 매 프롬프트에 포함 |
| 방 구조가 바뀜 | 장소 Anchor에 구조 없음 | 창/문/가구 위치를 관찰자 기준으로 고정, 빈 배경 플레이트를 참조로 첨부 |
| 소품 크기가 들쭉날쭉 | 크기 비교 대상 없음 | `palm-sized` 등 상대 크기 명시 |
| 그림체가 흔들림 | STYLE LOCK 누락/변형 | 모든 프롬프트 끝에 동일 복사 |
| 이미지에 글자가 들어감 | 텍스트 금지 문구 없음 | STYLE LOCK에 `no text` 포함 |
| 여러 인물이 서로 특징을 섞음 | 한 프롬프트에 묘사가 뒤섞임 | 인물별로 문단을 나누고, 위치(왼쪽/오른쪽)로 구분해 각 Anchor 붙이기 |

## 8. Story Bible 출력 양식

```
# STORY BIBLE — {제목}

## 개요
장르/시대/분위기: ...
장면 수: ...
(추정) 항목: ...

## STYLE LOCK
EN: ...
KO: ...

## CHARACTERS
### CHAR-{이름} — {역할}
EN anchor: ...
KO 설명: ...
식별 포인트: ...
의상 타임라인: COS-A (Scene 1–4), COS-B (Scene 5–)
#### COS-A
EN: ...
KO: ...
#### STATE 태그
- STATE-xxx: EN ... / KO ...

## PROPS
### PROP-{이름}
EN anchor: ...
KO 설명: ...

## LOCATIONS
### LOC-{이름}
EN anchor (구조): ...
KO 설명: ...
변형: LOC-{이름}/night — 조명 문장: ...
```

---

## 9. 시리즈 Bible과 회차 Bible (연재물)

연재물은 주인공과 반복 장소가 회차를 넘어 같은 얼굴로 유지되어야 하므로 Bible을 두 층으로 나눈다.

### 무엇을 어디에 두는가

| 항목 | 시리즈 Bible | 회차 Bible |
|---|---|---|
| STYLE LOCK | 여기에만 둔다. 회차마다 바꾸지 않는다 | 없음 |
| 주인공, 매 회 나오는 인물 | Anchor, COS, 상태 태그 | 없음 |
| 매 회 반복되는 장소와 소품 | Anchor | 없음 |
| 장기 떡밥의 시각 모티프 | 예를 들어 방패의 움푹 팬 자국처럼 회차를 넘어 이어지는 단서의 모양과 위치 | 없음 |
| 금지·주의 | 시리즈 바이블의 금지·주의를 시각 규칙으로 옮긴 것 (전투 묘사 없음 → 무기가 부딪치는 장면, 부상, 피를 그리지 않는다) | 없음 |
| 그 회에만 나오는 인물·소품·장소 | 없음 | Anchor |
| 연속성 기록 | 맨 아래에 회차마다 추가 | 없음 |

### 승격과 ID

- 회차 Bible의 항목이 다음 회에 다시 나오면 시리즈 Bible로 옮긴다. ID는 바꾸지 않는다. 시트 이미지 파일명도 그대로 쓴다.
- ID는 시리즈 안에서 겹치지 않게 한다. 같은 이름의 다른 대상이 생기면 구분어를 붙인다(`LOC-등대내부`, `LOC-망루쉼터`).
- 시리즈 Bible에 있는 항목은 회차 시작 때 다시 만들지 않고 확정된 시트를 첨부해서 쓴다.

### 외형이 나이를 먹는 경우

같은 인물의 외형이 회차 사이에 바뀌면(머리를 자름, 흉터가 생김) 인물 Anchor를 새 버전으로 만든다(`CHAR-카엘 v2`). 바뀐 회차부터 v2만 쓰고, 이전 회차의 이미지와 Bible은 건드리지 않는다.

### 연속성 기록

회차를 마칠 때 시리즈 Bible 맨 아래에 다음 화 그림에 영향을 주는 상태를 적는다.

```
## 연속성 기록
### EP01 종료 시점
- CHAR-카엘: COS-B 유지, 수첩 첫 장에 한 줄 기록됨
- PROP-수첩: 둘째 장 맨 위 줄에 선이 하나 그어짐
- PROP-방패: 자국 그대로
- 열린 실마리의 시각 모티프: (있다면)
```

### 입력으로 쓸 수 있는 자료

`dnd-sleep-story` 스킬은 시리즈 바이블(`series_bible_시리즈명.md`)과 대본 끝의 에피소드 기록을 만든다. 이 문서에서 주인공의 외형, 늘 지니는 물건, 반복 요소, 세계 설정, 금지·주의, 장기 떡밥을 읽어 시각 Bible의 출발점으로 쓴다. 시리즈 바이블의 외형 서술이 정본이고, 거기에 없는 부분만 `(추정)`으로 채운다.
