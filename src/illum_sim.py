# -*- coding: utf-8 -*-
"""조명 배치 B(렌즈 없음) 광선추적 — ../ILLUMINATION.md 의 수치를 재현한다.

기하·굴절률·굴절 함수는 segment_optics.py 를 그대로 import 하므로
두 스크립트의 결과는 정의상 일치한다 (주광선 검증: detector_pos 와 73.64 px 일치).

    python src/illum_sim.py

무엇을 계산하는가
-----------------
  1. 경계 폭이 조명팔 길이에 어떻게 의존하는가   (= 슬릿폭 x 검출팔/조명팔)
  2. 경계 폭이 슬릿 폭에 어떻게 의존하는가
  3. 부채꼴이 정하는 측정면 조명 패치 폭
  4. 염도가 0->35 PSU 로 바뀔 때 경계가 측정면 위에서 이동하는 거리
  5. 표면 기울기 오차 -> 2점 보정 후 남는 염도 오차
     (선형 기울기는 흡수되고, 짧은 주기 굴곡만 문제가 된다)

회절은 광선추적으로 계산할 수 없다. 여기 나오는 '경계 폭'은 기하 성분만이다.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segment_optics as so

NP=so.N_PRISM; PIX=so.PIXEL_MM
# ---- 형상과 팔 기준점 (2026-09-02 정정) ------------------------------
# 이 파일은 활꼴 60x20 @ 팔 250 으로 굳어 있었다. ILLUMINATION.md 의 계수
# (PATCH_M=1.89, EDGE_K=0.88, SWEEP_250=1.424)가 전부 그 조건에서 맞춘 값이다.
# 확정 형상은 **반원 60x30** 이고 그 계수들은 여기에 맞지 않는다 — 쓰지 말 것.
#
# ★ 이 파일 안에 기준점이 두 개 섞여 있다:
#     arm_s (조명팔)  : P_IN = 곡면 통과점 E 기준
#     ARM_D (검출기)  : 원점 = 측정점 M 기준
#   반원이면 지렛대 = R + 기계팔 이므로 기계팔 60 인 물건은 ARM_D = 90 이다.
CHORD_MM, SAG_MM = 60., 30.      # 확정 형상
ARM_D = 90.                      # 검출 지렛대 (M 기준) = R 30 + 기계팔 60
R,CY=so.segment_geometry(CHORD_MM, SAG_MM)
n_w=lambda S: so.n_water(so.T_C,S)
TH_INT=so.theta_c(so.S_AIM)      # 주광선 조준 = 보정범위 중앙(17.5 PSU)
_,CHIEF,_=so.trace(0.,TH_INT,R,CY)                      # 외부 주광선 방향
C_DIR=CHIEF; C_PERP=(-CHIEF[1],CHIEF[0])
A_DIR=(-CHIEF[0],CHIEF[1])                              # 조명팔 (거울상)
A_PERP=(CHIEF[1],CHIEF[0])
# 주광선은 곡면에서 꺾이므로 조명축은 '원점'이 아니라
# 출사점 P_out 의 거울상 P_in 을 지난다. 슬릿은 거기서 arm_s 만큼 나간 자리.
_POUT,_,_=so.trace(0.,TH_INT,R,CY)
P_IN=(-_POUT[0],_POUT[1])
CHORD=CHORD_MM

def unit(v):
    m=math.hypot(*v); return (v[0]/m,v[1]/m)
def circ(o,d,near):
    ox,oy=o[0],o[1]-CY
    b=2*(ox*d[0]+oy*d[1]); c=ox*ox+oy*oy-R*R
    disc=b*b-4*c
    if disc<0: return None
    s=math.sqrt(disc); t=(-b-s)/2 if near else (-b+s)/2
    return t if t>1e-9 else None
def refr(d,nv,n1,n2):
    ci=-(d[0]*nv[0]+d[1]*nv[1])
    if ci<0: nv=(-nv[0],-nv[1]); ci=-ci
    e=n1/n2; k=1-e*e*(1-ci*ci)
    if k<0: return None
    ct=math.sqrt(k)
    return unit((e*d[0]+(e*ci-ct)*nv[0], e*d[1]+(e*ci-ct)*nv[1]))

def trace(arm_s,p,delta,slope=None):
    S=(P_IN[0]+arm_s*A_DIR[0]+p*A_PERP[0], P_IN[1]+arm_s*A_DIR[1]+p*A_PERP[1])
    b=(-A_DIR[0],-A_DIR[1]); cd,sd=math.cos(delta),math.sin(delta)
    d=unit((b[0]*cd-b[1]*sd, b[0]*sd+b[1]*cd))
    t=circ(S,d,True)
    if t is None: return None
    P=(S[0]+t*d[0],S[1]+t*d[1])
    if P[1]<=0: return None
    nv=unit((P[0]/R,(P[1]-CY)/R))
    d2=refr(d,nv,1.0,NP)
    if d2 is None or d2[1]>=-1e-12: return None
    x=P[0]-P[1]*d2[0]/d2[1]
    if abs(x)>CHORD/2: return None
    inc=math.acos(min(1.0,abs(d2[1])))
    eps=slope(x) if slope else 0.0
    dr=(d2[0],-d2[1])
    if eps:
        ca,sa=math.cos(2*eps),math.sin(2*eps)
        dr=(dr[0]*ca-dr[1]*sa, dr[0]*sa+dr[1]*ca)
    O=(x,0.); t3=circ(O,dr,False)
    if t3 is None: return None
    Q=(O[0]+t3*dr[0],O[1]+t3*dr[1])
    d3=refr(dr,unit((Q[0]/R,(Q[1]-CY)/R)),NP,1.0)
    if d3 is None: return None
    Cc=(ARM_D*C_DIR[0],ARM_D*C_DIR[1])
    den=d3[0]*C_DIR[0]+d3[1]*C_DIR[1]
    if abs(den)<1e-12: return None
    s_=((Cc[0]-Q[0])*C_DIR[0]+(Cc[1]-Q[1])*C_DIR[1])/den
    H=(Q[0]+s_*d3[0],Q[1]+s_*d3[1])
    return x, inc+eps, (H[0]-Cc[0])*C_PERP[0]+(H[1]-Cc[1])*C_PERP[1]

def cutoff(arm_s,slit,fan,S_psu,slope=None,N=41):
    """슬릿 각 점에서 '입사각==theta_c' 인 광선의 검출기 위치.
       반환 (평균 X, X 폭, 평균 측정면 x, 측정면 x 폭)"""
    thc=math.asin(n_w(S_psu)/NP); h=math.radians(fan)/2
    Xs=[];xs=[]
    for i in range(N):
        p=(-slit/2+slit*i/(N-1)) if slit>0 and N>1 else 0.
        f=lambda dl:(trace(arm_s,p,dl,slope) or (0,-9,0))[1]-thc
        lo,hi=-h,h
        if f(lo)*f(hi)>0: continue
        for _ in range(70):
            mid=(lo+hi)/2
            if f(lo)*f(mid)<=0: hi=mid
            else: lo=mid
        r=trace(arm_s,p,(lo+hi)/2,slope)
        if r: Xs.append(r[2]); xs.append(r[0])
    if not Xs: return None
    return (sum(Xs)/len(Xs), max(Xs)-min(Xs), sum(xs)/len(xs), max(xs)-min(xs))

def beam_at(arm_s,slit,fan,lever):
    """검출기면(M 기준 lever)에서의 실제 빔 폭 [mm].
       ★ 이 빔은 팔 끝으로 갈수록 좁아진다 — 곡면이 렌즈로 작동해 슬릿을
         결상하기 때문이다. 2*lever*tan(fan/2) 로 계산하면 안 된다."""
    global ARM_D
    keep, ARM_D = ARM_D, lever
    h=math.radians(fan)/2; Xs=[]
    for i in range(9):
        p=(-slit/2+slit*i/8) if slit>0 else 0.
        for j in range(81):
            r=trace(arm_s,p,-h+2*h*j/80)
            if r: Xs.append(r[2])
    ARM_D = keep
    return (max(Xs)-min(Xs)) if Xs else 0.


def patch(arm_s,slit,fan):
    h=math.radians(fan)/2; xs=[]
    for i in range(15):
        p=(-slit/2+slit*i/14) if slit>0 else 0.
        for j in range(61):
            r=trace(arm_s,p,-h+2*h*j/60)
            if r: xs.append(r[0])
    return (min(xs),max(xs)) if xs else (0.,0.)


# ----------------------------------------------------------------------
def _cal_err(slope, arm=250., slit=0.3, fan=2.0, S_true=34.):
    """표면 기울기 오차 slope(x) 를 넣고 2점 보정을 통과시킨 뒤 남는 염도 오차."""
    c0 = cutoff(arm, slit, fan, 0., slope)
    c35 = cutoff(arm, slit, fan, 35., slope)
    cs = cutoff(arm, slit, fan, S_true, slope)
    if None in (c0, c35, cs) or abs(c35[0] - c0[0]) < 1e-9:
        return None
    return 35. * (cs[0] - c0[0]) / (c35[0] - c0[0]) - S_true


def main():
    P = PIX
    print()
    print("=" * 70)
    print("조명 배치 B 광선추적   활꼴 R=%.2f mm, 검출팔 %.0f mm, 중심각 %.3f deg"
          % (R, ARM_D, math.degrees(TH_INT)))
    print("=" * 70)

    r = trace(250., 0., 0.)
    print()
    print("[ 검증 ] 조명축 그대로 쏘면 원점에 임계각으로 도달해야 한다")
    print("   측정면 x = %+.6f mm (0 이어야)   입사각 = %.6f deg (%.6f 이어야)"
          % (r[0], math.degrees(r[1]), math.degrees(TH_INT)))
    ref = so.detector_pos(0., TH_INT, R, CY, C_DIR)
    print("   검출기 %+.2f px = segment_optics.detector_pos %+.2f px"
          % (r[2] / P, ref / P))

    print()
    print("[ 1. 경계 폭 vs 조명팔 ]  슬릿 0.3 mm, 부채꼴 2 deg")
    print("   %10s %13s %14s" % ("조명팔[mm]", "경계폭[px]", "조명패치[mm]"))
    for a in (60., 125., 250., 500.):
        c = cutoff(a, 0.3, 2.0, 34.)
        if not c:
            continue
        lo, hi = patch(a, 0.3, 2.0)
        print("   %10.0f %13.2f %14.2f" % (a, c[1] / P, hi - lo))
    print("   -> 경계폭 = 슬릿폭 x (검출팔/조명팔). 1:1(250mm) 이면 슬릿폭 그대로")

    print()
    print("[ 2. 경계 폭 vs 슬릿 폭 ]  조명팔 250 mm")
    print("   %9s %13s" % ("슬릿[mm]", "경계폭[px]"))
    for sl in (0.05, 0.1, 0.2, 0.3, 0.6, 1.0):
        c = cutoff(250., sl, 2.0, 34.)
        if c:
            print("   %9.2f %13.2f" % (sl, c[1] / P))

    print()
    print("[ 3. 부채꼴이 정하는 측정면 패치 ]  슬릿 0.3 mm, 조명팔 250 mm")
    for f in (0.5, 1.0, 2.0, 3.0):
        lo, hi = patch(250., 0.3, f)
        print("   부채꼴 %.1f deg -> 패치 %5.2f mm  (x = %+.1f ~ %+.1f)"
              % (f, hi - lo, lo, hi))

    print()
    print("[ 4. 염도가 바뀌면 경계가 측정면 위에서 이동한다 ]")
    print("   %6s %14s %14s %s" % ("PSU", "측정면 x[mm]", "검출기[px]", "x 이동"))
    base = None
    for S in (0., 17.5, 34., 35.):
        c = cutoff(250., 0.3, 2.0, S)
        if base is None:
            base = c[2]
        print("   %6.1f %14.4f %14.2f  %+.3f mm" % (S, c[2], c[0] / P, c[2] - base))

    print()
    print("[ 5. 표면 기울기 오차 -> 2점 보정 후 염도 오차 ]")
    base = _cal_err(None)
    print("   완벽한 평면: %+.4f PSU  (기하 직선성 오차, 상수)" % base)
    print()
    print("(a) 선형 기울기  eps = k*x  — 흡수되는가")
    lo, hi = patch(250., 0.3, 2.0)
    print("   %14s %18s %14s" % ("k[urad/mm]", "패치 양단차[urad]", "오차[PSU]"))
    for k_ur in (0., 100., 1000.):
        e = _cal_err(lambda x, k=k_ur * 1e-6: k * x)
        print("   %14.0f %18.0f %14.4f" % (k_ur, k_ur * (hi - lo), e))
    print("   -> 크기와 무관하게 흡수된다. 2점 보정이 재는 것이 바로 이 환율이므로")

    print()
    print("(b) 정현파 굴곡  eps = A*sin(2*pi*x/L)  — 주기가 문제")
    print("   경계는 0->35 PSU 동안 %.2f mm 만 움직인다. 그 거리 대비 주기가 관건."
          % 1.424)
    print("   %10s %12s %14s %14s" % ("주기 L[mm]", "진폭 A[urad]", "PV 사각[nm]", "오차[PSU]"))
    for L, A_ur in ((0.5, 100.), (1.5, 100.), (5.0, 100.), (20.0, 1000.)):
        A = A_ur * 1e-6
        sag = 2 * A * L / (2 * math.pi) * 1e6
        e = _cal_err(lambda x, A=A, L=L: A * math.sin(2 * math.pi * x / L))
        print("   %10.1f %12.0f %14.0f %14.4f" % (L, A_ur, sag, e))
    print("   -> 0.5~2 mm 주기에서 lambda/20 급 평면도가 필요하다 (배치 B 한정).")
    print("      배치 A(콘덴서로 집광)는 경계 자리가 고정이라 이 요구가 없다.")
    print()


if __name__ == "__main__":
    main()
