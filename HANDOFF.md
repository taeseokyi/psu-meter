# 인수인계 문서 (HANDOFF)

**프로젝트**: 해수 수조 광학식 염도계 (psu-meter)
**작성**: 2026-08-31 · Claude 세션 결과 정리
**대상**: 이 작업을 이어받는 사람 또는 다음 세션

이 문서는 "무엇을 만들었나"가 아니라 **"왜 이렇게 결정했고, 무엇이 아직 안 풀렸나"** 를 적은 것입니다.
결과물 목록은 [README.md](README.md), 부품은 [BOM.md](BOM.md)를 보세요.

---

## 1. 요청의 출발점

대화는 ESP32-S3 / HC-05 배선 질문에서 시작해 다음으로 이어졌습니다.

1. "아두이노로 염도를 안정적으로 측정할 수 있나" → 전기전도도(EC) 방식 설명
2. **"전기전도도 말고 광학적으로 안 되나? LED와 센서로?"** ← 프로젝트의 실질적 시작
3. 상시 침지 대신 펌프로 물을 퍼와 측정하는 구조 제안 (사용자 아이디어)
4. 측정 사이에 셀을 보관액으로 채우는 구조 제안 (사용자 아이디어)
5. 파워포인트 설계 문서 → 부품 조달 → 배선도 → 측정 헤드 조립 → 3D 프린팅 대응

**사용자 환경**: 해수 리프 수조. HC-06 블루투스 + 스마트폰 시리얼 터미널로 명령. 하루 2회 자동 측정.
**제약**: 알루미늄 절삭 가공은 불가, 3D 프린팅만 가능.

---

## 2. 핵심 아키텍처 — 이것만은 반드시 이해할 것

> **매 측정 사이클마다 RO-DI(0 PSU)와 표준액(35 PSU) 두 점으로 자가보정한다.**

이 한 줄이 설계 전체를 지탱합니다. 왜 중요한지:

| 오차원 | 절대 측정 | 차분 측정 | 비고 |
|---|---|---|---|
| 온도 | 0.667 PSU/°C | **0.0015 PSU/°C** | 450배 개선 |
| LED 파장 드리프트 | 0.19 PSU/nm | 거의 0 | 수 초 간격이면 무시 |
| LED 광량·검출기 게인 | 직접 영향 | 0 | 비율 연산으로 제거 |
| 기구 열팽창 (250 mm Al) | 0.091 PSU/°C | 거의 0 | 차분으로 상쇄 |

**파생 결론 세 가지** — 이걸 모르면 설계를 잘못 수정하게 됩니다.

**(a) 프리즘을 자유롭게 바꿔도 된다.** 검량선의 기울기·절편을 매번 실측하므로 프리즘의 정확한 굴절률·형상·검출팔 길이를 미리 알 필요가 없습니다. 계산값은 "감도가 충분한가, 두 보정점이 128 px 안에 들어오는가"만 확인하는 용도입니다. → **값싼 직각/정삼각 프리즘으로 먼저 시작해도 됩니다.**

**(b) 기구 정밀도 요구가 낮다.** 그래서 3D 프린팅이 가능합니다. 거울로 광로를 접어도 됩니다.

**(c) 온도 센서의 절대 정확도가 필요 없다.** 같은 센서로 표준액과 시료를 재고 차이만 쓰므로 절대 오차는 상쇄됩니다. 필요한 건 분해능뿐이고, DS18B20의 0.0625 °C면 0.042 PSU 수준입니다.

**전제 조건**: 표준액과 시료가 **같은 온도**여야 합니다. 이게 깨지면 위 표가 전부 무의미해집니다.

---

## 3. 주요 설계 결정과 그 이유

각 항목은 "이걸 바꾸려는 사람"이 왜 그러면 안 되는지 알 수 있게 적었습니다.

### 광학 방식 — 임계각(critical angle)

요구 분해능이 **굴절률의 1/14,800** (±0.5 PSU 기준 Δn ≈ 9.1×10⁻⁵)입니다. 흡광도 방식은 소금이 가시광을 거의 흡수하지 않아 불가능하고, 프리즘 편각 방식은 Δn에 대한 변위가 너무 작아 광학 벤치 길이가 비현실적입니다. 임계각 방식만 남습니다. 상용 디지털 굴절계와 같은 원리입니다.

### 광원 — 단색 LED 590 nm (백색 절대 불가)

물의 분산 때문에 **파장 1 nm = 0.19 PSU**입니다.

| 광원 | 스펙트럼 폭 | 경계 번짐 |
|---|---|---|
| 백색 LED | ~150 nm | **28 PSU** — 측정 범위 전체를 덮음, 사용 불가 |
| 단색 LED | ~20 nm | 3.8 PSU |
| 레이저 다이오드 | <1 nm | 0.2 PSU (단 스페클 노이즈) |

덤: 20 nm LED의 번짐 폭 3.8 PSU가 34 PSU ± 2 PSU를 덮어, 리프 수조가 실제로 머무는 범위와 우연히 일치합니다.

### 프리즘 — BK7 (저굴절이 오히려 유리)

| 유리 | 임계각 | 감도 |
|---|---|---|
| BK7 n=1.5168 | 61.93° | **253 µrad/PSU** |
| SF계 n=1.72 | 51.09° | 167 µrad/PSU (−34 %) |

임계각이 클수록 cos θc가 작아져 각도 변화가 증폭됩니다. 비싼 고굴절 유리가 불리합니다.
형상은 반원통(hemicylinder)이 이상적 — 곡면으로 들어온 빛이 중심을 향하면 굴절 없이 통과해 광로 계산이 단순합니다.

### 검출기 — TSL1401 리니어 어레이 (2분할 포토다이오드 아님)

처음엔 2분할 포토다이오드 차동 방식을 검토했으나 기각했습니다.
**RO-DI 보정점이 34 PSU 밖에 있어서 2분할 검출기의 선형 구간(약 ±2 PSU)으로는 볼 수 없습니다.** 1점 보정만 가능해지고, 그러면 오프셋 드리프트는 잡아도 **감도(기울기) 드리프트를 못 잡습니다.**

TCD1304(고해상도 리니어 CCD)도 기각 — 1~4 MHz ADC가 필요해 아두이노로는 불가능합니다. 실제로 Arduino 포럼에 ESP8266으로 200 kHz밖에 안 나와 실패한 사례가 있습니다. TSL1401은 클럭이 훨씬 느려 나노로도 충분합니다.

### 측정 위치 — 수조 밖 플로우셀 (상시 침지 아님)

수조에 광학면을 담그면 며칠 만에 생물막이 앉습니다. 임계각 측정은 표면에서 파장 이하(수백 nm) 두께만 보기 때문에 **눈에 안 보이는 얇은 막도 그대로 오차**가 됩니다. 해양 계류 광학 센서 분야의 오랜 난제이고, 상용 장비는 와이퍼·구리 차폐·UVC 같은 방오 기구를 따로 답니다.

→ 펌프로 필요할 때만 물을 퍼와 재고, 유휴 시에는 셀을 표준액으로 채워둡니다.

### 보관액 — 35.0 PSU 표준액 (RO-DI 아님)

잔류액의 굴절률 차이가 그대로 오차입니다. 오차 ≈ `잔류율 × (보관액 염도 − 34)`.

| 보관액 | 1 % 잔류 시 오차 |
|---|---|
| RO-DI (0 PSU) | 0.34 PSU |
| 35 PSU 표준액 | **0.01 PSU** |

**34배 차이**입니다. 게다가 유휴 셀이 늘 알려진 표준액으로 차 있으니 매 사이클 직전 보정점이 공짜로 생기고, 수조로 넘어가도 그냥 해수라 무해합니다.

셀을 비워 말리는 것은 **금지** — 해수가 마르면 염 결정이 남아 측정면을 망칩니다.

### 펌프 — 페리스탈틱 4개 (밸브 아님)

정지 시 튜브가 눌려 **사이펀이 원천 차단**됩니다. 수조에 연결된 장치에서 이건 타협 대상이 아닙니다. 자흡이 되고 액이 튜브 안에만 있어 교차오염도 없습니다.
예산이 문제면 밸브 + 펌프 1개로 줄일 수 있지만 침수 대책을 따로 세워야 합니다.

### 오손 방지 — UVC LED (화학약품 아님)

표백제는 미량이라도 수조 생물을 죽입니다. 자동 루프 안에 두면 안 됩니다.
UVC LED는 소모품이 없고 수조 유입 위험이 원천적으로 없습니다. 단 **UVC는 실리콘·PMMA·접착제를 열화**시키므로 근처는 PTFE나 유리를 쓰고, 프리즘 접착에 UV 경화 접착제는 금지입니다.
탄산칼슘 스케일은 UVC로 안 되므로 월 1회 묽은 구연산 순환을 따로 넣습니다.

### 3D 프린팅 — 광학면에서 좌우 클램셸 2분할

경사진 보어는 FDM으로 못 뚫습니다. **광선이 지나는 평면에서 두 쪽으로 가르면** 각 쪽에 반원 홈이 위를 향한 채 남아, 서포트 없이 매끈한 채널이 나옵니다.
250 mm 팔은 출력하면 휘므로 허브에서 각도만 잡고 검은 파이프를 끼웁니다. O-링 홈은 FDM 정밀도가 안 나오니 **1 mm 실리콘 시트 평면 가스켓**으로 대체합니다.

---

## 4. 발견해서 고친 오류

**두 광학팔 사이각 계산 오류** (2026-08-31 수정 완료)

`design_calc.py`에서 `180 − 2θc = 56.14°`로 계산했으나 실제로는 **`2θc = 123.86°`** 입니다.
θc = 45°일 때 두 식이 우연히 일치해서 검증에서 놓쳤습니다. 이대로 가공했으면 광로가 전혀 맞지 않았을 것입니다.

수정본에는 가공에 쓰기 편한 **"각 팔의 수평 기준 각도 = 28.07°"** 항목도 추가했습니다.

> **주의**: `fig_optics.png`(설계 문서 3장)에는 이 각도 표기가 없어 영향이 없지만, 혹시 초기 버전 그림을 따로 저장해 두셨다면 "두 팔 사이각 56.1°"라고 적힌 것은 폐기하십시오.

---

## 5. 검증된 것과 안 된 것

### 계산으로 확정 (`design_calc.py`로 재현 가능)

굴절률 경험식은 [Oregon State University, Parrish Research Group](https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature)의 계수를 사용했습니다. 본 프로젝트의 **모든 수치는 이 식에서 직접 계산**한 것이며 인용값이 아닙니다.

- dn/dS = 1.81×10⁻⁴ /PSU, dn/dT = −1.21×10⁻⁴ /°C, dn/dλ = −3.41×10⁻⁵ /nm
- 임계각 61.93° (BK7, 34 PSU, 26 °C, 590 nm), 감도 253 µrad/PSU
- 250 mm에서 0.997 px/PSU, RO-DI 보정점은 33.6 px 떨어짐
- 오차 예산 RSS = 0.117 PSU (표준액 정확도 0.1 PSU가 지배적)

### 확인된 조달처

- TSL1401CL 모듈 — 알리익스프레스 다수 (한 곳 표기가 약 US$58, 편차 큼)
- 연동펌프 — 디바이스마트 [BWP-2752P](https://www.devicemart.co.kr/goods/view?no=12759593), [ada-3910](https://www.devicemart.co.kr/goods/view?no=15531016)

### 확인 못 한 것 (⚠ 인수받는 사람이 확인해야 함)

| 항목 | 사유 |
|---|---|
| **디바이스마트 가격·재고 전반** | 사이트가 자동 접근을 차단. 검색엔진에 색인된 URL 2건 외에는 페이지를 열지 못함 |
| **BK7 반원통 렌즈 실제 구매 가능성** | Alibaba B2B(MOQ 미확인)와 광학 전문점만 확인. 개인 소량 구매 경로 불명 |
| **TSL1401 모듈의 렌즈 탈거 가능 여부** | 상품 사진으로 나사식인지 접착인지 확인 필요. 렌즈가 붙어 있으면 이 설계는 동작하지 않음 |
| **590 nm LED의 실제 반치폭(FWHM)** | 데이터시트 확인 필요. 20 nm를 가정했음 |
| **일체형 모듈 대안** | 산업용 인라인 굴절계(Pyxis RT-50, Anton Paar L-Rix, MISCO IRIS, ATAGO)는 존재하나 가격 미확인. 포켓 굴절계(ATAGO PAL-06S)는 ±2 PSU로 목표에 한참 못 미침 |

### 전혀 검증 안 된 것

**실물 제작·측정이 하나도 없습니다.** 전부 계산상 설계입니다. 특히 다음은 실물에서 깨질 수 있습니다.

- 그림자 경계가 실제로 관측 가능한 대비로 생기는지
- 미광 차단이 충분한지
- 기포 대책이 실효가 있는지
- 3D 출력물의 방수·강성이 버티는지

---

## 6. 다음 단계 (우선순위 순)

### 1순위 — 광학 벤치 가조립 ★ 최대 기술 위험

값싼 직각/정삼각 프리즘 + 590 nm LED + TSL1401로 임시 벤치를 세우고 **그림자 경계가 보이는지** 확인합니다.
측정면에 RO-DI 한 방울, 표준액 한 방울을 번갈아 올려 **경계 픽셀이 30 px 이상 이동**하면 성공입니다.

여기서 실패하면 나머지 설계가 전부 무의미하므로, **반드시 이것부터** 하십시오. 유체부·기구부에 돈과 시간을 쓰기 전에 확인해야 합니다.

확인 순서:
1. 공기 중 — 어레이 전체가 밝아짐 (전 각도 전반사, 풀스케일 기준점)
2. RO-DI 한 방울 — 경계선 등장
3. 표준액 한 방울 — 경계선 이동

### 2순위 — 아두이노 스케치 (미작성)

필요한 것: TSL1401 프레임 읽기 → 서브픽셀 에지 검출 → 블루투스 명령 파서 → 시퀀스 상태머신.
명령어 세트와 10단계 시퀀스는 설계 문서 13~14장에 정의되어 있습니다.

주의: SoftwareSerial은 송신 중 인터럽트를 막으므로 TSL1401 프레임 캡처와 겹치지 않게 순차 처리해야 합니다.

### 3순위 — 프리즘 실측 후 STL 설계

클램셸 파라메트릭 모델(OpenSCAD 권장)을 만들려면 **실제 프리즘 치수**가 필요합니다. 프리즘을 먼저 구입하십시오.

### 4순위 — 유체부

펌프 4개 + MOSFET을 채널 하나씩 검증한 뒤 시퀀스를 붙입니다. **플라이백 다이오드를 먼저 다십시오.**

---

## 7. 인수받는 사람이 흔히 저지를 실수

| 실수 | 결과 |
|---|---|
| TSL1401 모듈의 광각 렌즈를 그대로 둠 | 각도 분포가 뭉개져 **경계선 자체가 안 생김** |
| 백색 LED 사용 | 번짐 28 PSU, 측정 불가 |
| IRF520 MOSFET 모듈 구입 | 로직레벨 아님. 반쯤 켜진 채 발열하다 고장 |
| MOSFET 게이트 풀다운 생략 | 전원 투입·리셋 시 펌프 폭주 → 물난리 |
| HC-06 RXD 직결 | 5 V 인가로 모듈 손상 |
| 플라이백 다이오드 방향 반대 | 전원 투입 즉시 단락 |
| 셀을 비워서 보관 | 염 결정이 측정면에 남음 |
| 프리즘을 접착제로 고정 | 유리에 응력, UV 경화형은 UVC에 열화 |
| 광학 팔을 별도 마운트 2개로 제작 | 서로 움직여 감도를 드리프트로 상실 |
| 온도 센서를 수조에 설치 | 셀 온도와 다름. **셀 유로 안**에 넣어야 함 |

---

## 8. 열려 있는 설계 질문

**검출팔 250 mm의 하우징 크기.** 상자가 약 500 × 150 mm가 됩니다. 부담되면 팔 중간에 평면거울을 넣어 광로를 접으면 절반이 됩니다. 거울 각도 오차는 2점 보정이 흡수하므로 정밀한 거울일 필요는 없습니다. 아직 도면화하지 않았습니다.

**온도 균일화 방식이 두 번 바뀌었습니다.** 처음엔 섬프 침수 → 이후 단열 + 알루미늄 열용량 → 3D 프린팅 대응으로 알루미늄 평판 + 단열 + 코드 보정. 최종안은 `fig_printed.png` 기준이지만 **실측으로 ΔT가 얼마나 남는지 확인이 필요합니다.**

**수조물의 온도 도달.** 수조(26 °C)에서 실온 셀로 들어오는 물이 표준액과 온도가 다를 수 있습니다. 플러시 볼륨을 늘리거나 단열 박스 안에 예열 코일을 넣는 방안이 있으나 아직 정량화하지 않았습니다.

**표준액 소모량.** 셀 2 mL × 하루 4회 = 월 240 mL 내외로 추정했으나 실제 플러시 볼륨에 따라 달라집니다.

---

## 9. 참고자료

- [Index of Refraction of Seawater and Freshwater as a Function of Wavelength and Temperature — Oregon State University, Parrish Research Group](https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature) — 모든 수치의 근거
- [Digital handheld refractometer — Wikipedia](https://en.wikipedia.org/wiki/Digital_handheld_refractometer) — 임계각·그림자 경계 원리
- [TSL1401CL 데이터시트 — ams-osram (Mouser)](https://www.mouser.com/datasheet/2/588/TSL1401CL-1214741.pdf) · [제품 페이지](https://ams-osram.com/products/photodetectors/photodiodes/ams-tsl1401cl-linear-array-sensor)
- [LED refractometry with Arduino — Arduino Forum](https://forum.arduino.cc/t/led-refractometry-with-arduino/684120) — TCD1304 MHz 샘플링 한계 사례
- [Interfacing Arduino Boards with Optical Sensor Arrays — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10747067/)
- [Biofouling protection for marine environmental sensors — Ocean Science](https://os.copernicus.org/articles/6/503/2010/os-6-503-2010.pdf) · [Antifouling Strategies for Sensors Used in Water Monitoring — Sensors (MDPI)](https://www.mdpi.com/1424-8220/21/2/389)
- [UVC LEDs reduce marine biofouling — Laser Focus World](https://www.laserfocusworld.com/lasers-sources/article/16547014/photonic-frontiers-leds-uvc-leds-reduce-marine-biofouling)
- [The IRF520 FET switching module — arduinodiy](https://arduinodiy.wordpress.com/2020/11/22/the-irf520-fet-switching-module/) · [IRF520 not a good choice for Arduino — Arduino Forum](https://forum.arduino.cc/t/irf520-mosfet-not-a-good-choice-for-arduino-use/702391)
- [HC-05·HC-06 ZS-040 보드 — Martyn Currey](https://www.martyncurrey.com/hc-05-and-hc-06-zs-040-bluetooth-modules-first-look/) · [ProtoSupplies](https://protosupplies.com/product/hc-05-zs-040-bluetooth-module/)
- [ATAGO PAL-06S 사양 (±2‰)](https://novatech-usa.com/Products/Seawater-Salinity/4406-PAL-06S_2.html) — 시판 포켓 굴절계 정확도 비교 기준
- 산업용 인라인 굴절계: [Pyxis RT-50](https://www.pyxis-lab.com/product/rt-50-prism-inline-refractometer/) · [Anton Paar L-Rix](https://www.anton-paar.com/us-en/products/details/l-rix/) · [MISCO IRIS](https://www.misco.com/product/iris-inline-process-refractometer/) · [ATAGO](https://www.atago.net/en/products-prm-top.php)
