#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
수동 전자식 굴절 염도계(1단계) 의 계통오차 예산
==================================================

이 스크립트는 세 가지를 계산합니다.

  Q1. 2점 보정을 **직선**으로 하면 얼마나 틀리는가  (답: 0.084 PSU, 팔 길이와 무관)
  Q2. PRNU(화소 응답 불균일)가 위치 추정을 얼마나 밀어내는가
  Q3. 팔 길이를 바꾸면 위 둘이 어떻게 변하는가

**핵심 결론 두 개**

  - 직선성 오차 0.084 PSU 는 **팔 길이와 무관**하고, 알려진 응답 곡선을
    피팅하면 사라집니다. 가장 큰 항목이 펌웨어로 공짜로 없어집니다.
  - PRNU 는 팔이 짧을수록 커집니다(화소당 PSU 가 커지므로).
    플랫필드로 잔차를 0.2 %까지 내리는 것이 전제입니다.

잡음 한계는 `profile_crb.py` 가 따로 계산합니다 (0.014 PSU @1프레임).
온도 항(0.667 PSU/°C)은 기하와 무관해서 여기서 계산하지 않고 상수로 넣습니다 —
근거는 `../HANDOFF.md` §1.

외부 라이브러리가 필요 없습니다.

    python budget_manual.py
"""

import math
import random

import segment_optics as so

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
CHORD, SAG = 60.0, 30.0          # 반원 60x30x10 (2026-09-02 확정)
ARM_I = 40.0                     # 조명팔 [mm] — 액적(조명 패치)이 정한다
ARM_CONF = 60.0                  # 검출팔 [mm] — 화소당 PSU 와 기계 안정성이 정한다
FAN_CONF = 4.5                   # 확정 부채꼴 [deg]
TARGET = 0.12                    # 목표 [PSU]
NFRAME = 16                      # 프레임 평균
FLAT_RESID = 0.002               # 플랫필드 후 남는 PRNU 비율 (0.2 %)
T_SENSOR = 0.0625                # DS18B20 12비트 분해능 [degC]
DNDT_PSU = 0.667                 # 두 액의 온도차 1 degC 당 [PSU/degC]  (HANDOFF §1)
SNR1 = 1300.0                    # 단일 프레임 SNR (데이터시트 + 10비트 ADC)

# 팔 길이별 최적 슬릿 = sqrt(lambda*L)
ARMS = [(30.0, 0.13), (40.0, 0.15), (60.0, 0.19), (100.0, 0.30), (160.0, 0.30)]

PIX = so.PIXEL_MM
NS = so.n_water(so.T_C, 35.0)
NP = so.N_PRISM
DTH_DS = so.dtheta_dS()
TC = math.asin(NS / NP)

R, CY = so.segment_geometry(CHORD, SAG)
_P, CHIEF, _INC = so.trace(0.0, so.theta_c(34.0), R, CY)


# ----------------------------------------------------------------------
# 프레넬 프로파일 — 실제 신호는 계단이 아니라 이 곡선이다
# ----------------------------------------------------------------------
def fresnel_R(n1, n2, th1):
    """입사각 th1 (매질 n1 -> n2) 의 무편광 반사율. 전반사면 1.0"""
    s = n1 / n2 * math.sin(th1)
    if s >= 1.0:
        return 1.0
    th2 = math.asin(s)
    c1, c2 = math.cos(th1), math.cos(th2)
    rs = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
    rp = (n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)
    return (rs * rs + rp * rp) / 2.0


def profile(dS, width_psu):
    """theta_c 아래 dS [PSU] 지점의 세기. width_psu 로 가우시안 번짐 적용."""
    sg = width_psu / 2.563                  # 10~90 폭 -> sigma
    acc = wsum = 0.0
    for i in range(-18, 19):
        x = i * sg * 3.0 / 18
        g = math.exp(-0.5 * (x / sg) ** 2)
        th = TC - (dS + x) * DTH_DS
        acc += g * (fresnel_R(NP, NS, th) if th > 0 else 1.0)
        wsum += g
    return acc / wsum


# ----------------------------------------------------------------------
# Q1 — 2점 보정을 직선으로 하면
# ----------------------------------------------------------------------
def linearity_psu(arm):
    p = {S: so.detector_pos(0.0, so.theta_c(S), R, CY, CHIEF, arm)
         for S in (0.0, 5.0, 10.0, 17.5, 25.0, 30.0, 34.0, 35.0)}
    mm_per_psu = abs(p[35.0] - p[0.0]) / 35.0
    line = lambda S: p[0.0] + (p[35.0] - p[0.0]) * S / 35.0
    err = {S: (p[S] - line(S)) / mm_per_psu for S in p}
    return max(abs(v) for v in err.values()), err


# ----------------------------------------------------------------------
# Q2 — PRNU 가 위치 추정을 밀어내는 양 (선형화 추정기 + 몬테카를로)
# ----------------------------------------------------------------------
def prnu_bias(arm, slit, sigma_g, trials=400, npx=128, seed=7):
    r = so.edge_width_psu(R, CY, CHIEF, arm, slit)
    if not r:
        return None
    width_psu, _tot, _geo, _dif, _spec, span = r
    psu_per_px = 35.0 / (span / PIX)
    xs = [(i - 8) * psu_per_px for i in range(npx)]
    I0 = [profile(x, width_psu) for x in xs]
    h = 0.05
    D = [(profile(x + h, width_psu) - profile(x - h, width_psu)) / (2 * h) for x in xs]
    den = sum(d * d for d in D)
    if den <= 0:
        return None
    random.seed(seed)
    acc = 0.0
    for _ in range(trials):
        num = sum((I0[i] * random.gauss(0.0, sigma_g)) * (-D[i]) for i in range(npx))
        acc += (num / den) ** 2
    return math.sqrt(acc / trials), width_psu, psu_per_px, span / PIX


def noise_sigma(arm, slit, nframe):
    """profile_crb.py 와 같은 CRB. 여기서는 예산 합산용으로만."""
    r = so.edge_width_psu(R, CY, CHIEF, arm, slit)
    width_psu, _t, _g, _d, _s, span = r
    psu_per_px = 35.0 / (span / PIX)
    h = 0.05
    tot = 0.0
    for i in range(128):
        x = (i - 8) * psu_per_px
        d = (profile(x + h, width_psu) - profile(x - h, width_psu)) / (2 * h)
        tot += d * d
    return (1.0 / (SNR1 * math.sqrt(nframe))) / math.sqrt(tot)


# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("수동 전자식 굴절 염도계 — 계통오차 예산")
    print("=" * 70)
    print("반원 %g x %g · 아크릴 n=%.4f · %g nm · 목표 +-%.2f PSU"
          % (CHORD, SAG, NP, so.LAMBDA_NM, TARGET))
    print("감도 %.1f urad/PSU   1 deg = %.1f PSU"
          % (DTH_DS * 1e6, 1.0 / math.degrees(DTH_DS)))
    print()

    print("[Q1] 2점 보정을 **직선**으로 했을 때의 오차")
    nl, err = linearity_psu(ARM_CONF)
    for S in sorted(err):
        print("      %5.1f PSU -> %+.4f PSU" % (S, err[S]))
    print("      최대 %.4f PSU" % nl)
    print("      팔 길이를 바꿔도 같은 값인지 확인:")
    for arm, _slit in ARMS:
        print("        팔 %5.1f mm -> %.4f PSU" % (arm, linearity_psu(arm)[0]))
    print("      >>> 팔 길이와 무관합니다. 순수하게 '직선 근사' 탓이고,")
    print("          응답 곡선은 물리로 계산되므로 **피팅하면 사라집니다.**")
    print()

    print("[Q2] PRNU 로 인한 위치 편향  (데이터시트 +-4 % typ)")
    print("      팔   슬릿  스팬   PSU/px  경계폭   보정없음   플랫 0.4%  플랫 0.2%")
    print("     [mm]  [mm]  [px]           [PSU]    [PSU]      [PSU]      [PSU]")
    for arm, slit in ARMS:
        b4, w, ppp, spx = prnu_bias(arm, slit, 0.040)
        b04 = prnu_bias(arm, slit, 0.004)[0]
        b02 = prnu_bias(arm, slit, 0.002)[0]
        print("     %4.0f  %.2f  %5.1f  %6.2f  %6.1f   %7.4f    %7.4f    %7.4f"
              % (arm, slit, spx, ppp, w, b4, b04, b02))
    print("      >>> 팔이 짧으면 화소당 PSU 가 커져 레버리지가 커집니다.")
    print("          플랫필드(§ILLUMINATION 6-4)가 **선택이 아니라 필수**입니다.")
    print()

    print("[Q3] 확정 형상(조명 %g / 검출 %g mm)의 예산 합산" % (ARM_I, ARM_CONF))
    slit_conf = round(math.sqrt(so.LAMBDA_NM * 1e-6 * ARM_CONF), 2)
    items = [
        ("잡음 (%d프레임, SNR %.0f)" % (NFRAME, SNR1), noise_sigma(ARM_CONF, slit_conf, NFRAME)),
        ("PRNU (플랫필드 잔차 %.1f %%)" % (FLAT_RESID * 100),
         prnu_bias(ARM_CONF, slit_conf, FLAT_RESID)[0]),
        ("2점 보정 — 곡선 피팅 후 잔차", 0.005),
        ("온도 (센서 %.4f degC x %.3f)" % (T_SENSOR, DNDT_PSU), T_SENSOR * DNDT_PSU),
    ]
    for name, v in items:
        print("      %-34s %.4f PSU" % (name, v))
    rss = math.sqrt(sum(v * v for _n, v in items))
    print("      %-34s %.4f PSU" % ("제곱합", rss))
    rest = math.sqrt(max(0.0, TARGET ** 2 - rss ** 2))
    print("      %-34s %.4f PSU" % ("미광·표면굴곡·드리프트 여유", rest))
    print()
    print("      비교 — 직선 보정을 그대로 쓰면:")
    items2 = list(items)
    items2[2] = ("2점 보정 — 직선 그대로", nl)
    rss2 = math.sqrt(sum(v * v for _n, v in items2))
    print("      제곱합 %.4f PSU -> 여유 %.4f PSU  (목표에 붙어서 사실상 실패)"
          % (rss2, math.sqrt(max(0.0, TARGET ** 2 - rss2 ** 2))))
    print()
    print("[Q4] 기계 안정성 — 칩이 프리즘에 대해 옆으로 미끄러지면")
    print("      검출팔  스팬   PSU/px   1 um 이동    0.05 PSU 허용 이동")
    print("       [mm]   [px]             [PSU]         [um]")
    for det in (40.0, 50.0, 60.0, 80.0, 100.0, 160.0):
        span = so.edge_width_psu(R, CY, CHIEF, det, 0.15)[5]
        ppp = 35.0 / (span / PIX)
        per_um = 1e-3 / PIX * ppp
        print("      %5.0f  %5.1f  %6.2f   %8.4f     %8.2f%s"
              % (det, span / PIX, ppp, per_um, 0.05 / per_um,
                 "   <= 확정" if abs(det - ARM_CONF) < 1e-9 else ""))
    print("      >>> **절대** 안정성이 아니라 보정과 시료 측정 사이(1분)의 상대 이동입니다.")
    print("      >>> 균일 열팽창은 무해합니다 — 본체가 통째로 커지면 각도는 안 변하고")
    print("          배율만 변해서 PLA 70 ppm/degC 로도 %.4f PSU/degC 입니다." % (70e-6*35))
    print("      >>> 위험한 것은 비대칭 이동. **뚜껑을 누르는 힘이 프리즘-칩 사이를")
    print("          휘게 하면 안 됩니다** — 힌지를 받침대로 물려 하중 경로를 우회시킬 것.")
    print()
    print("[Q5] 부채꼴과 액적  (조명팔 %g mm 기준)" % ARM_I)
    for fan in (3.0, FAN_CONF, 6.0, 13.4):
        reach = 2 * ARM_CONF * math.tan(fan / 2 * math.pi / 180)
        patch = 16.51 * (ARM_I / 250.0) * (fan / 2.0)
        dia = patch + 2.5
        vol = math.pi * (dia / 2) ** 2 * 0.2
        print("      부채꼴 %5.1f deg -> 도달 %4.2f mm (%4.0f px) · 패치 %4.1f mm"
              " · 액적 지름 %4.1f mm = %3.0f uL%s"
              % (fan, reach, reach / PIX, patch, dia, vol,
                 "   <= 확정" if abs(fan - FAN_CONF) < 1e-9 else ""))
    print("      >>> 어레이를 채울 필요가 없습니다. 프레넬 곡선의 유용 각도폭이")
    print("          %.2f deg 뿐이므로, 부채꼴을 줄여 **액적을 작게** 하는 것이 이득입니다."
          % (171 * math.degrees(DTH_DS)))


if __name__ == "__main__":
    main()
