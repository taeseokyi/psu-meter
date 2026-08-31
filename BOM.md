# 해수 수조 광학식 염도계 — 부품 목록 (BOM)

배선도: `figures/fig_breadboard.png`
설계 계산: `design_calc.py`
설계 문서: `해수수조_광학식_염도측정_설계.pptx`

---

## 조달 상태 표기

| 표기 | 의미 |
|---|---|
| **확인됨** | 실제 판매 페이지를 확인한 항목. 링크 있음 |
| **검색어** | 디바이스마트가 자동 접근을 차단해 페이지를 열지 못함. 검색어로 직접 확인 필요 |
| **주의** | 조달이 까다로워 대안을 함께 적음 |

> 가격과 재고는 확인하지 못했습니다. 링크가 있는 항목도 주문 전에 현재 가격·재고를 직접 확인해 주세요.

---

## 1. 광학부 — 가장 조달이 까다로운 부분

### 1-1. 리니어 CCD 센서 — **확인됨**

| 항목 | 내용 |
|---|---|
| 부품 | TSL1401CL 128×1 리니어 CCD 모듈 (렌즈 포함형) |
| 수량 | 1 |
| 조달 | 알리익스프레스 |

- [TSL1401CL 128x1 Linear CCD Sensor with Hold, 광각 렌즈 포함](https://www.aliexpress.com/item/32763299880.html) — 검색 시점 표기가가 약 US$58 (13% 할인가). 판매자별 편차가 크므로 비교 구매 권장
- [TSL1401CL 128*1 Linear CCD Camera Module DIY Kit](https://www.aliexpress.com/i/4001057790766.html)
- [TSL1401CL 128X1 Linear CCD, 120도 광각 렌즈 모듈](https://www.aliexpress.us/item/3256805466654518.html)
- 국내 대안: [Tindie — TSL1401CL Linear Sensor Array (JasonKits)](https://www.tindie.com/products/jasonkits/tsl1401cl-linear-sensor-array/)
- 칩 단품이 필요하면: [ams-osram TSL1401CL 제품 페이지](https://ams-osram.com/products/photodetectors/photodiodes/ams-tsl1401cl-linear-array-sensor) · [데이터시트 (Mouser)](https://www.mouser.com/datasheet/2/588/TSL1401CL-1214741.pdf)

**주의** — 모듈에 딸려오는 120° 광각 렌즈는 라인트레이싱용입니다. 이 프로젝트에서는 **렌즈를 떼고 베어 센서면을 그대로** 씁니다. 임계각 방식은 각도 분포를 그대로 받아야 하므로 렌즈가 있으면 안 됩니다. 렌즈 마운트가 나사식인지 접착인지 상품 사진으로 미리 확인하세요.

### 1-2. 반원통 렌즈 (프리즘) — **주의**

| 항목 | 내용 |
|---|---|
| 부품 | BK7 반원통(hemi-cylindrical) 렌즈, 반경 10~25 mm |
| 수량 | 1 |

이 부품이 조달 난이도가 가장 높습니다. 알리익스프레스에는 규격품이 거의 없고, 아래처럼 B2B 또는 광학 전문점 경로가 됩니다.

- [Alibaba — Optical BK7 Half Cylinder Prism (B2B, MOQ 확인 필요)](https://www.alibaba.com/showroom/optical-bk7-half-cylinder-prism.html)
- [Alibaba — Optical Glass BK7 Quartz Half Cylindrical Prism Lens](https://www.alibaba.com/product-detail/Optical-Glass-Bk7-Quartz-Half-Cylindrical_1601020893505.html)
- [VY Optoelectronics — Half Round Cylindrical Lens BK7](https://www.vyoptics.com/optical-glass-half-round-cylindrical-lens-fused-silica-bk7-cylindrical-lens.html)
- [DM Photonics — Hemicylindrical prism BK7](http://www.dmphotonics.com/Hemicylindrical%20prism%20made%20of%20BK7/hemicylindrical%20prism%20made%20of%20BK7.htm)
- [Edmund Optics — N-BK7 Half-Ball Lenses](https://www.edmundoptics.com/f/n-bk7-half-ball-lenses/12559/) (반구형. 원통형 대신 쓸 수 있으나 집광 평면이 하나 더 생김)

#### 중요 — 프리즘은 생각보다 자유롭게 대체할 수 있습니다

이 설계는 **매 측정 사이클마다 RO-DI와 표준액 두 점으로 자가보정**을 합니다. 검량선의 기울기와 절편을 그때그때 실측하므로, **프리즘의 정확한 굴절률이나 형상, 검출팔 길이를 미리 알 필요가 없습니다.** 설계 계산값은 "이 조합으로 감도가 충분한가, 두 보정점이 128픽셀 안에 들어오는가"를 확인하는 용도일 뿐입니다.

따라서 현실적인 대안:

| 대안 | 장점 | 확인할 것 |
|---|---|---|
| **직각 프리즘 (BK7/K9)** | 알리에 매우 흔하고 저렴 | 입사면 굴절이 추가됨. 실측 보정으로 흡수되지만 광로 배치를 다시 그려야 함 |
| **정삼각 분광 프리즘** | 가장 저렴하고 흔함 | 위와 동일 |
| **반구(half-ball) 렌즈** | 규격품 존재 | 한 방향으로만 집광, 슬릿 방향 주의 |
| 유리 블록 + 광학 접착 | 자작 가능 | 접착면 기포가 치명적 |

**권장 진행 순서**: 값싼 직각 프리즘이나 정삼각 프리즘을 먼저 사서 광학 벤치를 세우고, 경계선이 실제로 보이고 RO-DI ↔ 표준액 사이가 30픽셀 이상 벌어지는 것을 확인한 뒤에, 필요하면 반원통 렌즈로 업그레이드하십시오. `design_calc.py`의 `N_PRISM`, `ARM_MM`을 바꿔 미리 시뮬레이션할 수 있습니다.

### 1-3. 광원 — **검색어**

| 항목 | 사양 | 수량 |
|---|---|---|
| 측정 LED | 590 nm 앰버, 스펙트럼 폭 20 nm 이하, 5 mm 또는 SMD | 1 |
| UVC LED | 265~275 nm, 수 mW | 1 |

- 디바이스마트 검색: `앰버 LED`, `590nm LED`, `황색 LED 5mm`
- 알리익스프레스 검색: [`590nm led`](https://www.aliexpress.com/w/wholesale-590nm-led.html), `amber LED 5mm 590nm`, `UVC LED 265nm 3535`
- 데이터시트로 중심 파장과 반치폭(FWHM)을 반드시 확인하세요. **백색 LED는 절대 사용 불가**입니다(경계 번짐 28 PSU).

**UVC 주의** — 265 nm는 눈과 피부에 유해합니다. 완전 차광 하우징 안에서만 쓰고, 하우징이 열리면 꺼지는 인터록을 넣으십시오.

---

## 2. 유체부

### 2-1. 페리스탈틱(연동) 펌프 — **확인됨**

| 항목 | 내용 |
|---|---|
| 부품 | 연동펌프 (peristaltic pump) |
| 수량 | **4** (표준액 / RO-DI / 수조물 / 배수) |

디바이스마트에서 확인된 상품입니다.

- [BLDC모터 연동워터펌프 BWP-2752P DC3V~24V, 속도조절 가능, 의료용·분석기용](https://www.devicemart.co.kr/goods/view?no=12759593) — 이 프로젝트에 가장 적합해 보입니다. 12 V 구동 가능, 분석기용 등급
- [Peristaltic Liquid Pump with Silicone Tubing 5V~6V DC (Adafruit ada-3910)](https://www.devicemart.co.kr/goods/view?no=15531016) — 5~6 V 저전압형. 12 V 대신 5 V 계통으로 갈 경우 후보
- 알리 검색어: `peristaltic pump 12V dosing`, `연동펌프 12V`

**주의** — 4개가 필요해서 이 항목이 예산에서 가장 큰 비중을 차지할 가능성이 높습니다. 예산이 부담되면 **3방/4방 솔레노이드 밸브 + 펌프 1개** 구성으로 줄일 수 있지만, 페리스탈틱의 최대 장점인 "정지 시 사이펀 원천 차단"을 잃게 되므로 수조 침수 위험 대책을 따로 세워야 합니다.

### 2-2. 셀 · 배관 — **검색어**

| 부품 | 사양 | 수량 | 검색어 |
|---|---|---|---|
| 실리콘 튜브 | 내경 2~3 mm (펌프 규격에 맞춤) | 수 m | `실리콘 튜브 2mm`, `연동펌프 튜브` |
| PTFE 튜브 | 내경 2~3 mm, UVC 근처 구간용 | 1 m | `PTFE 튜브 2mm`, `테프론 튜브` |
| Viton O-링 | 프리즘 실링용, 규격은 셀 설계에 맞춤 | 수 개 | `바이톤 오링`, `viton o-ring` |
| 튜브 피팅 | 배럴(barb) 피팅, T자 커넥터 | 약간 | `배럴 피팅`, `루어락 커넥터` |
| 셀 본체 | PTFE 또는 PVDF 블록 (가공) | 1 | `테프론 블록`, `PVDF 봉` |

**주의** — UVC LED 근처에는 실리콘·PMMA·일반 접착제를 쓰지 마십시오. 자외선에 열화됩니다. PTFE나 유리를 쓰고, 프리즘 접착에 UV 경화 접착제는 피하십시오.

---

## 3. 전자부 — **검색어** (디바이스마트에 모두 있는 흔한 부품)

디바이스마트 상품 페이지가 자동 접근을 차단해 개별 링크를 확인하지 못했습니다. 아래 검색어로 직접 확인해 주세요.

| 부품 | 사양 | 수량 | 디바이스마트 검색어 |
|---|---|---|---|
| Arduino Nano | ATmega328P, 5 V, USB | 1 | `아두이노 나노`, `Arduino Nano 호환` |
| HC-06 | 블루투스 슬레이브, ZS-040 보드 | 1 | `HC-06`, `블루투스 모듈 HC06` |
| DS18B20 | 방수 케이블형 온도센서 | 1 | `DS18B20 방수` |
| DS3231 | I2C RTC 모듈 (배터리 포함) | 1 | `DS3231 RTC 모듈` |
| MOSFET 모듈 | 4채널 로직레벨 (또는 IRLZ44N 단품 ×6) | 1 | `모스펫 모듈 4채널`, `IRLZ44N` |
| 다이오드 | 1N4007 (플라이백용) | 4 이상 | `1N4007` |
| 저항 | 1 kΩ, 2 kΩ, 4.7 kΩ, 220 Ω (1/4 W) | 각 수 개 | `저항 키트 1/4W` |
| 브레드보드 | 830 타이포인트 | 1 | `브레드보드 830` |
| 점퍼 와이어 | M-M, M-F | 각 1세트 | `점퍼케이블 세트` |
| 12 V SMPS | 2 A 이상 (펌프 4개 동시 구동 여유) | 1 | `SMPS 12V 2A`, `12V 아답터 2A` |
| DC 잭 / 터미널 | 나사 단자대 | 약간 | `DC잭 터미널`, `터미널블록 2P` |

**전원 참고** — 펌프는 한 번에 하나씩만 돌리므로 12 V 2 A면 충분하지만, 여유를 두려면 3 A를 권합니다. 로직 5 V는 나노의 USB 또는 별도 5 V 레귤레이터에서 받고, **12 V와 5 V의 GND는 반드시 한 점에서 공통**으로 묶으십시오.

---

## 4. 소모품

| 부품 | 용도 | 검색어 |
|---|---|---|
| 35.0 PSU 표준 해수 | 보관액 겸 보정액. 월 250 mL 내외 | `염도 표준액`, `refractometer calibration fluid 35ppt`, 리프 용품점 |
| RO-DI 정제수 | 헹굼 겸 0 PSU 보정점 | 리프 용품점, `RO/DI water` |
| 구연산 | 월 1회 탄산칼슘 스케일 제거 | `구연산 무수` |

**표준액이 전체 정확도를 결정합니다.** 오차 예산에서 표준액 정확도(0.1 PSU)가 가장 큰 항목이므로, 밀폐 보관하고 개봉 후 사용 기한을 지키는 것이 더 좋은 부품을 사는 것보다 정밀도에 크게 기여합니다.

---

## 5. 조립 순서 권장

1. **전자부만 먼저** — 브레드보드에 나노 + HC-06을 올려 블루투스 명령이 오가는지 확인 (분압기 잊지 마세요)
2. **TSL1401 단독 테스트** — 프레임을 읽어 128픽셀 값이 나오는지, 손으로 그림자를 만들면 반응하는지
3. **광학 벤치 가조립** — 값싼 프리즘으로 경계선이 보이는지, RO-DI와 표준액 한 방울씩으로 픽셀이 움직이는지
4. **플로우셀 결합** — 누수·기포 확인
5. **펌프 + MOSFET** — 채널 하나씩 검증. **플라이백 다이오드를 먼저 다십시오**
6. **시퀀스 자동화**

3단계에서 픽셀 이동이 확인되면 이 프로젝트의 가장 큰 기술적 위험은 넘긴 것입니다.

---

## 근거

- TSL1401CL 모듈 판매 페이지 — [AliExpress 32763299880](https://www.aliexpress.com/item/32763299880.html) 외 다수, [ams-osram 제품 페이지](https://ams-osram.com/products/photodetectors/photodiodes/ams-tsl1401cl-linear-array-sensor)
- 연동펌프 — [디바이스마트 BWP-2752P](https://www.devicemart.co.kr/goods/view?no=12759593), [디바이스마트 ada-3910](https://www.devicemart.co.kr/goods/view?no=15531016)
- BK7 반원통 프리즘 — [Alibaba 쇼룸](https://www.alibaba.com/showroom/optical-bk7-half-cylinder-prism.html), [DM Photonics](http://www.dmphotonics.com/Hemicylindrical%20prism%20made%20of%20BK7/hemicylindrical%20prism%20made%20of%20BK7.htm), [Edmund Optics N-BK7 Half-Ball](https://www.edmundoptics.com/f/n-bk7-half-ball-lenses/12559/)
- 590nm LED — [AliExpress 검색](https://www.aliexpress.com/w/wholesale-590nm-led.html)
- 설계 수치의 근거는 `design_calc.py` 및 설계 문서의 참고자료 슬라이드 참조
