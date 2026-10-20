---
name: "minimax-h3-video-prompt"
description: "MiniMax H3(Hailuo 3) 영상 생성 프롬프트를 공식 가이드 형식(T2VA/I2VA/FL2VA/L2VA/Ref2VA)으로 작성할 때 사용한다."
---

# MiniMax H3 영상 프롬프트 작성

출처: MiniMax 공식 저장소 https://github.com/MiniMax-AI/MiniMax-H3 의 `skills/h3-prompt-writing` (SKILL.md, references/base-en.txt, references/ref-en.txt). 아래 규칙은 그 가이드를 그대로 옮긴 것이다. 필드 이름, 섹션 순서, 라벨, 시간 표기는 절대 바꾸지 않는다. 원문 사본이 `/mnt/project-files/minimax-h3-official/`에 있으면 애매할 때 그 파일을 읽는다.

## 사용자와 소통

- 사용자는 한국어로 요청한다. 설명과 질문은 한국어로 한다.
- 최종 프롬프트 본문은 영어로 쓴다. 대사, 가사, 화면에 보이는 글자만 원래 언어(예: 한국어) 그대로 둔다.
- 결과는 (1) 복사해 붙일 프롬프트 코드 블록, (2) 한국어로 된 짧은 장면 요약(샷별 시간, 카메라, 소리) 순으로 준다.
- 길이(4~15초), 모드, 스타일이 빠졌으면 합리적인 기본값(8초, T2VA, Live-action cinematic)을 고르고 무엇을 골랐는지 한 줄로 밝힌다.

## 1단계: 모드 판별

- T2VA: 텍스트만 있음. 오디오·영상 타임라인 전체를 텍스트로 구성.
- I2VA: 첫 프레임 이미지 1장. 첫 프레임에서 앞으로 전개.
- FL2VA: 첫 프레임 + 마지막 프레임 2장. 두 장면 사이의 연속 경로를 묘사.
- L2VA: 마지막 프레임 1장. 그럴듯한 시작 상태를 추론하고 마지막 프레임으로 수렴.
- Ref2VA(풀 레퍼런스): 인물/배경/스타일 참조 이미지, 참조 영상(편집·이어붙이기·카메라 구조), 참조 오디오(음색·BGM 재사용) 등을 섞어 쓰는 경우.

## 2단계: 베이스 모드(T2VA/I2VA/FL2VA/L2VA) 최종 구조

### 첫 줄 지시문 (T2VA는 없음, 바로 세 필드로 시작)

I2VA:
```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```
FL2VA:
```
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```
L2VA:
```
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```
N은 실제 마지막 샷 번호, S.SS는 영상 길이(소수 둘째 자리까지, 예: 8.00). 지시문은 반드시 첫 줄이고, 그 뒤에 빈 줄 하나, 그다음 세 필드.

### 세 핵심 필드 (이 순서 고정, 필드 사이 빈 줄)
```
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```
- integrated_multimodal_description: 타임라인을 따라 화면, 동작, 샷, 화자, 대사, 노래, 극중 소리(diegetic)를 모두 묘사. 본문의 중심.
- overall_soundscape: 영상 전체의 환경음, 물리적 동작음, 비언어 인간 소리(숨, 웃음 등)를 1~4문장 한 문단으로. 대사·노래·극중 음악은 여기 반복하지 않는다. 사용자가 완전 무음을 요구할 때만 `N/A`.
- non_diegetic_music: 인물은 못 듣고 관객만 듣는 배경음악을 1~3문장으로. 악기, 템포, 리듬, 다이내믹 변화만 쓰고 추상적 감정어나 음악의 감정적 기능 설명은 쓰지 않는다. 라디오·TV·인물이 부르는 노래는 극중 소리이므로 본문에 쓴다. 없으면 `N/A`.

### 키프레임 반영 방법
- I2VA: `<Picture 1>`은 0.00초 실제 첫 프레임이고 [Shot 1]에 속한다. 먼저 이미지의 스타일, 인물, 구도, 장면 앵커를 세우고 다음 동작을 묘사. 인물 정체성, 옷, 색, 핵심 소품, 공간 관계 유지. 구조: 첫 프레임 앵커 → 동작 시작 → 연속 전개 → 결과/반응.
- FL2VA: 두 이미지를 정적으로 반복 묘사하지 말고 잇는 움직임 경로를 쓴다. 기본은 단일 샷(명시 요청 시에만 다중 샷). 마지막 [Shot N] 끝에서 마지막 프레임에 도달. 구조: 첫 프레임 상태 → 관찰 가능한 중간 변화 → 차이가 점점 줄어듦 → 마지막 프레임 상태.
- L2VA: `<Picture 1>`은 마지막 샷의 마지막 프레임이며 Shot 1 소속이 아니다. 구조: 그럴듯한 이전 상태 → 명확한 동작·전환 경로 → 마지막 샷에서 점진적 수렴 → 마지막 프레임 착지.

## 3단계: 본문 공통 작성 규칙

### 스타일과 첫 구도
[Shot 1] 시작에서 전체 스타일과 첫 구도를 밝힌다. 스타일 예: `Cinematic`, `live-action`, `2D-animated`, `3D CG`, `claymation`, `watercolor`, `vintage film`. 키프레임 모드는 이미지에서 스타일을 따오고, T2VA는 사용자 텍스트에서 고른다.
```
[Shot 1] Live-action, cinematic, a medium-wide shot frames...
```

### 샷과 컷
- 첫 샷에는 타임스탬프를 붙이지 않는다.
- 이후 샷은 순서대로 번호를 매기고, 엄격히 증가하며 영상 길이 안에 있는 컷 시간으로 시작: `[Shot 2] At 00:03.500, the camera cuts to...`
- 일반 컷 표현: `the camera cuts to`, `the shot cuts to`, `the shot transitions to`, `the shot changes to`, `the shot switches to`. cross-dissolve, fade, wipe는 사용자가 명시할 때만.
- 컷은 피사체, 공간, 상태, 시점, 시간 중 새 정보를 줄 때만. 거리나 각도만 살짝 바뀌면 카메라 무빙을 쓴다.

### 카메라 무빙 = 동작 유형 + 폭 + 속도
동작 유형: Zoom In/Out(초점거리 변화, 몸체 고정), Push In/Pull Out(전진/후진), Pan Left/Right(제자리 수평 회전), Truck Left/Right(수평 이동), Tilt Up/Down(제자리 수직 회전), Pedestal Up/Down(카메라 전체 상하 이동), Arc Shot(피사체 주위 호), Tracking Shot(움직이는 피사체 추적), Static Shot(고정), Shake Slightly/Strongly(흔들림), POV(인물 시점), Roll Clockwise/Counterclockwise(렌즈 축 회전).
폭: `with small amplitude` / `with large amplitude`. 속도: `at slow speed` / `at fast speed`. 중간 폭·보통 속도는 보통 생략.
라벨을 문장 끝에 나열하지 말고 자연스러운 영어 동작 문장으로 쓴다.
```
The camera pushes in with small amplitude at slow speed toward the folded letter in her hands.
The camera pans right with large amplitude at fast speed, revealing the open doorway.
The camera holds a static shot as the runner exits the frame.
```

### 화자, 대사, 노래
- 말하거나 노래하거나 화면 밖 목소리를 내는 주체만 `(S1)`, `(S2)` 같은 고정 ID를 받는다. 샷이 바뀌어도 같은 ID 유지. 동시에 말하면 `(S1,S2)`.
- 화자가 처음 등장할 때 캐릭터 유형, 나이, 성별, 화면 안/밖, 음높이, 음색, 말 속도, 억양 등으로 정체성을 세운다.
- 화자 묘사, ID, 동작, 말투는 `<d>` 밖에. `<d>` 안에는 언어 태그와 사용자가 준 대사 원문만. 단어와 문장부호를 번역·수정하지 않는다.
```
The young woman with a quiet, breathy voice (S1) says: <d>[English] I get off at the next station.</d>
The two children (S1,S2) shout together, <d>[English] Wait for us!</d>
The middle-aged man with a low, calm voice (S1) says: <d>[Korean] 다음 역에서 내릴게.</d>
```
- 보이스오버는 정확히 `says in an off-screen voiceover`를 쓰고, `<d>` 직후에 해당 인물의 입술이 닫혀 있다고 명시:
```
The man (S1) says in an off-screen voiceover: <d>[English] I still remember that road.</d> while his lips remain completely closed.
```
- 대사·가사가 컷을 넘어가면 양쪽 연결 지점에 `<scenetrans>`를 넣고 소리가 이어진다고 명시(`continues seamlessly across the cut`, `continues uninterrupted into the next shot`, `carries over from the previous shot`, `remains audible across the transition`). 영상 끝에서 말이 잘리면 `<cutoff>`.

### 화면 속 글자
간판, 현수막, 라벨, 자막, 네온 등 실제로 보이는 글자는 영어 큰따옴표 안에 원문 그대로: `A red neon sign reading "영업중" glows above the doorway.`

## 4단계: Ref2VA(풀 레퍼런스) 구조

여섯 섹션을 이 순서로, 모두 영어로(대사·가사·화면 글자만 원어):
`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`

### 라벨 (한 번 정한 의미는 모든 섹션에서 동일)
- `<Subject N>`: 참조 자산에서 추출해 실제로 쓰는 보이는 내용(인물, 동물, 사물, 배경, 의상, 소품, UI, 이펙트, 스타일, 동작, 표정, 포즈). 한 주체가 여러 자산에서 올 수 있고, 한 자산이 여러 주체를 줄 수 있다.
- `<Picture N>`: 이미지 자체가 샷의 첫/키/마지막 프레임, 편집 키프레임, 구도 앵커, 스토리보드일 때만 별도 줄. 인물·배경·스타일 정의용이면 해당 `<Subject N>` 정의 안에서만 인용.
- `<Video N>`: 원본 영상 편집, 원본 끝에서 이어가기, 카메라·컷·리듬·시간 구조 참조 같은 영상 전체 관계 전용. 영상 속 인물·사물은 여전히 `<Subject N>`.
- `<Audio N>`: 독립 오디오 또는 활성화된 영상의 동기 오디오 트랙. 복사, BGM 스타일 참조, 음색 참조, 대사·가사·효과음 사용, 비트·연속성 참조. 화자와 연결되면 `<Audio 1> is the voice-timbre reference for <Subject 1> (S1).` 처럼 전역 화자 ID 재사용. `<Video N>`과 `<Audio N>` 번호는 서로 독립. 소리가 들어 있다는 이유만으로 `<Audio N>`을 만들지 않는다.

### subject_definitions
추적할 항목마다 한 줄. 라벨이 무엇인지, 참조 역할, 따라야 할 주요 특징, 필요하면 출처 자산.
```
<Subject 1> is the young woman in <Picture 1>, with long dark hair, a blue cardigan, and a thin silver necklace.
<Subject 2> is the woman whose appearance comes from <Picture 2> and whose walking motion comes from <Video 1>.
<Picture 3> is the first frame of [Shot 1], showing a woman seated beside a café window.
<Video 1> is the source video for the target video edit.
<Audio 2> is the synchronized audio track of <Video 1> and is reused in the target video.
```

### summary
짧은 영어 한 문단. 대괄호 작업 유형 접두어로 시작하고, 여러 개면 ` + `로 결합(중복 금지). 새 라벨 도입 금지.
- `keyframe completion`: 이미지가 구체적 프레임 앵커
- `reference generation`: 인물·배경·스타일·동작·카메라·스토리보드 가이드(구체 프레임도 편집 대상도 아님)
- `video editing`: 기존 원본 영상을 직접 수정. 이때 summary는 `The target video is an edited version of <Video 1>.`로 시작. 원본 오디오가 남으면 `audio reuse`도 붙인다.
- `video continuation`: 원본 영상에서 이어가기/전환
- `audio reuse`: 같은 오디오 신호를 전부 또는 일부 재사용
- `audio reference`: 신호를 복사하지 않고 스타일·음색·대사 내용·질감·비트·연속성만 참조
참조 영상이 카메라·컷·리듬만 주면 보통 `reference generation`이다.

### retention_analysis
라벨마다 한 줄. `(Sx)`는 쓰지 않는다. 새로 추가된 동작·배경을 충실도 손실로 보지 않는다.
보이는 내용 마커: `fully_preserved`, `partially_preserved`, `attribute_transfer`(다른 대상에 특징 이전), `weak_reference`(스타일·범주·구도·분위기만 유사).
오디오 마커: `fully_copy`(원본 전체가 최종 오디오 전체), `partially_copy`(일부 구간·레이어만 복사, 또는 추가·삭제·교체), `reference`, `weak_reference`.
```
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - ...
<Picture 2> ([Shot 1] first frame): fully_preserved - ...
<Video 1> (cut and pacing structure): weak_reference - ...
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track.
```

### detailed_description
- `[Shot 1]` 앞에 스타일을 영어 한두 문장으로 먼저 세운다: `The target video is in a cinematic, literary music-video style with soft lighting and a slightly desaturated color palette.`
- 샷, 카메라, 화자, `<d>`, `<scenetrans>`, `<cutoff>` 규칙은 베이스 모드와 동일.
- 생성 작업은 보통 350~500 영어 단어. 대사가 많으면 단어 수보다 대사 타임라인을 다 담는 것이 우선. 편집 작업은 원본 복잡도에 맞춘다. 단일 샷이라고 짧게 쓰지 않는다.
- 중요한 `<Subject N>`이 처음 분명히 등장할 때 참조 특징, 화면 내 위치, 현재 동작을 묘사하고 이후엔 같은 라벨만 쓴다.
- 프레임 앵커 표현: `the shot begins from <Picture 1>`, `the shot's keyframe corresponds to <Picture 2>`, `the shot ends on <Picture 3>`.
- 참조 주체가 말하면 `<Subject 2> (S1) ... says, <d>[English] ...</d>`. 화면 밖이면 같은 형식에 `off-screen` 표시. 정의된 주체가 아니면 고정된 목소리 묘사 + `(Sx)`.
- 재사용 BGM·사운드트랙 안의 말 신호일 뿐 실제 발화자가 없으면 `<Audio N>`을 소리 출처로 쓰고 `(Sx)`를 만들지 않는다.
- 참조 오디오의 대사·가사를 재사용하거나 재연을 요청받으면 원문과 원어 그대로, 알아들을 수 없는 부분은 `[unclear]`. 문장부호는 `,` `.` `?` `!`만 남기고 장식 기호·이모지 제거, 완결 문장은 `</d>` 앞에 `.` `?` `!`로 끝낸다. 음색·리듬·감정만 참조하면 원 대사를 가져오지 않는다.
- `(Sx)`는 타깃 영상의 실제 발화 순서대로 한 번 부여하고 이후 재사용.

### overall_soundscape / non_diegetic_music (Ref2VA)
정의는 베이스 모드와 같다. 참조 오디오의 복사·참조 관계는 해당 레이어 섹션에만 적는다(환경음·효과음은 soundscape, 관객용 스코어는 music). 대사·가사는 여기서 반복하지 않는다.
```
overall_soundscape: The copied ambience layer from <Audio 1> continues throughout the target video.
non_diegetic_music: <Audio 2> is directly reused as the complete audience-only score.
```

## 5단계: 제출 전 점검

- 모드에 맞는 첫 줄 지시문이 있는가(T2VA는 없음), 그 뒤 빈 줄이 있는가.
- 필드 이름·순서가 정확한가.
- 묘사 전체 길이가 요청 길이(4~15초)와 맞고, 컷 시간이 증가하며 길이 안에 있는가. FL2VA/L2VA의 S.SS가 영상 길이와 같은가.
- 모든 라벨이 정의되어 있고 섹션 간 의미가 일관적인가(미해결 라벨 없음).
- "cinematic", "beautiful" 같은 추상어 대신 구체적인 시각·청각 디테일을 썼는가.
- 줄거리 요약이 아니라 보이고 들리는 것으로 썼는가.
- 대사·화면 글자는 원어 그대로, 나머지는 영어인가.

## 예시 (T2VA, 공식 가이드)
```
integrated_multimodal_description: [Shot 1] Live-action, cinematic, a medium-wide shot frames a baker opening the shutters of a small street bakery before sunrise. The camera pushes in with small amplitude at slow speed as the middle-aged baker with a calm, slightly raspy voice (S1) places a fresh loaf on the wooden counter and says: <d>[English] First batch of the morning.</d> [Shot 2] At 00:05.000, the camera cuts to a close-up of steam rising from the sliced bread while the baker's final words carry over from the previous shot.

overall_soundscape: Wooden shutters scrape open over a quiet street as trays clink softly inside the bakery. The doorbell rings once, followed by light footsteps and the crisp sound of bread being sliced.

non_diegetic_music: A soft acoustic-guitar pattern at a moderate tempo, joined by sparse upright-bass notes and a gentle fade at the end.
```

## 예시 (I2VA, 공식 가이드)
```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, the young woman shown in <Picture 1> remains beside the rain-covered train window, preserving her appearance, clothing, seat position, and the carriage layout. The camera trucks right with small amplitude at slow speed as she lifts her gaze from the folded letter toward the passing city lights. Her reflection moves across the glass while the quiet, breathy young woman (S1) says: <d>[English] I get off at the next station.</d> She folds the letter along its existing crease.

overall_soundscape: The train wheels produce a steady metallic rhythm beneath a low ventilation hum. Rain ticks against the window while paper rustles softly in her hands.

non_diegetic_music: Sustained cello notes at a slow tempo with widely spaced piano tones, gradually decreasing in volume.
```