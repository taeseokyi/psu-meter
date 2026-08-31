#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
해수 수조 광학식 염도 측정 시스템 — 설계 수치 계산

임계각(critical angle) 굴절계 방식의 감도, 기하, 오차 예산을 계산합니다.
아래 CONFIG 값만 바꾸면 모든 수치가 다시 계산됩니다.

굴절률 경험식 출처:
  Index of Refraction of Seawater and Freshwater as a Function of
  Wavelength and Temperature — Oregon State University, Parrish Research Group
  n = a*T^2 + b*L^2 + c*T + d*L + e      (T: 0~30 degC, L: 400~700 nm)
  염도 의존성은 S=0 과 S=35 사이에서 선형 보간.
"""

import math

# ─────────────────────────────────────────────────────────────
# CONFIG — 여기만 바꾸면 됩니다
# ─────────────────────────────────────────────────────────────
T_C        = 26.0      # 수조 온도 [degC]
LAMBDA_NM  = 590.0     # LED 중심 파장 [nm]
LED_FWHM   = 20.0      # LED 스펙트럼 폭 [nm]
N_PRISM    = 1.5168    # 프리즘 굴절률 (BK7)
ARM_MM     = 250.0     # 측정면 중심 → 검출기 거리 [mm]
PIXEL_MM   = 0.0635    # TSL1401CL 픽셀 피치 [mm]
N_PIXELS   = 128       # 어레이 픽셀 수
S_TANK     = 34.0      # 목표 수조 염도 [PSU]
S_STD      = 35.0      # 표준액 염도 [PSU]
CELL_ML    = 2.0       # 셀 용적 [mL]
SUBPIXEL   = 1/20      # 서브픽셀 에지 검출 성능 [px]
ARM_MAT_PPM= 23e-6     # 기구 재질 열팽창계수 [1/degC]  (알루미늄)

_SW = (-1.50156e-6, 1.07085e-7, -4.27594e-5, -1.60476e-4, 1.39807)  # S = 35
_FW = (-1.97812e-6, 1.03223e-7, -8.58125e-6, -1.54834e-4, 1.38919)  # S = 0


def n_water(T, S, lam=LAMBDA_NM):
    """온도 T[degC], 염도 S[PSU], 파장 lam[nm]에서의 굴절률."""
    f = lambda c: c[0]*T*T + c[1]*lam*lam + c[2]*T + c[3]*lam + c[4]
    n0, n35 = f(_FW), f(_SW)
    return n0 + (n35 - n0) * S / 35.0


def critical_angle(n_sample, n_prism=N_PRISM):
    """프리즘·시료 경계의 임계각 [rad]."""
    return math.asin(n_sample / n_prism)


def d(f, x, h=1e-4):
    """중앙차분 수치미분."""
    return (f(x + h) - f(x - h)) / (2 * h)


def main():
    line = lambda c='─', n=66: print(c * n)

    n_tank = n_water(T_C, S_TANK)
    n_std  = n_water(T_C, S_STD)
    n_rodi = n_water(T_C, 0.0)

    dn_dS   = (n_water(T_C, 35.0) - n_rodi) / 35.0
    dn_dlam = d(lambda L: n_water(T_C, S_TANK, L), LAMBDA_NM, h=0.5)
    dn_dT   = d(lambda t: n_water(t, S_TANK), T_C, h=1e-3)
    dn_dT_s = d(lambda t: n_water(t, S_STD),  T_C, h=1e-3)

    tc_tank = critical_angle(n_tank)
    tc_rodi = critical_angle(n_rodi)
    tc_air  = critical_angle(1.0)
    dth_dn  = 1.0 / (N_PRISM * math.cos(tc_tank))

    rad_per_psu = dn_dS * dth_dn
    um_per_psu  = rad_per_psu * ARM_MM * 1000.0
    px_per_psu  = rad_per_psu * ARM_MM / PIXEL_MM
    rodi_off_px = (tc_tank - tc_rodi) * ARM_MM / PIXEL_MM

    line('═')
    print(f"  광학식 염도계 설계 수치   (T={T_C}degC, lambda={LAMBDA_NM}nm, "
          f"prism n={N_PRISM}, arm={ARM_MM}mm)")
    line('═')

    print("\n[ 굴절률 ]")
    print(f"  RO-DI (0 PSU)     n = {n_rodi:.6f}")
    print(f"  수조  ({S_TANK} PSU)  n = {n_tank:.6f}")
    print(f"  표준액({S_STD} PSU)  n = {n_std:.6f}")
    print(f"  dn/dS   = {dn_dS:.4e} /PSU")
    print(f"  dn/dT   = {dn_dT:.4e} /degC")
    print(f"  dn/dlam = {dn_dlam:.4e} /nm")

    print("\n[ 임계각 기하 ]")
    print(f"  공기        theta_c = {math.degrees(tc_air):7.3f} deg  (전 영역 전반사 → 풀스케일 기준)")
    print(f"  RO-DI       theta_c = {math.degrees(tc_rodi):7.3f} deg")
    print(f"  수조 {S_TANK} PSU theta_c = {math.degrees(tc_tank):7.3f} deg")
    print(f"  두 광학팔 사이각      = {2*math.degrees(tc_tank):7.3f} deg  (= 2 x theta_c)")
    print(f"  각 팔의 수평 기준 각도 = {90 - math.degrees(tc_tank):7.3f} deg  (수평면에서 아래로)")
    print(f"  dtheta/dn = {dth_dn:.4f} rad/RIU")

    print("\n[ 감도 ]")
    print(f"  {rad_per_psu*1e6:8.1f} urad / PSU")
    print(f"  {um_per_psu:8.1f} um  / PSU   (검출팔 {ARM_MM:.0f} mm)")
    print(f"  {px_per_psu:8.3f} px  / PSU")
    print(f"  RO-DI 경계는 {S_TANK} PSU 지점에서 {rodi_off_px:.1f} px 떨어짐 "
          f"({'배열 안' if rodi_off_px < N_PIXELS*0.8 else '★배열 밖★'})")
    print(f"  분해능 (서브픽셀 {SUBPIXEL:.3f} px) = {SUBPIXEL/px_per_psu:.3f} PSU")

    print("\n[ 검출팔 길이별 비교 ]")
    print(f"  {'arm[mm]':>8} {'um/PSU':>9} {'px/PSU':>9} {'RO-DI[px]':>11} {'분해능[PSU]':>12}")
    for arm in (100, 150, 200, 250, 300, 400):
        pp = rad_per_psu * arm / PIXEL_MM
        ro = (tc_tank - tc_rodi) * arm / PIXEL_MM
        flag = '' if ro < N_PIXELS * 0.8 else '  ← 배열 밖'
        print(f"  {arm:>8} {rad_per_psu*arm*1000:>9.1f} {pp:>9.3f} {ro:>11.1f} "
              f"{SUBPIXEL/pp:>12.3f}{flag}")

    print("\n[ 광원 — 스펙트럼 폭이 곧 경계 번짐 ]")
    psu_per_nm = abs(dn_dlam) / dn_dS
    print(f"  파장 민감도            {psu_per_nm:.3f} PSU / nm")
    for name, fwhm in (('백색 LED', 150.0), (f'단색 LED {LED_FWHM:.0f}nm', LED_FWHM),
                       ('레이저 다이오드', 1.0)):
        print(f"  {name:<18} 폭 {fwhm:6.1f} nm → 경계 번짐 {fwhm*psu_per_nm:6.2f} PSU")

    print("\n[ 온도 — 차분 측정의 효과 ]")
    raw  = abs(dn_dT) / dn_dS
    diff = abs(dn_dT_s - dn_dT) / dn_dS
    print(f"  절대 측정      {raw:.4f} PSU / degC")
    print(f"  차분 측정      {diff:.4f} PSU / degC   ({raw/diff:.0f} 배 개선)")
    print(f"  → 표준액과 시료를 같은 온도에서 재고 그 차이를 쓸 것")

    print("\n[ 캐리오버 — 보관액 선택 ]")
    for label, s_store in (('RO-DI', 0.0), (f'{S_STD} PSU 표준액', S_STD)):
        print(f"  {label:<16} 1% 잔류 시 오차 = {0.01*abs(s_store-S_TANK):.3f} PSU")
    for target in (0.01, 0.001):
        v = -math.log(target)
        print(f"  잔류율 {target*100:>5.1f}% 까지 → 셀 용적의 {v:.1f} 배 "
              f"= {v*CELL_ML:.1f} mL 플러시")

    print("\n[ 오차 예산 (자가보정 이후) ]")
    mech = ARM_MAT_PPM * ARM_MM * 1000 / um_per_psu   # 1 degC 당 PSU
    budget = [
        ('표준액 정확도',              0.100),
        ('에지 검출 노이즈',           SUBPIXEL / px_per_psu),
        ('기포 · 재현성',              0.030),
        ('캐리오버 (10x 플러시)',      0.010),
        ('기구 열팽창 잔차',           0.010),
        ('잔류 온도차 (2 degC 가정)',  diff * 2),
    ]
    for k, v in budget:
        print(f"  {k:<26} {v:6.3f} PSU")
    rss = math.sqrt(sum(v*v for _, v in budget))
    line()
    print(f"  {'RSS 합계':<26} {rss:6.3f} PSU")
    print(f"\n  (참고) 기구 열팽창 미보정 시 {mech:.3f} PSU/degC — 차분으로 상쇄됨")
    line('═')


if __name__ == '__main__':
    main()
