#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
활꼴 프리즘 광선추적 · 경계 폭 예산 · AR 코팅 검증
====================================================

이 스크립트는 네 가지 질문에 답합니다.

  Q1. 프리즘이 "정확한 반원"이 아니라 "활꼴"이어도 임계각 염도 측정이 되는가?
  Q2. 반사방지(AR) 코팅이 있으면 임계각이 움직이는가?
  Q3. 그림자 경계는 실제로 얼마나 넓게 번지고, 무엇이 그것을 지배하는가?
  Q4. 검출기 앞에 렌즈를 넣으면(푸리에면 배치) 무엇이 달라지는가?

Q1·Q2 는 "문제 없다"가 답입니다.
Q3 은 **회절이 지배하며, 좁은 슬릿이 오히려 불리하다**가 답입니다.
Q4 는 "경계가 20~30배 날카로워지지만, 대신 표면 평면도가 다시 문제가 된다"가 답입니다.

자세한 배경은 ../PRISM_SOURCING.md 를 보십시오.
외부 라이브러리가 필요 없습니다.

    python segment_optics.py
"""

import math
import cmath

# ----------------------------------------------------------------------
# CONFIG — 여기만 고치면 전부 다시 계산됩니다
# ----------------------------------------------------------------------
T_C        = 26.0      # 수조 온도 [degC]
LAMBDA_NM  = 590.0     # LED 중심 파장 [nm]
LED_FWHM   = 20.0      # LED 스펙트럼 폭 [nm]
N_PRISM    = 1.491     # 프리즘 굴절률 (아크릴 PMMA). BK7 이면 1.5168
DNDL_PRISM = -4.16e-5  # 프리즘 재질의 분산 dn/dlambda [1/nm] @590nm
#   PMMA  -4.16e-5  (Kasarova Sellmeier)
#   BK7   -4.13e-5  (Schott Sellmeier)
#   0 으로 두면 프리즘 분산을 무시한 (보수적으로 과대평가된) 값이 나옵니다.
ARM_MM     = 250.0     # 측정면 중심 -> 검출기 거리 [mm]  (무렌즈 배치)
PIXEL_MM   = 0.0635    # TSL1401CL 픽셀 피치 [mm]
SLIT_MM    = 0.2       # 측정면에서의 조명 스폿 폭 [mm]
N_PIXELS   = 128       # TSL1401CL 화소 수
MAX_SPAN_PX= 110.0     # 0~35 PSU 스팬 상한. 128 px 안에 두 보정점이 들어와야 한다
S_TANK     = 34.0      # 수조 목표 염도 [PSU] — 운용점(민감도·분산 계산용)
# ---- 주광선 조준 염도 (2026-09-02 신설) ------------------------------
# 기구의 팔 각도를 정하는 것은 **주광선을 어느 염도에 맞추느냐**다.
# 예전에는 S_TANK(34)에 맞췄는데, 34 는 35 와 거의 같아서 2점 보정에 필요한
# 0~35 PSU 범위가 전부 조명 부채꼴의 아래쪽 끝에 몰렸다 —
# RO-DI(0 PSU) 쪽 여유가 0.046 deg 밖에 없었다(35 쪽은 0.561).
# 보정 범위의 **한가운데**에 맞추면 양쪽이 0.30 deg 로 균형이 잡히고,
# 팔 각도는 26.152 -> 26.411 deg, 0.26 deg 만 움직인다.
S_AIM      = 17.5      # 주광선 조준 = (0 + 35)/2 [PSU]
SUBPIXEL   = 1/20      # design_calc.py 가 가정하는 에지 검출 성능 [px]

# 검토할 프리즘 형상: (이름, 현 길이 mm, 사지타 mm)
#   사지타 = 현에서 곡면 정점까지의 높이.
#   정확한 반원이면 사지타 = 현/2.
SHAPES = [
    ("정확한 반원 60x30", 60.0, 30.0),
    ("활꼴 60x20 (사이언스트리 8종)", 60.0, 20.0),
    ("활꼴 60x25", 60.0, 25.0),
    ("정확한 반원 150x75 (DR-257)", 150.0, 75.0),
]

# 렌즈(푸리에면) 배치를 검토할 개구 폭 [mm]
APERTURES = [0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]

# ----------------------------------------------------------------------
# 해수 굴절률 — OSU/Parrish 실험식
#   n = a*T^2 + b*lam^2 + c*T + d*lam + e   (S=0 과 S=35 계수조를 선형보간)
# ----------------------------------------------------------------------
_SW = (-1.50156e-6, 1.07085e-7, -4.27594e-5, -1.60476e-4, 1.39807)  # S = 35
_FW = (-1.97812e-6, 1.03223e-7, -8.58125e-6, -1.54834e-4, 1.38919)  # S = 0


def n_water(T, S, lam=LAMBDA_NM):
    f = lambda c: c[0] * T * T + c[1] * lam * lam + c[2] * T + c[3] * lam + c[4]
    n0, n35 = f(_FW), f(_SW)
    return n0 + (n35 - n0) * S / 35.0


def theta_c(S, n_prism=N_PRISM, T=T_C):
    """프리즘 내부에서 본 임계각 [rad]. 측정면 법선 기준."""
    return math.asin(n_water(T, S) / n_prism)


def dtheta_dS(n_prism=N_PRISM, T=T_C, S=S_TANK):
    """염도 감도 [rad/PSU]. 측정면에서의 임계각 변화율."""
    dn_dS = (n_water(T, 35.0) - n_water(T, 0.0)) / 35.0
    return dn_dS / (n_prism * math.cos(theta_c(S, n_prism, T)))


def dtheta_dlambda(n_prism=N_PRISM, dn_prism=DNDL_PRISM, T=T_C, S=S_TANK):
    """파장 감도 [rad/nm].

    **프리즘 분산이 시료 분산을 대부분 상쇄합니다.**
    theta_c = asin(n_s / n_p) 이므로

        d(theta_c)/dlam = [ dn_s/dlam - sin(theta_c) * dn_p/dlam ] / (n_p cos theta_c)

    물과 유리·아크릴의 dn/dlam 이 같은 부호로 비슷한 크기라서 대괄호 안이
    거의 0 이 됩니다. 프리즘 분산을 빼먹으면 파장 민감도를 10배 이상
    과대평가하게 됩니다 (0.19 vs 0.013 PSU/nm).
    """
    h = 0.5
    dn_s = (n_water(T, S, LAMBDA_NM + h) - n_water(T, S, LAMBDA_NM - h)) / (2 * h)
    tc = theta_c(S, n_prism, T)
    return (dn_s - math.sin(tc) * dn_prism) / (n_prism * math.cos(tc))


# ----------------------------------------------------------------------
# 활꼴 기하
#   현을 x축(y=0)에 놓고 유리를 y>0 쪽에 둔다. 측정점 M = 원점.
#   현 반길이 a, 사지타 h 이면
#       R  = (a^2 + h^2) / (2h)
#       Cy = h - R          (원 중심의 y 좌표. 반원이면 0, 활꼴이면 음수)
# ----------------------------------------------------------------------
def segment_geometry(chord_mm, sagitta_mm):
    a, h = chord_mm / 2.0, sagitta_mm
    R = (a * a + h * h) / (2.0 * h)
    return R, h - R


# ----------------------------------------------------------------------
# 광선추적 — 측정점에서 출발해 곡면에서 굴절, 검출기까지
# ----------------------------------------------------------------------
def trace(x0, theta, R, cy, n=N_PRISM):
    """(x0, 0) 에서 법선(+y)으로부터 theta 만큼 기운 광선을 곡면까지 보내고 굴절시킨다.
    반환: (곡면 교점, 출사 단위벡터, 곡면 내부 입사각 deg) — 전반사면 dir=None."""
    d = (math.sin(theta), math.cos(theta))
    ox, oy = x0, -cy                      # 원 중심 기준 출발점
    b = 2.0 * (ox * d[0] + oy * d[1])
    c = ox * ox + oy * oy - R * R
    disc = b * b - 4.0 * c
    if disc < 0:
        return None, None, 90.0
    t = (-b + math.sqrt(disc)) / 2.0
    P = (x0 + t * d[0], t * d[1])
    nrm = (P[0] / R, (P[1] - cy) / R)     # 바깥쪽 법선
    ci = d[0] * nrm[0] + d[1] * nrm[1]    # cos(입사각)
    si = math.sqrt(max(0.0, 1.0 - ci * ci))
    st = n * si                            # 스넬: n*sin(i) = 1*sin(t)
    inc_deg = math.degrees(math.acos(min(1.0, max(-1.0, ci))))
    if st >= 1.0:
        return P, None, inc_deg            # 곡면에서 전반사 -> 빛이 못 나감
    ct = math.sqrt(1.0 - st * st)
    k = n * ci - ct
    r = (n * d[0] - k * nrm[0], n * d[1] - k * nrm[1])
    m = math.hypot(*r)
    return P, (r[0] / m, r[1] / m), inc_deg


def detector_pos(x0, theta, R, cy, chief, arm=ARM_MM):
    """주광선에 수직인 검출기면(측정점에서 arm mm) 위의 좌표 [mm]."""
    P, r, _ = trace(x0, theta, R, cy)
    if r is None:
        return None
    Q = (arm * chief[0], arm * chief[1])
    den = r[0] * chief[0] + r[1] * chief[1]
    s = ((Q[0] - P[0]) * chief[0] + (Q[1] - P[1]) * chief[1]) / den
    H = (P[0] + s * r[0], P[1] + s * r[1])
    perp = (-chief[1], chief[0])
    return (H[0] - Q[0]) * perp[0] + (H[1] - Q[1]) * perp[1]


# ----------------------------------------------------------------------
# 회절 — 무렌즈 배치에서 경계 폭의 지배 항
# ----------------------------------------------------------------------
def diffraction_mm(arm, slit=SLIT_MM, lam_nm=LAMBDA_NM):
    """검출기에서 본 회절 번짐 폭 [mm]. 두 영역을 모두 본다.

    프레넬 수  N_F = w^2 / (lam * L) 로 영역이 갈립니다.

      N_F >> 1 (넓은 개구)  : 나이프에지 프레넬 회절, 폭 ~ sqrt(lam*L).
                              개구 폭과 무관.
      N_F << 1 (좁은 슬릿)  : 프라운호퍼 영역. 슬릿 자체의 원거리장 폭
                              lam*L/w 로 퍼진다. **슬릿을 좁힐수록 나빠진다.**

    둘 중 큰 쪽이 실제 폭을 지배하므로 max 를 씁니다.
    두 식은 w = sqrt(lam*L) 에서 정확히 만나고, 그 지점이 무렌즈 배치의
    최적 슬릿 폭입니다 (250 mm 에서 0.384 mm).

    원설계는 sqrt(lam*L) 만 썼는데, 슬릿 0.2 mm 는 프라운호퍼 영역
    (w^2/lam = 68 mm << L = 250 mm)이라 실제로는 1.9배 더 넓습니다.
    """
    lam = lam_nm * 1e-6                      # mm
    fresnel = math.sqrt(lam * arm)           # 나이프에지
    fraunhofer = lam * arm / slit            # 슬릿 원거리장
    return max(fresnel, fraunhofer)


def spectral_mm(arm, n_prism=N_PRISM):
    """LED 대역폭에 의한 경계 번짐 [mm]. 프리즘 분산 상쇄를 반영."""
    return abs(dtheta_dlambda(n_prism)) * LED_FWHM * arm


# ----------------------------------------------------------------------
def analyze(name, chord, sagitta):
    R, cy = segment_geometry(chord, sagitta)
    t_tank = theta_c(S_TANK)
    t_aim = theta_c(S_AIM)                     # 주광선은 보정범위 중앙에 조준
    P, chief, inc = trace(0.0, t_aim, R, cy)
    print("[%s]" % name)
    print("   R = %.2f mm, 원 중심 y = %+.2f mm (%s)"
          % (R, cy, '측정면 위 = 정확한 반원' if abs(cy) < 1e-9
             else '측정면에서 %.1f mm 바깥' % -cy))
    if chief is None:
        print("   >>> 곡면에서 전반사. 이 형상은 쓸 수 없습니다.\n")
        return

    p = {S: detector_pos(0.0, theta_c(S), R, cy, chief) for S in (0.0, 10.0, 17.5, 25.0, 34.0, 35.0)}
    span = abs(p[35.0] - p[0.0])
    px = span / PIXEL_MM
    mm_per_psu = span / 35.0

    # 슬릿 폭에 의한 경계 번짐: 같은 각도, 스폿 양 끝에서 출발한 두 광선의 착지 간격
    a_ = detector_pos(-SLIT_MM / 2, t_tank, R, cy, chief)
    b_ = detector_pos(+SLIT_MM / 2, t_tank, R, cy, chief)
    blur = abs(b_ - a_)

    # 0/35 두 점을 잇는 직선과 실제 응답의 차이 = 2점 보정 직선성 오차
    lin = lambda S: p[0.0] + (p[35.0] - p[0.0]) * S / 35.0
    err = {S: (p[S] - lin(S)) / mm_per_psu for S in (10.0, 17.5, 25.0, 34.0)}

    arm_deg = math.degrees(math.atan2(chief[0], chief[1]))

    print("   곡면 내부 입사각        = %6.2f deg   (아크릴 임계각 %.2f deg 미만이어야 함)"
          % (inc, math.degrees(math.asin(1.0 / N_PRISM))))
    print("   0~35 PSU 검출기 스팬    = %7.3f mm = %6.1f px (%.3f PSU/px)"
          % (span, px, 35.0 / px))
    print("   슬릿 %s mm 기하 번짐    = %7.4f mm = %5.2f px = %5.3f PSU"
          % (SLIT_MM, blur, blur / PIXEL_MM, blur / mm_per_psu))
    print("   2점 보정 직선성 오차     = "
          + ", ".join("%.0fPSU:%+.4f" % (S, e) for S, e in sorted(err.items())) + "  [PSU]")
    print("   출사광 = 법선에서 %.2f deg  ->  두 광학팔 사이각 = %.2f deg"
          % (arm_deg, 2 * arm_deg))

    cur = edge_width_psu(R, cy, chief, ARM_MM)
    if cur:
        psu, tot, geo, dif, spec, _ = cur
        print("   경계 폭 합계            = %5.2f px = %5.2f PSU"
              "   (기하 %.2f + 회절 %.2f + 스펙트럼 %.2f px, 제곱합)"
              % (tot / PIXEL_MM, psu, geo / PIXEL_MM, dif / PIXEL_MM, spec / PIXEL_MM))
    print()


def edge_width_psu(R, cy, chief, arm, slit=SLIT_MM):
    """검출기에서 본 그림자 경계의 폭.

    세 항을 제곱합으로 합칩니다.
      기하    — 슬릿 폭 x 곡면의 렌즈 작용
      회절    — diffraction_mm() 참조. 무렌즈 배치에서는 보통 이게 지배한다
      스펙트럼 — LED 대역폭 x 파장 감도 (프리즘 분산 상쇄 반영)

    반환: (PSU 환산 폭, 총폭 mm, 기하 mm, 회절 mm, 스펙트럼 mm, 스팬 mm)

    **경계가 넓다는 것 자체는 오차가 아닙니다.** 매 사이클 2점 보정이
    같은 모양의 경계를 세 번(RO-DI·표준액·시료) 재고 그 이동량만 쓰므로,
    재현성만 있으면 모양은 상쇄됩니다. 경계 폭이 정하는 것은 에지 검출의
    잡음 민감도입니다 — required_snr() 를 보십시오.
    """
    t = theta_c(S_AIM)
    a_ = detector_pos(-slit / 2, t, R, cy, chief, arm)
    b_ = detector_pos(+slit / 2, t, R, cy, chief, arm)
    s0 = detector_pos(0.0, theta_c(0.0), R, cy, chief, arm)
    s35 = detector_pos(0.0, theta_c(35.0), R, cy, chief, arm)
    if None in (a_, b_, s0, s35):
        return None
    span = abs(s35 - s0)
    if span <= 0:
        return None
    geo = abs(b_ - a_)
    dif = diffraction_mm(arm, slit)
    spec = spectral_mm(arm)
    tot = math.sqrt(geo * geo + dif * dif + spec * spec)
    return tot / span * 35.0, tot, geo, dif, spec, span


def arm_table(R, cy, chief, slit=SLIT_MM):
    """검출팔 길이를 바꿔 가며 무엇이 좋아지고 무엇이 나빠지는지 본다.

    **팔 길이는 각도 분해능을 개선하지 못합니다.** 프라운호퍼 영역에서
    회절 폭은 lam*L/w 로 L 에 **비례**하고 스팬도 L 에 비례하므로, PSU 로
    환산한 경계 폭은 팔 길이에 무관합니다. 팔이 정하는 것은 px/PSU 배율,
    즉 픽셀 샘플링뿐입니다.

    (원설계는 회절을 sqrt(lam*L) 로 잡아 "팔을 늘리면 조금 좋아진다"고
     결론냈지만, 그 식은 0.2 mm 슬릿에 맞지 않습니다. diffraction_mm 참조.)

    실제 트레이드오프는 이렇습니다.
      팔이 짧다 -> px/PSU 가 작아 픽셀 양자화가 정밀도를 제한
      팔이 길다 -> 기하 번짐(슬릿 x 확대율)이 커지고 하우징이 커짐
    """
    print("[검출팔 길이 — 무엇이 실제로 바뀌는가]   슬릿 %.2f mm" % slit)
    print("   %8s %9s %9s %10s %10s %11s"
          % ("팔[mm]", "스팬[px]", "px/PSU", "경계[px]", "경계[PSU]", "분해능[PSU]"))
    for arm in (60, 90, 150, 250, 400, 600, 730):
        r = edge_width_psu(R, cy, chief, arm, slit)
        if not r:
            continue
        psu, tot, geo, dif, spec, span = r
        pxpsu = span / PIXEL_MM / 35.0
        flag = '  <- 배열 밖' if span / PIXEL_MM > MAX_SPAN_PX else ''
        print("   %8d %9.1f %9.3f %10.2f %10.2f %11.3f%s"
              % (arm, span / PIXEL_MM, pxpsu, tot / PIXEL_MM, psu,
                 SUBPIXEL / pxpsu, flag))
    print("   -> 경계[PSU] 열이 팔 길이에 거의 무관한 것에 주목하십시오.")
    print("      팔을 늘려 얻는 것은 분해능[PSU] 열, 즉 픽셀 샘플링뿐입니다.")
    print()


def slit_scan(R, cy, chief, arm=ARM_MM):
    """슬릿 폭을 바꿔 가며 경계 폭을 본다. 무렌즈 배치의 최적 슬릿을 찾는다."""
    print("[무렌즈 배치 — 슬릿 폭 최적화]   팔 %.0f mm" % arm)
    print("   좁힐수록 좋아지지 않습니다. sqrt(lam*L) = %.3f mm 부근이 최적입니다."
          % math.sqrt(LAMBDA_NM * 1e-6 * arm))
    print("   %8s %9s %9s %11s %10s %9s"
          % ("슬릿[mm]", "기하[px]", "회절[px]", "스펙트럼[px]", "합계[px]", "PSU"))
    best = None
    for w in (0.05, 0.1, 0.2, 0.3, 0.384, 0.5, 0.8, 1.5, 3.0):
        r = edge_width_psu(R, cy, chief, arm, w)
        if not r:
            continue
        psu, tot, geo, dif, spec, _ = r
        if best is None or psu < best[1]:
            best = (w, psu)
        print("   %8.3f %9.2f %9.2f %11.2f %10.2f %9.2f"
              % (w, geo / PIXEL_MM, dif / PIXEL_MM, spec / PIXEL_MM,
                 tot / PIXEL_MM, psu))
    here = edge_width_psu(R, cy, chief, arm, SLIT_MM)[0]
    print("   -> 최적 슬릿 %.3f mm 에서 %.2f PSU.  현 설계 %.2f mm 는 %.2f PSU "
          "(%.0f%% 손해)" % (best[0], best[1], SLIT_MM, here,
                            (here / best[1] - 1) * 100))
    print("      바닥이 완만하므로 슬릿 폭은 큰 결정이 아닙니다. 다만 0.1 mm 이하로")
    print("      좁히면 급격히 나빠집니다 — 좁은 슬릿은 회절로 되갚습니다.")
    print()
    return best


# ----------------------------------------------------------------------
# 렌즈(푸리에면) 배치
# ----------------------------------------------------------------------
def lens_mode(n_prism=N_PRISM):
    """검출기를 볼록렌즈의 뒤초점면에 놓는 배치.

    상용 임계각 굴절계가 쓰는 구조입니다. 초점면에서는 위치가 곧 각도이므로
    (x = f * theta) **조명 스폿 크기와 각도 분해능이 분리됩니다.**
    측정면을 넓게 비춰도 경계가 흐려지지 않습니다.

    핵심 결과: 초점면에서의 PSU 환산 경계 폭은 **초점거리와 무관**합니다.
    f 는 px/PSU 배율만 정합니다. 경계 폭을 정하는 것은 개구 폭뿐입니다.

        경계 폭[rad] = hypot( lam/w,  2*표면기울기오차,  파장항 )
        경계 폭[PSU] = 위 / (dtheta/dS)
    """
    sens = dtheta_dS(n_prism)                      # rad/PSU
    lam = LAMBDA_NM * 1e-6                          # mm
    spec = abs(dtheta_dlambda(n_prism)) * LED_FWHM  # rad
    f_for_1px = PIXEL_MM / sens                     # 1 px/PSU 가 되는 초점거리

    print("=" * 70)
    print("렌즈(푸리에면) 배치 — 검출기를 초점면에 놓으면")
    print("=" * 70)
    print("   감도 %.1f urad/PSU,  1 px/PSU 가 되는 초점거리 f = %.0f mm"
          % (sens * 1e6, f_for_1px))
    print("   스펙트럼 항 %.1f urad = %.3f PSU (개구와 무관, 렌즈로도 안 줄어듦)"
          % (spec * 1e6, spec / sens))
    print()
    print("   %8s %12s %10s %14s %14s"
          % ("개구[mm]", "회절[urad]", "경계[PSU]", "허용 기울기오차", "= PV 사각"))
    print("   %8s %12s %10s %14s %14s"
          % ("", "lam/w", "", "[urad]", "[nm over w]"))
    for w in APERTURES:
        dif = lam / w                                     # rad
        tot = math.hypot(dif, spec)
        psu = tot / sens
        # 회절과 같은 크기가 되는 표면 기울기 오차 (2*sigma = dif)
        slope = dif / 2.0
        sag_nm = slope * w / 8.0 * 1e6                    # 포물면 근사 PV [nm]
        print("   %8.2f %12.0f %10.3f %14.0f %14.1f"
              % (w, dif * 1e6, psu, slope * 1e6, sag_nm))
    print()
    print("   읽는 법 — 개구를 넓히면 회절은 1/w 로 줄지만, 그만큼 표면 평면도가")
    print("   빡빡해집니다. 오른쪽 두 열은 '회절과 표면오차가 같아지는 지점'이고,")
    print("   그보다 표면이 나쁘면 개구를 더 넓혀도 이득이 없습니다.")
    print()
    print("   PV 사각 열이 개구와 무관하게 %.0f nm = lambda/16 인 것은 우연이 아닙니다."
          % (LAMBDA_NM / 16.0))
    print("   회절 한계(lam/w)와 표면 한계(사각/w)가 같은 1/w 스케일을 따르기 때문입니다.")
    print("   즉 렌즈 배치의 요구는 개구 크기와 무관하게 **lambda/16 PV 평면도** 하나로")
    print("   요약됩니다. 사출 아크릴이 이걸 만족하는지는 **측정해 봐야 압니다.**")
    print()
    print("   무렌즈 배치와 비교 — 각도 분해능은 두 배치 모두 lam/w 입니다.")
    print("   차이는 w 를 키울 수 있느냐뿐입니다. 무렌즈에서는 슬릿을 넓히면")
    print("   기하 번짐이 그대로 커져 0.3 mm 가 한계지만, 초점면에서는 스폿 크기가")
    print("   각도 분해능과 분리되므로 개구를 자유롭게 넓힐 수 있습니다.")
    print()


def required_snr(width_px, target_px=SUBPIXEL):
    """폭 width_px 인 경계를 target_px 까지 찾아내려면 필요한 SNR.

    센트로이드 정밀도의 어림식  sigma ~ W / (SNR * sqrt(N))  을 씁니다.
    (N = 평균한 프레임 수)
    """
    print("[에지 검출 — 넓은 경계가 실제로 무엇을 요구하는가]")
    print("   경계 폭 W = %.1f px, 목표 정밀도 %.3f px (design_calc.py 가정)"
          % (width_px, target_px))
    print("   센트로이드 어림식  sigma ~ W / (SNR * sqrt(N))")
    print("   -> 필요한 SNR * sqrt(N) = %.0f" % (width_px / target_px))
    print()
    print("   %8s %10s %10s %10s" % ("SNR", "N=1", "N=16", "N=64"))
    for snr in (30, 60, 100, 200, 400):
        vals = [width_px / (snr * math.sqrt(n)) for n in (1, 16, 64)]
        flag = '  <= 충족' if vals[1] <= target_px else ''
        print("   %8d %10.3f %10.3f %10.3f px%s" % (snr, vals[0], vals[1], vals[2], flag))
    print()
    print("   즉 경계가 넓다는 것은 설계를 깨는 결함이 아니라 **SNR 요구로**")
    print("   바뀝니다. SNR 100 + 16프레임 평균이면 목표를 넘습니다 — 10비트 ADC 와")
    print("   제대로 된 차광이면 어렵지 않은 수준입니다.")
    print("   진짜 위험은 폭 자체가 아니라 경계 모양의 **재현성**입니다 —")
    print("   미광·정렬 드리프트·프레넬 링잉이 모양을 바꾸면 2점 보정이 못 지웁니다.")
    print("   1순위 검증에서 경계 프로파일을 프레임 단위로 저장해 확인하십시오.")
    print()


# ----------------------------------------------------------------------
# AR 코팅 검증 — 전달행렬법(TMM)
#   결론: 접선 방향 파수 n*sin(theta) 가 모든 층에서 보존되므로
#         임계각은 첫 매질과 마지막 매질만으로 결정된다. 중간층은 무관.
# ----------------------------------------------------------------------
def reflectance_s(theta_i, n_list, d_list_nm, lam_nm=LAMBDA_NM):
    """s편광 반사율. n_list = [입사매질, 층..., 출사매질], d_list_nm = 층 두께."""
    n0 = n_list[0]
    kx = n0 * math.sin(theta_i)                      # 보존되는 접선 파수 (n*sin)
    def kz(n):
        return cmath.sqrt(complex(n * n - kx * kx))
    M = [[1, 0], [0, 1]]
    for n, d in zip(n_list[1:-1], d_list_nm):
        kzj = kz(n)
        delta = 2 * cmath.pi * d * kzj / lam_nm
        c_, s_ = cmath.cos(delta), cmath.sin(delta)
        Mj = [[c_, -1j * s_ / kzj], [-1j * kzj * s_, c_]]
        M = [[M[0][0] * Mj[0][0] + M[0][1] * Mj[1][0], M[0][0] * Mj[0][1] + M[0][1] * Mj[1][1]],
             [M[1][0] * Mj[0][0] + M[1][1] * Mj[1][0], M[1][0] * Mj[0][1] + M[1][1] * Mj[1][1]]]
    k0, ks = kz(n_list[0]), kz(n_list[-1])
    num = (M[0][0] + M[0][1] * ks) * k0 - (M[1][0] + M[1][1] * ks)
    den = (M[0][0] + M[0][1] * ks) * k0 + (M[1][0] + M[1][1] * ks)
    return abs(num / den) ** 2


def find_critical(n_list, d_list_nm, lo=40.0, hi=89.9):
    """반사율이 1에 도달하는 각도 = 임계각. 이분법으로 찾는다."""
    for _ in range(60):
        mid = (lo + hi) / 2
        if reflectance_s(math.radians(mid), n_list, d_list_nm) > 0.9999:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def ar_check():
    n_glass, n_sample = 1.5168, n_water(T_C, 35.0)   # BK7 기준으로 검증
    cases = [
        ("맨유리 (코팅 없음)", [n_glass, n_sample], []),
        ("AR 단층 107 nm (n=1.38)", [n_glass, 1.38, n_sample], [107.0]),
        ("AR 단층 200 nm (n=1.38)", [n_glass, 1.38, n_sample], [200.0]),
        ("저굴절 코팅 (n=1.30, 150 nm)", [n_glass, 1.30, n_sample], [150.0]),
    ]
    print("=" * 70)
    print("AR 코팅 검증 — 전달행렬법 (유리 n=%s, 시료 n=%.6f, S=35 PSU)"
          % (n_glass, n_sample))
    print("=" * 70)
    for name, nl, dl in cases:
        print("   %-32s -> 임계각 %8.4f deg" % (name, find_critical(nl, dl)))
    print()
    print("   중간층 종류·두께와 무관하게 임계각이 동일합니다.")
    print("   접선 방향 파수 n*sin(theta) 가 모든 층을 통해 보존되므로")
    print("   임계각은 첫 매질과 마지막 매질만으로 결정됩니다.")
    print()
    for th in (61.0,):
        r_bare = reflectance_s(math.radians(th), [n_glass, n_sample], [])
        r_ar = reflectance_s(math.radians(th), [n_glass, 1.38, n_sample], [107.0])
        print("   임계각 아래(%s deg) 반사율: 맨유리 %.3f -> AR %.3f" % (th, r_bare, r_ar))
        print("   AR 코팅은 임계각 아래 반사율을 낮춰 경계 대비를 오히려 개선합니다.")
    print()


def dispersion_check():
    """파장 민감도 — 프리즘 분산을 넣고 뺀 값을 나란히 본다."""
    dn_dS = (n_water(T_C, 35.0) - n_water(T_C, 0.0)) / 35.0
    sens = dtheta_dS()
    print("=" * 70)
    print("파장 민감도 — 프리즘 분산이 시료 분산을 상쇄합니다")
    print("=" * 70)
    h = 0.5
    dn_s = (n_water(T_C, S_TANK, LAMBDA_NM + h) - n_water(T_C, S_TANK, LAMBDA_NM - h)) / (2 * h)
    print("   dn_water/dlam = %.3e /nm,   dn_prism/dlam = %.3e /nm" % (dn_s, DNDL_PRISM))
    print()
    print("   %-28s %14s %14s" % ("", "PSU/nm", "20 nm LED"))
    for label, dnp in (("프리즘 분산 무시 (원설계)", 0.0),
                       ("프리즘 분산 포함 (실제)", DNDL_PRISM)):
        pn = abs(dtheta_dlambda(N_PRISM, dnp)) / sens
        print("   %-28s %14.4f %12.2f PSU" % (label, pn, pn * LED_FWHM))
    pn0 = abs(dtheta_dlambda(N_PRISM, 0.0)) / sens
    pn1 = abs(dtheta_dlambda(N_PRISM, DNDL_PRISM)) / sens
    print()
    print("   백색 LED(150 nm) 환산: 무시 %.1f PSU -> 포함 %.1f PSU" % (pn0 * 150, pn1 * 150))
    print("   결론은 안 바뀝니다 — 34 +- 2 PSU 창에 %.1f PSU 번짐은 여전히 못 씁니다." % (pn1 * 150))
    print("   달라지는 것은 **LED 반치폭 요구**입니다. 40 nm 라도 %.2f PSU 라서"
          % (pn1 * 40))
    print("   '반치폭 20 nm 이하 확인'은 더 이상 발주 조건이 아닙니다.")
    print()


# ----------------------------------------------------------------------
def main():
    print()
    print("=" * 70)
    print("활꼴 프리즘 광선추적   n_prism=%s  T=%sdegC  lambda=%snm"
          % (N_PRISM, T_C, LAMBDA_NM))
    print("검출팔 %s mm, 픽셀 %s mm, 슬릿 %s mm, 동작점 %s PSU"
          % (ARM_MM, PIXEL_MM, SLIT_MM, S_TANK))
    print("=" * 70)
    print()
    for name, chord, sag in SHAPES:
        analyze(name, chord, sag)

    print("요점")
    print("  - 활꼴이어도 스팬이 오히려 넓어져 분해능이 좋아집니다.")
    print("  - 확대율이 얼마인지 알 필요가 없습니다. 매 사이클 2점 보정이 실측합니다.")
    print("  - 동작점 34 PSU 는 보정점 35 에 붙어 있어 직선성 오차가 거의 0 입니다.")
    print("  - 바뀌는 것은 두 광학팔 사이각뿐입니다. 도면을 다시 그리십시오.")
    print()

    R, cy = segment_geometry(60.0, 20.0)          # 사이언스트리 8종 기준
    _, chief, _ = trace(0.0, theta_c(S_AIM), R, cy)
    arm_table(R, cy, chief)
    slit_scan(R, cy, chief)
    cur = edge_width_psu(R, cy, chief, ARM_MM)
    required_snr(cur[1] / PIXEL_MM)
    lens_mode()
    dispersion_check()
    ar_check()


if __name__ == "__main__":
    main()
