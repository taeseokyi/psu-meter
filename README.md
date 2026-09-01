# 해수 수조 광학식 염도계 (psu-meter)

해수 수조의 염도를 **34 PSU 근처로 유지·모니터링**하기 위한 광학식 염도 측정 장치의 설계 자료입니다.
전기전도도 방식이 아니라 **임계각 굴절계(critical-angle refractometer)** 방식이며, 하루 2회 무인 자동 측정을 목표로 합니다.

> **현재 상태 — 설계 단계.** 계산과 도면은 완료되었으나 **실물 제작·검증은 아직 없습니다.**
> 자세한 배경과 다음 단계는 [HANDOFF.md](HANDOFF.md)를 보세요.

---

## 한 줄 요약

BK7 프리즘 위에 시료를 올리고, 590 nm 단색 LED를 임계각으로 쏴서 생기는 **그림자 경계의 픽셀 위치**를 TSL1401 리니어 CCD로 읽습니다.
매 측정마다 **RO-DI(0 PSU)와 표준액(35 PSU) 두 점으로 자가보정**하므로, 싸구려 부품으로도 시판 포켓 굴절계(±2 PSU)보다 좋은 정확도가 나옵니다.

| 항목 | 값 |
|---|---|
| 목표 정밀도 | **± 0.124 PSU** (RSS) |
| 감도 | 253 µrad / PSU · 검출팔 250 mm에서 **1 px ≈ 1 PSU** |
| 경계 폭 | 약 12.7 px ≈ 10.8 PSU (회절 지배). 오차가 아니라 SNR 요구로 바뀜 — [HANDOFF.md](HANDOFF.md) §5 |
| 측정 주기 | 1일 2회, 1 사이클 약 8분 |
| 제어 | Arduino Nano + HC-06 블루투스, 스마트폰 시리얼 터미널 |
| 비교 대상 | ATAGO PAL-06S 포켓 굴절계 = ±2 PSU |

---

## 파일 안내

### 먼저 볼 것

> **⚠ pptx / pdf 는 2026-08-31 기준입니다.** 09-01 에 정정된 내용(프리즘을 BK7 →
> 아크릴 활꼴로, 두 팔 사이각 123.9° → 149.3°, 회절 항목 추가, 파장 민감도 14배 하향,
> 오차예산 온도 항목)이 **반영돼 있지 않습니다.**
> 슬라이드와 아래 마크다운 문서가 어긋나면 **마크다운 쪽이 최신**입니다.
> 정정 목록은 [HANDOFF.md](HANDOFF.md) §4 를 보십시오.

| 파일 | 내용 |
|---|---|
| **`해수수조_광학식_염도측정_설계.pptx`** | 18장짜리 설계 문서. 원리·오차·배선·명령어·부품·안전 전체 (08-31 기준) |
| `해수수조_광학식_염도측정_설계.pdf` | 위 문서의 PDF 사본 (빠른 열람용, 08-31 기준) |
| **[`HANDOFF.md`](HANDOFF.md)** | 왜 이렇게 설계했는지, 무엇이 미해결인지, 다음에 뭘 할지 |
| **[`BOM.md`](BOM.md)** | 부품 목록과 조달처. 확인된 링크 / 검색어 / 주의 3단계로 구분 |
| **[`PRISM_SOURCING.md`](PRISM_SOURCING.md)** | 프리즘 후보 비교와 선정 근거. **주문 전에 이것부터** |
| **[`ILLUMINATION.md`](ILLUMINATION.md)** | 조명계 설계. 슬릿·입사창의 역할, 두 배치와 평면도 요구. **미결정 항목 있음** |

### 도면 (`figures/`)

| 파일 | 내용 |
|---|---|
| `fig_optics.png` | 임계각 원리와 광학 배치 |
| `fig_cal.png` | 2점 자가보정 검량선 (1 px ≈ 1 PSU) |
| `fig_head.png` | 측정 헤드 조립 단면도 (알루미늄 가공 기준) |
| `fig_printed.png` | **3D 프린팅용 측정 헤드 분해도** ← 실제로 만들 때는 이쪽 |
| `fig_cell.png` | 플로우셀 설계 요점 (기포·온도 대책) |
| `fig_fluidics.png` | 유체 회로 (페리스탈틱 펌프 4개) |
| `fig_breadboard.png` | 브레드보드 배선도 (Fritzing 스타일) |
| `fig_mosfet.png` | **MOSFET 1채널 상세 회로** — 배선도의 모듈 블록 내부 |
| `fig_wiring.png` | 아두이노 핀 배치 요약 |

### 계산

| 파일 | 내용 |
|---|---|
| `design_calc.py` | 모든 설계 수치의 계산 근거. 외부 라이브러리 불필요 |
| `src/segment_optics.py` | 활꼴 광선추적 · 경계 폭 예산(회절·슬릿·팔 길이) · 렌즈 배치 비교 · 파장 분산 · AR 코팅 TMM |
| `src/illum_sim.py` | 조명 배치 B 광선추적. 조명팔·패치·경계 이동·표면 평면도 민감도 |

---

## 빠른 시작

### 설계 수치 확인

```bash
python design_calc.py
```

파일 상단 `CONFIG` 블록만 고치면 전부 다시 계산됩니다.

```python
T_C       = 26.0     # 수조 온도
LAMBDA_NM = 590.0    # LED 중심 파장
N_PRISM   = 1.5168   # 프리즘 굴절률 (BK7)
ARM_MM    = 250.0    # 검출팔 길이
```

예를 들어 하우징 공간 때문에 검출팔을 200 mm로 줄이면 분해능이 0.050 → 0.063 PSU로 바뀝니다.
**프리즘을 다른 종류로 바꿔도 됩니다** — 2점 자가보정이 실제 기울기를 실측하므로, 계산값은 "감도가 충분한가, 두 보정점이 128 px 안에 들어오는가"만 확인하는 용도입니다.

### 프리즘 형상 비교

```bash
python src/segment_optics.py
```

프리즘이 정확한 반원이 아니어도 되는지, AR 코팅이 임계각을 움직이는지,
두 광학팔 사이각을 몇 도로 잡아야 하는지가 형상별로 출력됩니다.
이어서 경계 폭이 무엇에 지배되는지(회절), 검출팔·슬릿 폭을 바꾸면 무엇이 달라지는지,
렌즈를 넣으면 어디까지 좋아지고 대신 무엇을 요구받는지가 표로 나옵니다.

### 만들기 시작할 때

1. `PRISM_SOURCING.md`대로 프리즘 주문 (사이언스트리 2세트, 21,000원)
2. `BOM.md`로 나머지 부품 주문
3. **프리즘 도착 즉시 1순위 검증** — 밀봉 불필요. 평면 위에 RO-DI/표준액 액적만
4. 두께 실측 후 `fig_printed.png` 셀 치수를 다시 잡아 헤드 출력 (PETG 검정)
5. `fig_breadboard.png` + `fig_mosfet.png`대로 배선
6. `HANDOFF.md`의 "다음 단계" 순서대로 진행

---

## 반드시 지켜야 할 네 가지

**HC-06 RXD에 1 kΩ/2 kΩ 분압기.** ZS-040 보드의 통신 핀은 3.3 V 소자입니다. 나노의 5 V TX를 직결하면 모듈이 손상됩니다.

**MOSFET 게이트에 10 kΩ 풀다운.** 없으면 전원 투입·리셋 순간에 게이트가 떠서 펌프가 제멋대로 돕니다. 수조 옆에서는 물난리로 직결됩니다.

**페리스탈틱 펌프만 사용.** 정지 시 튜브가 눌려 사이펀이 원천 차단됩니다. 다른 펌프는 정전 시 수조를 바닥으로 옮겨놓을 수 있습니다.

**표준액과 시료를 같은 온도에서 잴 것.** 자가보정이 지우는 온도 오차는 둘이 *함께* 드리프트할 때뿐입니다.
둘 **사이**에 온도차가 있으면 0.667 PSU/°C 가 그대로 살아납니다 — 0.1 PSU 를 지키려면 **0.15 °C 이내**여야 합니다.
온도 센서는 수조가 아니라 **셀 유로 안**에 넣고, 표준액과 시료 양쪽을 재서 보정하십시오.

---

## 도해 재생성 (`src/`)

`figures/`의 그림은 모두 matplotlib으로 생성한 것입니다. 수정이 필요하면:

```bash
python src/diag1_optics.py       # fig_optics.png     임계각 원리
python src/diag2_calibration.py  # fig_cal.png        2점 보정 검량선
python src/diag3_cell.py         # fig_cell.png       플로우셀
python src/diag4_fluidics.py     # fig_fluidics.png   유체 회로
python src/diag5_wiring.py       # fig_wiring.png     핀 배치
python src/head.py               # fig_head.png       측정 헤드 단면도
python src/printed.py            # fig_printed.png    3D 프린팅 분해도
python src/mosfet.py             # fig_mosfet.png     MOSFET 회로
python src/fritz.py              # fig_breadboard.png 브레드보드 배선도
```

**그림은 `figures/`에 바로 떨어져 기존 파일을 덮어씁니다.** 시험 삼아 돌려 보려면
`PSU_FIG_DIR` 로 다른 곳을 지정하십시오.

```bash
PSU_FIG_DIR=/tmp/fig python src/head.py
```

한글 폰트는 `src/kfont.py`가 플랫폼별로 알아서 찾습니다
(윈도우 맑은고딕·나눔고딕, 리눅스 Noto Sans CJK, macOS). 못 찾으면 경고를 내고 계속하므로
한글이 깨져 나오면 `PSU_FONT=/경로/폰트.ttf` 로 직접 지정하십시오.
필요한 것은 matplotlib 뿐입니다: `pip install matplotlib`

설계 문서 pptx 는 Node 로 만듭니다.

```bash
npm install     # pptxgenjs (최초 1회)
npm run build   # 해수수조_광학식_염도측정_설계.pptx 를 저장소 루트에 씀
```

`figures/`의 5장(optics · cal · cell · fluidics · wiring)을 읽어 박아 넣으므로
그림을 먼저 재생성해야 합니다. 나머지 4장(head · printed · mosfet · breadboard)은
pptx에 들어가지 않고 저장소 문서에서만 참조됩니다.

`python design_calc.py` · `python src/segment_optics.py` · `python src/illum_sim.py` 는
그림 없이 수치만 출력하며 외부 라이브러리가 필요 없습니다.
