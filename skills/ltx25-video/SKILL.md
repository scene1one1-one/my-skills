---
name: "ltx25-video"
description: "LTX-2.5 영상 프롬프트를 공식 가이드 형식(단일 샷/멀티샷/I2V/R2V 레퍼런스 시트)으로 쓰고, RunningHub API로 시작 이미지와 영상을 실제로 생성할 때 사용한다."
---

# LTX-2.5 영상 프롬프트 + RunningHub 실행

출처: LTX 공식 프롬프트 가이드 https://ltx.io/blog/ltx-2-5-prompt-guide (2026-08-10), Ingredients IC-LoRA 모델 카드 https://huggingface.co/Lightricks/LTX-2.5-22b-IC-LoRA-Ingredients , 기능 페이지 https://ltx.io/model/capabilities/ingredients . 실행 부분은 2026-10-29 이 프로젝트에서 실제로 돌려 확인한 값이다. 애매하면 위 원문을 다시 읽는다.

## 사용자와 소통

- 사용자는 한국어로 요청한다. 설명과 질문은 한국어로 한다.
- 프롬프트 본문은 영어로 쓴다. 대사(따옴표 안)만 원래 언어(예: 한국어) 그대로 둔다.
- 결과는 (1) 복사해 붙일 프롬프트 코드 블록, (2) 네거티브 프롬프트, (3) 한국어 장면 요약(샷, 카메라, 소리), (4) 실행 설정(해상도, 길이, FPS, 시드) 순으로 준다.
- 빠진 값은 기본값을 고르고 한 줄로 밝힌다: 단일 샷, I2V, 15초, 24fps, 16:9 720p(1280×720, 아래 권장 설정), 실사 시네마틱. 쇼츠 세로 요청이면 9:16(720×1280: 403을 9:16 항목으로, 900 ImageScale을 720×1280으로).
- 실제 생성은 코인이 든다. 사용자가 "만들어줘/돌려줘"라고 했으면 그게 승인이다. 프롬프트만 요청했으면 실행 비용(아래 표)을 한 줄로 알리고 실행 여부를 묻는다.

## 1단계: 모드 판별

- T2V: 텍스트만. 단일 샷 또는 멀티샷.
- I2V: 첫 프레임 이미지 1장. 이미지에서 앞으로 전개. 기본은 단일 연속 테이크(공식 가이드 권장). 이미지에서 컷으로 벗어나려면 프롬프트에 컷을 명시.
- R2V(레퍼런스→영상, LTX 이름은 "Ingredients"): 인물·소품·장소를 정리한 레퍼런스 시트 1장으로 여러 클립에서 같은 외형을 유지. 첫 프레임이 아니라 외형 참조다. 4단계 참고.
- 인물 일관성만 필요하고 R2V 워크플로가 없으면: 같은 인물 레퍼런스로 시작 이미지를 매번 만들고(Qwen 편집, 5단계) I2V로 돌린다. 프롬프트 맨 앞에 50~80단어짜리 고정 인물 묘사 블록을 두고 클립마다 행동·카메라만 바꾼다(LTX 공식 캐릭터 일관성 글).

## 2단계: 프롬프트 요소 (공식 가이드 6요소, 이 순서로)

1. 샷 설정: 장르에 맞는 촬영 용어와 샷 크기(wide establishing, medium-wide, close-up, over-the-shoulder 등).
2. 장면: 조명, 색감, 질감, 분위기. 샷마다 조명 논리는 하나로(촛불이면 촛불, 섞지 않는다).
   - 깜빡임 방지: "flickering candles"처럼 흔들리는 빛을 쓰지 말고 "steady warm candlelight", "soft, even light"로 쓴다. 문살·창살 너머 빛은 모아레·번쩍임을 부르니 "closed paper doors"처럼 고르게. 끝에 "The lighting and exposure stay constant"를 한 문장 넣는다.
3. 행동: 처음부터 끝까지 자연스러운 순서로.
4. 인물: 나이, 머리, 옷, 특징. 감정은 "angry" 같은 라벨 대신 몸의 신호(jaw tight, fists clench, eyes lowered)로.
5. 카메라: 언제 어떻게 움직이는지, 피사체 기준으로. 움직인 뒤 피사체가 어떻게 보이는지도 쓴다("…pushes in until the king's face fills the frame").
6. 오디오: 환경음, 음악, 말, 노래. 대사는 큰따옴표 안에, 필요하면 언어·억양 명시("says in Korean, in a low, furious voice, \"…\"").

## 3단계: 구조

### 단일 샷 (기본)
- 한 문단, 현재형 동사, 4~8문장.
- 디테일 양은 샷 크기에 맞춘다(클로즈업일수록 자세히).
- 인물과 행동은 적게, 명확하게. 붐비는 화면은 망가진다.

### 대사 많은 장면 (스크린플레이 스타일)
- 장면 헤더, 인물 큐, 따옴표 대사를 써도 된다. 현재형, 몸의 감정 신호, 따옴표 대사 원칙은 그대로.
- 길이는 장면 복잡도에 맞추되 모든 문장이 보이거나 들리는 구체 정보를 담아야 한다.

### 멀티샷 (2~4컷)
- 장면 전체를 시간순 한 문단으로. 샷 리스트·번호·슬러그라인 금지(쓰면 컷도 산문으로 설명).
- 컷마다 네 가지:
  1. 전환 이름: "A hard cut transitions to…", "The view cuts to a close-up of…", "A match cut connects…", "The image dissolves into…"
  2. 새 샷 재설정: 샷 크기, 각도, 화면 속 인물, 바뀌었으면 조명.
  3. 정체성 유지: 같은 식별어 반복("the minister in the dark red robe, earlier below the dais, now…").
  4. 오디오 연속성: "the drum continues across the cut", "the dialogue drops; only wind remains."
- 샷마다 역할 하나(설정 → 디테일 → 반응, 또는 wide → medium → close-up). 시간 연결어(Initially, A moment later, Simultaneously) 사용.
- 이유 없는 지리·의상 변화 금지(시간·장소 점프면 그렇다고 쓴다).
- 클로즈업 컷에서는 의상이 다른 인물 쪽으로 번진다(실제로 신하가 왕처럼 금색 옷을 입고 나옴). 컷마다 그 인물의 옷·모자·수염을 다시 명시한다.
- I2V 한 번에 3컷(15초)도 된다(약 47코인). 컷을 문단으로 나누고 각 문단을 "A hard cut transitions to a close-up of…"로 시작하면 잘 끊긴다. 예: `/mnt/project-files/joseon-scene/prompt_3cut.txt`
- I2V에서는 립싱크 대사·연속 동작이 필요하면 단일 샷을 유지한다.

### 공식 멀티샷 예시
```
A wide shot frames a rainy city intersection at dusk, neon signs reflecting on wet asphalt. A young woman in a yellow raincoat walks toward camera, gripping a folded newspaper, while cars hiss past behind her. Soft synth music and distant traffic fill the air. A hard cut transitions to a medium close-up of her face under the hood, raindrops catching the neon as she looks off-screen left; the synth score continues across the cut, traffic muffled. She whispers, "He's late." Another hard cut jumps to a low-angle shot of a man's scuffed boots stepping into a puddle at the curb; the music drops to a low drone. He lifts his head into frame — short dark hair, soaked jacket — and smiles toward her off-screen as a bus rumbles past.
```

### 약점 (공식 가이드)
- 화면 글자: 짧은 글자는 나아졌지만 철자·프레임 간 일관성 보장 없음. 제목·자막·현판 글씨는 후반 편집에서 넣는다.
- 복잡한 물리(난전, 폭발, 군중 충돌): 아티팩트. 단순하고 그럴듯한 동작이 안정적.
- 한국어 대사: 발음이 어색하면 대사를 짧게 하거나, 효과음만 생성하고 대사는 TTS/더빙으로.

### 유용한 용어
- 장르: Period drama, Documentary, Film noir, Epic, Thriller
- 조명: Steady candlelight, Natural sunlight, Dramatic shadows / 질감: Rough stone, Worn fabric / 분위기: Fog, Dust, Smoke
- 카메라: Follows, Tracks, Pans across, Circles around, Tilts upward, Pushes in / pulls back, Overhead view, Handheld movement, Over-the-shoulder, Static frame
- 템포: Slow motion, Lingering shot, Continuous shot, Sudden stop / 필름: Film grain, Depth of field
- 목소리: Resonant voice with gravitas, Whisper, Mutter, Shout

## 4단계: R2V (Ingredients 레퍼런스 시트)

### 무엇인가
- LTX-2.5-22B용 IC-LoRA `ltx-2.5-22b-ic-lora-ingredients-0.9.safetensors`(2026-09-10 공개, 프리뷰). 레퍼런스 시트 한 장에 있는 인물·소품·장소를 영상에서 같은 모습으로 유지한다.
- 일반 T2V가 아니다. 시트 없이 쓰면 안 되고, 시트에 없는 것은 나오지 않는다.
- 학습 버킷: 768×448, 121프레임(약 5초), 24fps. 다른 해상도·더 긴 길이는 분포 밖이라 품질이 떨어진다. 쇼츠용 긴 장면은 5초 클립 여러 개로 나눠 같은 시트로 생성한 뒤 편집으로 잇는다.

### 레퍼런스 시트 만들기
- 검은 배경, 글자 없음, 요소마다 깨끗한 패널 하나.
  - 인물: 정면 얼굴 클로즈업 + 전신 턴어라운드(앞/옆/뒤).
  - 소품: 제품 사진처럼 단독 렌더(예: 홀, 옥새, 칼).
  - 장소: 장소 패널 하나(예: 편전 내부).
- 중요한 인물·소품은 패널을 크게. 작거나 빽빽하면 외형이 흔들린다.
- 시트는 출력 해상도(768×448)로 맞추고, 정지 이미지를 출력 길이·fps와 같은 정지 영상(최소 121프레임)으로 반복해 넣는다(`reference_downscale_factor`=1). 121프레임보다 짧으면 깨진다.
  ```bash
  ffmpeg -loop 1 -i sheet.png -t 5.042 -r 24 -vf scale=768:448 -pix_fmt yuv420p sheet_121f.mp4
  ```
- 시트 이미지는 Qwen Image로 생성 가능(5단계). 프롬프트 예: "character reference sheet on a pure black background, no text: left large panel a front-facing close-up of …, right panel full-body turnaround front, side, back of the same man …, bottom panel an ivory hol tablet product render, bottom-right panel an empty Joseon throne hall interior".

### R2V 프롬프트 형식 (두 부분, 라벨 그대로)
```
Reference sheet: <시트의 모든 패널을 묘사: 인물 외형, 의상, 소품, 장소>

Generated video: <일어나는 일: 샷, 행동, 카메라, 소리 — 2~3단계 규칙 그대로>
```
- `Reference sheet:`는 생김새, `Generated video:`는 동작. 둘을 나눠 고칠 수 있다.
- 시트에 있는 패널은 전부 묘사한다. 안 나오는 요소는 자기 패널을 주고 여기서 묘사.
- 네거티브: `worst quality, inconsistent motion, blurry, jittery, distorted`
- 설정: LoRA 강도 1.0(HF 모델 카드, 가중치 사전 스케일). ltx.io 기능 페이지는 강도 1.4, 30스텝, guidance 4.0, STG `stg_v` 블록 29 스케일 1.0을 권장한다. 1.0으로 시작하고 외형이 약하면 1.4로 올린다.
- ComfyUI 공식 워크플로: ComfyUI-LTXVideo `example_workflows/2.5/LTX-2.5_ICLoRA_Ingredients_Single_Stage_Distilled.json`. 시트 정지 영상은 control/reference 입력에 연결해야 한다(일반 LoRA 로더만 쓰면 조건이 안 걸린다).

### R2V 예시
```
Reference sheet: A Korean king in his forties with a short black beard, wearing a crimson gonryongpo robe with gold dragon roundels and a black ikseongwan cap, shown as a front-facing close-up and a full-body turnaround. An elderly Korean minister with a grey beard in a dark red danryeong robe with a crane rank badge and a black winged samo hat, shown as a close-up and turnaround. An ivory hol tablet. A dim Joseon throne hall with red pillars and an Irworobongdo screen.

Generated video: A medium shot inside the candlelit throne hall at dusk. The minister in the dark red robe kneels below the dais and lifts the ivory tablet to his chest while the king on the throne leans forward, his jaw tight. The camera slowly pushes in toward the king's face. The king says in Korean, in a low, furious voice, "물러가라." Candle flames crackle and silk rustles in the silence.
```

### RunningHub에서 R2V
- 2026-10-29 기준 RunningHub에서 Ingredients 공개 워크플로는 확인하지 못했다. 사용자가 링크를 주거나 RunningHub에서 "LTX 2.5 Ingredients / ref sheet" 워크플로를 찾으면, 5단계의 `getJsonApiFormat`으로 노드를 확인한 뒤 같은 방식으로 돌린다(시트는 영상으로 업로드, fileType=input).
- 찾지 못하면 대안(이 프로젝트에서 검증한 캐릭터 시트 파이프라인):
  1. Qwen으로 인물별 캐릭터 시트 생성(예: `sheet_king.png`, `sheet_minister.png`).
  2. Qwen 편집에 시트를 레퍼런스로 넣어 컷별 시작 이미지 생성. Qwen은 LoadImage 노드를 추가해 `images.image_1`~`image_3`으로 최대 3장 레퍼런스를 받는다.
  3. 컷별 LTX-2.5 I2V(예: 4초/6초/5초) → ffmpeg로 이어 붙이기.
  - 주의: 앞쪽에 사람이 걸친 오버더숄더 시작 이미지는 그 사람이 돌아서 카메라 쪽으로 걸어 나온다. 측면 와이드 구도를 쓴다.
  - 사용자는 대사가 15초를 꽉 채우길 원한다. 컷 길이에 맞춰 대사를 배분한다.
  - 이 경우 R2V가 아니라 I2V라는 점을 사용자에게 밝힌다.

## 5단계: RunningHub API로 실행

### 환경
- 프로젝트 클라우드 환경(Default)에 `RUNNINGHUB_API_KEY`, `RUNNINGHUB_HOST`(https://www.runninghub.ai), `RUNNINGHUB_EDIT_WORKFLOW_ID`(Qwen Image 2.1)가 있다. 키를 출력하거나 파일에 쓰지 않는다.
- 엔드포인트(POST, JSON, 모두 `apiKey` 포함):
  - `/api/openapi/getJsonApiFormat` {workflowId} → 노드 구조 확인
  - `/task/openapi/upload` multipart(apiKey, fileType=input, file) → 반환 fileName을 이미지 노드에
  - `/task/openapi/create` {workflowId, nodeInfoList:[{nodeId, fieldName, fieldValue}]} 또는 {workflowId, workflow:"<전체 JSON 문자열>"}
  - `/task/openapi/status` {taskId} → QUEUED/RUNNING/SUCCESS/FAILED
  - `/task/openapi/outputs` {taskId} → 결과 파일 URL
- 폴링은 15~20초 간격. 실패하면 outputs/status 응답의 에러 메시지를 사용자에게 그대로 요약.

### 시작 이미지 (Qwen Image 2.1, 약 8코인, 40초)
- nodeInfoList로는 안 되고 전체 `workflow` 덮어쓰기로만 동작한다. getJsonApiFormat으로 받은 JSON을 고쳐 문자열로 보낸다.
  - `459:451` UNETLoader `unet_name` = `qwen_image_2.1_int8_convrot.safetensors` (원본의 `qwen2\` 접두어를 지운다. 백슬래시 경로가 깨진다)
  - 텍스트→이미지: `459:468` switch=true, 노드 `470`(LoadImage) 삭제, 그 노드를 가리키는 `images.image_1` 입력 제거
  - 레퍼런스 편집(인물 유지): `470`에 업로드한 레퍼런스 이미지를 넣고 switch는 편집 쪽으로 둔다(먼저 JSON으로 분기 확인)
  - `13` ResolutionSelector `aspect_ratio` = `16:9 (Widescreen)` (쇼츠 세로면 9:16 항목)
  - 프롬프트는 `459:474` TextEncodeQwenImage21
- Krea 워크플로(`RUNNINGHUB_KREA_WORKFLOW_ID`)는 VAE 오류로 실패한다. 쓰지 않는다.

### LTX-2.5 I2V (워크플로 2087902142043815938)
https://www.runninghub.ai/post/2087902142043815938/ — 최대 19초, 오디오 포함, 2단계(저해상도 → 잠재 업스케일).

**권장 설정(v3, 얼굴 깨짐 + 깜빡임 수정, 기본값으로 쓴다).** nodeInfoList가 아니라 getJsonApiFormat으로 받은 JSON을 고쳐 전체 `workflow` 문자열로 보낸다(새 노드 추가가 필요하다). 검증된 스크립트: `/mnt/project-files/joseon-scene/run_ltx25_facefix.py`, JSON: `ltx25_i2v_facefix_api.json`. 스크립트는 작업 폴더에 getJsonApiFormat 응답 `wf_2087902142043815938.json`과 프롬프트 파일(`vidprompt3.txt`)이 있다고 가정하고 `python3 run_ltx25_facefix.py <업로드 fileName> 1.33`으로 실행한다. 길이·프롬프트 파일·출력 이름은 스크립트에서 바꾼다.

| 노드 | 필드 | 값 | 이유 |
|---|---|---|---|
| 395 LoadImage | image | 업로드한 시작 이미지 fileName | |
| 409 PrimitiveStringMultiline | value | 영상 프롬프트 | |
| 419 CLIPTextEncode | text | 네거티브(아래) | |
| 403 ResolutionSelector | aspect_ratio / megapixels | `16:9 (Widescreen)` / **1.33**(1536×864) | 720p보다 크게 렌더 후 축소 |
| 433 ResizeImageMaskNode | resize_type.longer_size | **1536** (원래 512) | 입력 이미지가 작아 작은 얼굴이 뭉개짐 |
| 436 LTXVPreprocess | img_compression | **12** (원래 18) | 얼굴 디테일 |
| 422, 446 KSamplerSelect | sampler_name | **euler** (원래 euler_ancestral) | ancestral은 매 스텝 노이즈를 다시 넣어 질감이 끓고 번쩍임 |
| 449 VAEDecodeTiled | temporal_size / temporal_overlap / tile_size / overlap | **128 / 32 / 512 / 64** | 기본값(4096/32/768)은 15초에서 OOM, 64/8은 덩어리 경계에서 번쩍임 |
| 900 (새 노드) ImageScale | image=["449",0], lanczos, 1280×720, crop disabled | 정확한 720p로 축소(세로면 720×1280) |
| 452 VHS_VideoCombine | images | ["900",0] | |
| 413 / 425 / 423 | value / value / noise_seed | 길이(초, 최대 19) / 24 / 고정 시드 | |

- 비용: 15초 약 49코인, 약 4분(2026-10-29). 예전 기본(0.92MP, 1280×704, 32코인)은 작은 얼굴이 뭉개지고 깜빡임이 있어 쓰지 않는다.
- 권장 네거티브:
```
text, subtitles, watermark, logo, modern clothing, Chinese or Japanese costume, extra people, distorted face, deformed face, melting face, asymmetric eyes, blurry face, distorted hands, extra fingers, face morphing, identity change, flicker, flickering light, flashing, strobing, exposure changes, shimmering patterns, moire, blurry, low quality, cartoon
```
- 시드는 고정하고 2~3개만 바꿔 본다. 프롬프트를 고칠 때는 시드를 그대로 둬야 비교가 된다.
- RunningHub는 동시 작업이 약 2개까지다. `421 TASK_QUEUE_MAXED`가 오면 잠시 뒤 다시 보낸다.

### 결과 저장
- 결과 mp4와 시작 이미지, 사용한 프롬프트·설정을 정리한 .md를 `/mnt/project-files/<장면-이름>/`에 저장하고 메시지에 첨부한다. 예: `/mnt/project-files/joseon-scene/`.
- 받으면 ffprobe로 해상도·길이·오디오 트랙을 확인하고, 프레임 몇 장을 뽑아 얼굴·손이 망가졌는지 직접 본 뒤 결과를 알린다.

## 6단계: 제출 전 점검

- 모드에 맞는 구조인가(단일 샷 한 문단 / 멀티샷 컷마다 4요소 / R2V 두 라벨).
- 현재형, 감정은 몸 신호, 대사는 큰따옴표 안 원어 그대로.
- 조명 논리가 샷마다 하나인가, 인물·행동이 과하지 않은가.
- 카메라 움직임과 움직인 뒤의 화면이 있는가. 소리 묘사가 있는가.
- 화면 글자를 모델에 맡기지 않았는가(후반에서 넣기).
- I2V는 프롬프트가 시작 이미지의 인물·의상·배치와 맞는가. R2V는 시트의 모든 패널을 묘사했는가.
- 실행 설정: v3 권장값(1536 입력, 1.33MP 렌더 → 1280×720, 압축 12, euler, 타일 128/32), R2V는 768×448·121프레임·24fps.
- 조명을 "steady"로 썼는가(flickering 금지), 멀티샷 컷마다 의상을 다시 썼는가.

## 예시 (I2V 3컷, 이 프로젝트에서 실제 생성, 15초 1280×720, v3 설정)
```
A medium-wide shot inside a dim Joseon Dynasty throne hall at dusk, lit by steady warm candlelight and soft, even dusk light through closed paper doors, with the Irworobongdo screen of sun, moon and five peaks behind the throne. The king, a man in his forties in a crimson dragon-embroidered robe and black ikseongwan cap, grips the armrests of his throne and leans forward, while in the foreground an elderly grey-bearded minister in a dark red official robe with a crane badge and black winged samo hat holds an ivory tablet against his chest. The king strikes the armrest with his palm and says in a low, furious voice, "감히 과인의 명을 거역하겠다는 것이냐."
A hard cut transitions to a close-up of the elderly minister's face from the front, his grey beard and black winged samo hat in sharp focus, candlelight on his wrinkled skin. He slowly lowers his eyes, then raises them and answers firmly, "전하, 신은 목이 떨어질지언정 이 상소를 거둘 수 없사옵니다."
A hard cut transitions to a close-up of the king's face under the black ikseongwan cap, the sun and moon screen softly blurred behind him. His jaw tightens, his eyes narrow, and he stares down in silence as his breathing grows heavy.
The lighting and exposure stay constant across all three shots. Throughout, the hall is quiet except for the faint crackle of candles, rustling silk, and wind pressing against the doors.
```
네거티브는 위 권장 네거티브를 쓴다.