# -*- coding: utf-8 -*-
"""프로파일 위치 추정의 정보 한계 (Cramer-Rao) 로 투과형 vs 반사형을 비교.

'경계 폭'은 계단 모델의 지표다. 실제 프로파일은 프레넬 곡선이고, 염도가 바뀌면
그 곡선이 통째로 평행이동한다. 알려진 모양의 평행이동량을 추정하는 한계는

    sigma_S = sigma_I / sqrt( sum_i (dI_i/dS)^2 )

이고, 이것은 '폭'이 아니라 '기울기의 제곱합'이 정한다. 폭이 넓어도 기울기가
살아 있으면 정밀도가 나온다.
"""
import math
import segment_optics as so

NS = so.n_water(so.T_C, 35.0)
NP = so.N_PRISM
DTH_DS = so.dtheta_dS()                 # rad/PSU
PSU_PER_DEG = 1.0 / math.degrees(DTH_DS)


def fresnel_R(n1, n2, th1):
    s = n1 / n2 * math.sin(th1)
    if s >= 1.0:
        return 1.0
    th2 = math.asin(s)
    c1, c2 = math.cos(th1), math.cos(th2)
    rs = (n1*c1 - n2*c2) / (n1*c1 + n2*c2)
    rp = (n1*c2 - n2*c1) / (n1*c2 + n2*c1)
    return (rs*rs + rp*rp) / 2.0


def refl(dS, nsamp):
    """반사형: theta_c 로부터 dS [PSU] 만큼 아래 각도에서의 반사율."""
    tc = math.asin(nsamp / NP)
    th = tc - dS * DTH_DS
    if th <= 0:
        return 1.0
    return fresnel_R(NP, nsamp, th)


def trans(dS, nsamp):
    """투과형: 같은 자리에서 시료->프리즘 투과율 (램버시안 시료)."""
    tc = math.asin(nsamp / NP)
    th = tc - dS * DTH_DS
    if th <= 0:
        return 0.0
    s = NP / nsamp * math.sin(th)
    if s >= 1.0:
        return 0.0
    th_s = math.asin(s)
    return 1.0 - fresnel_R(nsamp, NP, th_s)


def blur(f, dS, nsamp, w_psu):
    """가우시안 번짐 (회절+기하) 를 PSU 폭 w 로 적용. w 는 10~90 폭 근사 -> sigma = w/2.563"""
    if w_psu <= 0:
        return f(dS, nsamp)
    sg = w_psu / 2.563
    n, acc, wsum = 25, 0.0, 0.0
    for i in range(-n, n+1):
        x = i * sg * 3.0 / n
        g = math.exp(-0.5*(x/sg)**2)
        acc += g * f(dS + x, nsamp)
        wsum += g
    return acc / wsum


def crb(f, w_psu, psu_per_px, npx, snr, nframe, span_psu=140.0):
    """화소마다 dI/dS 를 수치미분해 정보합을 낸다. 화소는 theta_c 아래로 깔린다."""
    h = 0.02
    tot = 0.0
    used = 0
    for i in range(npx):
        dS = (i - 6) * psu_per_px          # theta_c 위 6화소 여유
        if dS < -3*w_psu - 1 or dS > span_psu:
            continue
        d = (blur(f, dS + h, NS, w_psu) - blur(f, dS - h, NS, w_psu)) / (2*h)
        tot += d*d
        used += 1
    if tot <= 0:
        return None, used
    sigma_I = 1.0 / (snr * math.sqrt(nframe))
    return sigma_I / math.sqrt(tot), used


print('n_s = %.5f  n_p = %.4f  theta_c = %.4f deg  감도 %.1f urad/PSU'
      % (NS, NP, math.degrees(math.asin(NS/NP)), DTH_DS*1e6))
print('1 deg = %.1f PSU' % PSU_PER_DEG)
print()
print('프로파일 값 (theta_c 아래 dS PSU 지점)')
print('    dS[PSU]    반사형 R    투과형 T')
for dS in (0, 1, 3, 10, 30, 60, 120):
    print('     %6.1f     %7.4f     %7.4f' % (dS, refl(dS, NS), trans(dS, NS)))
print()

print('── 번짐(회절+기하+표면)에 대한 둔감성 ──')
print('   번짐[PSU]   반사형 sigma(1프레임)   투과형 sigma')
for w in (0.72, 2.0, 5.0, 8.94, 20.0, 40.0, 80.0):
    sr, _ = crb(refl, w, 2.308, 128, 1300.0, 1)
    st, _ = crb(trans, w, 2.308, 128, 1300.0, 1)
    print('   %8.2f      %.4f PSU            %.4f PSU' % (w, sr, st))
print()
print('── 화소 피치(= 팔 길이)에 대한 둔감성, 번짐 8.94 PSU 고정 ──')
print('   PSU/px   팔[mm]   반사형 sigma(1프레임)   유효화소')
for ppp, arm in ((1.44, 160), (2.31, 100), (3.85, 60), (7.76, 30)):
    sr, u = crb(refl, 8.94, ppp, 128, 1300.0, 1)
    print('   %6.2f     %4d       %.4f PSU            %3d' % (ppp, arm, sr, u))
print()
print('── 프레임 평균 ──')
for nf in (1, 16, 64):
    sr, _ = crb(refl, 8.94, 2.308, 128, 1300.0, nf)
    print('   %2d프레임 : %.4f PSU' % (nf, sr))
print()
print('목표 +-0.12 PSU.')
print('T = 1 - R 이므로 투과형과 반사형의 정보량은 **정확히 같습니다.**')
print('이 sigma 는 잡음 한계입니다. 계통오차(미광·PRNU·드리프트·스펙트럼)는 별도이고,')
print('위 숫자들이 목표보다 10배 작으므로 **예산 전체가 계통오차 몫**입니다.')
