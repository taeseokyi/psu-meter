# -*- coding: utf-8 -*-
"""측정 헤드 조립 단면도"""
import math
from kfont import DEEP, TEAL, MID, AMB, INK, GREY, figpath
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Rectangle, Circle, Wedge,
                                Polygon, PathPatch, FancyArrowPatch)
from matplotlib.path import Path
import numpy as np

AL='#C8CDD2'; ALD='#A7AEB5'; PTFE='#F0F2F4'; PTFED='#C6CBD0'
GLASS='#D9E9F2'; GLASSE='#5F97B5'; WATER='#BFE0EF'
ORING='#2E2E2E'; FOAM='#EDE2CE'; FOAME='#C9B896'
AMB='#E8901F'; DEEP='#065A82'; MID='#21295C'; INK='#1A2430'; GREY='#78899A'
BLACKBOX='#2B3238'

TC = 61.928                  # 임계각
ARM_DEG = 90 - TC            # 수평 기준 28.07도
th = math.radians(TC)

fig, ax = plt.subplots(figsize=(15.5, 9.4), dpi=150)
ax.set_xlim(0, 155); ax.set_ylim(0, 94); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 155, 94, facecolor='white', zorder=0))

CX, CY = 52.0, 58.0          # 측정면 중심 (프리즘 평면의 중앙)

# ── 단열 하우징 ────────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((6, 12), 94, 62,
    boxstyle='round,pad=0.2,rounding_size=1.6', facecolor=FOAM,
    edgecolor=FOAME, lw=1.6, zorder=1))
ax.text(9.5, 71.2, '단열 하우징 (스티로폼)', fontsize=9.0,
        color='#8A7A55', fontweight='bold', va='center', zorder=3)

# ── 차광 박스 (알루미늄 광학 벤치) ─────────────────────────────
ax.add_patch(FancyBboxPatch((11, 17), 84, 50,
    boxstyle='round,pad=0.15,rounding_size=1.2', facecolor=BLACKBOX,
    edgecolor='#1A1F24', lw=1.4, zorder=2))
ax.text(13.5, 20.6, '차광 알루미늄 블록 — 광학 벤치 겸 열용량체', fontsize=8.8,
        color='#9FB3C0', fontweight='bold', va='center', zorder=4)

# ── 광학 팔 (보어) ────────────────────────────────────────────
ARM = 40.0
def arm_end(sign, L=ARM):
    return (CX + sign*L*math.sin(th), CY - L*math.cos(th))

for sign in (-1, 1):
    ex, ey = arm_end(sign)
    dx, dy = ex-CX, ey-CY
    n = math.hypot(dx, dy); px_, py_ = -dy/n, dx/n
    hw = 3.1
    ax.add_patch(Polygon([(CX+px_*hw, CY+py_*hw), (ex+px_*hw, ey+py_*hw),
                          (ex-px_*hw, ey-py_*hw), (CX-px_*hw, CY-py_*hw)],
                         closed=True, facecolor='#171C21', edgecolor='#0D1114',
                         lw=1.0, zorder=5))
    # 배플 (미광 차단)
    for f in (0.34, 0.55, 0.76):
        bx, by = CX+dx*f, CY+dy*f
        ax.plot([bx+px_*hw, bx+px_*1.15], [by+py_*hw, by+py_*1.15],
                color='#4A555E', lw=2.0, zorder=6, solid_capstyle='butt')
        ax.plot([bx-px_*hw, bx-px_*1.15], [by-py_*hw, by-py_*1.15],
                color='#4A555E', lw=2.0, zorder=6, solid_capstyle='butt')

# 광선
for sign, col in ((-1, AMB), (1, AMB)):
    ex, ey = arm_end(sign, ARM-4)
    if sign < 0:
        ax.annotate('', xy=(CX, CY), xytext=(ex, ey),
                    arrowprops=dict(arrowstyle='-|>', lw=2.2, color=col,
                                    mutation_scale=15), zorder=8)
    else:
        ax.annotate('', xy=(ex, ey), xytext=(CX, CY),
                    arrowprops=dict(arrowstyle='-|>', lw=2.2, color=col,
                                    mutation_scale=15), zorder=8)
    for d in (-2.0, 2.0):
        t2 = math.radians(TC+d)
        e2 = (CX+sign*(ARM-4)*math.sin(t2), CY-(ARM-4)*math.cos(t2))
        ax.plot([CX, e2[0]], [CY, e2[1]], color=col, lw=0.8, ls=':',
                alpha=.75, zorder=7)

# ── 프리즘 (반원통) ───────────────────────────────────────────
PR = 11.0
ax.add_patch(Wedge((CX, CY), PR, 180, 360, facecolor=GLASS,
                   edgecolor=GLASSE, lw=1.8, zorder=10))
ax.text(CX, CY-8.4, 'BK7 반원통', ha='center', va='center', fontsize=7.4,
        color=DEEP, fontweight='bold', zorder=12)
ax.plot([CX-PR, CX+PR], [CY, CY], color=MID, lw=2.6, zorder=12)

# ── 각도 표시 ─────────────────────────────────────────────────
ax.plot([CX, CX], [CY, CY+13], color=GREY, lw=1.0, ls='-.', zorder=11)
ax.text(CX+0.8, CY+12.6, '법선', fontsize=8, color=GREY, va='top', zorder=11)
for sign in (-1, 1):
    a = np.linspace(0, th, 50)
    ax.plot(CX+sign*7.2*np.sin(a), CY-7.2*np.cos(a), color='white', lw=1.4,
            zorder=13)
ax.text(CX-4.9, CY-4.2, '61.93°', fontsize=8.4, color='white',
        fontweight='bold', ha='center', zorder=14)
ax.text(CX+4.9, CY-4.2, '61.93°', fontsize=8.4, color='white',
        fontweight='bold', ha='center', zorder=14)

# ── 플로우셀 (PTFE 상판) ──────────────────────────────────────
FW, FH = 34.0, 13.0
ax.add_patch(FancyBboxPatch((CX-FW/2, CY+0.6), FW, FH,
    boxstyle='round,pad=0.1,rounding_size=0.8', facecolor=PTFE,
    edgecolor=PTFED, lw=1.6, zorder=14))
ax.add_patch(Rectangle((CX-11.5, CY+0.6), 23.0, 7.4, facecolor=WATER,
                       edgecolor='none', zorder=15))
ax.text(CX, CY+4.3, '시료  2 mL', ha='center', va='center', fontsize=8,
        color=DEEP, fontweight='bold', zorder=17)
ax.text(CX, CY+11.2, 'PTFE 플로우셀 상판', ha='center', va='center',
        fontsize=8.4, color='#5A6570', fontweight='bold', zorder=17)

# O-링
for sx in (-1, 1):
    ax.add_patch(Circle((CX+sx*12.4, CY+1.5), 1.25, facecolor=ORING,
                        edgecolor='#000', lw=0.6, zorder=18))
ax.annotate('O-링 (Viton)\n젖는 면적을 이 안쪽으로', xy=(CX+12.4, CY+1.5),
            xytext=(CX+26.0, CY+16.0), fontsize=8.2, color=INK,
            fontweight='bold', ha='left', va='center', linespacing=1.5,
            arrowprops=dict(arrowstyle='-', lw=1.1, color=INK), zorder=20)

# 포트
ax.annotate('', xy=(CX-11.0, CY+2.4), xytext=(CX-24.0, CY+2.4),
            arrowprops=dict(arrowstyle='-|>', lw=2.2, color=DEEP,
                            mutation_scale=14), zorder=19)
ax.text(CX-25.0, CY+2.4, '주입', fontsize=8.2, color=DEEP, ha='right',
        va='center', fontweight='bold', zorder=19)
ax.annotate('', xy=(CX+24.0, CY+11.0), xytext=(CX+11.0, CY+11.0),
            arrowprops=dict(arrowstyle='-|>', lw=1.8, color=GREY,
                            mutation_scale=13), zorder=19)
ax.text(CX+25.0, CY+11.0, '벤트', fontsize=8.2, color=GREY, ha='left',
        va='center', fontweight='bold', zorder=19)
ax.annotate('', xy=(CX+24.0, CY+2.0), xytext=(CX+11.0, CY+2.0),
            arrowprops=dict(arrowstyle='-|>', lw=2.2, color=AMB,
                            mutation_scale=14), zorder=19)
ax.text(CX+25.0, CY+2.0, '배수', fontsize=8.2, color=AMB, ha='left',
        va='center', fontweight='bold', zorder=19)

# 클램프 (프리즘 압착)
for sx in (-1, 1):
    ax.add_patch(Rectangle((CX+sx*16.4-1.4, CY-3.0), 2.8, 17.0,
                           facecolor=ALD, edgecolor='#8A9199', lw=0.8,
                           zorder=16))
    ax.add_patch(Circle((CX+sx*16.4, CY+12.2), 1.5, facecolor='#8A9199',
                        edgecolor='#6E757C', lw=0.6, zorder=19))
ax.text(CX-16.4, CY+15.8, '클램프 볼트\n(접착 금지)', ha='center', va='bottom',
        fontsize=7.8, color=INK, fontweight='bold', zorder=19, linespacing=1.5)

# ── LED 어셈블리 ──────────────────────────────────────────────
lx, ly = arm_end(-1)
ax.add_patch(Circle((lx, ly), 2.6, facecolor=AMB, edgecolor='white', lw=1.6,
                    zorder=12))
ax.add_patch(Rectangle((lx-4.2, ly-4.2), 1.6, 8.4, facecolor='#3B444B',
                       edgecolor='none', zorder=11))
ax.text(lx+1.0, ly-6.6, 'LED 590nm\n+ 슬릿 0.2 mm\n+ 정전류 구동',
        ha='center', va='top', fontsize=8.2, color='#F0D9B5', fontweight='bold',
        zorder=13, linespacing=1.55)

# ── TSL1401 ──────────────────────────────────────────────────
dx_, dy_ = arm_end(1)
ang = math.degrees(math.atan2(dy_-CY, dx_-CX))
ax.add_patch(Rectangle((dx_-1.0, dy_-4.0), 2.0, 8.0, facecolor='#14415C',
                       edgecolor='#0B2A3C', lw=1.0, zorder=12))
ax.add_patch(Rectangle((dx_-0.4, dy_-2.6), 0.8, 5.2, facecolor='#0B0B0B',
                       zorder=13))
ax.text(dx_-1.0, dy_-6.6, 'TSL1401CL\n렌즈 제거 후\n베어 센서면 사용',
        ha='center', va='top', fontsize=8.2, color='#BBD7E8', fontweight='bold',
        zorder=13, linespacing=1.55)

# 검출팔 치수
ax.annotate('', xy=(dx_, dy_), xytext=(CX, CY),
            arrowprops=dict(arrowstyle='<->', lw=1.1, color='#6FA8C7'),
            zorder=9)
mxa, mya = (CX+dx_)/2, (CY+dy_)/2
ax.text(mxa+3.0, mya+2.2, '검출팔 L = 250 mm', fontsize=8.4, color='#6FA8C7',
        fontweight='bold', rotation=ang, ha='center', va='center', zorder=9)

# ── 온도센서 ─────────────────────────────────────────────────
ax.add_patch(Rectangle((CX-9.0, CY+5.2), 4.6, 1.6, facecolor='#4A5560',
                       edgecolor='white', lw=0.8, zorder=17))
ax.text(CX-6.7, CY+8.0, 'DS18B20', fontsize=7.2, color='#3B4650', ha='center',
        va='bottom', fontweight='bold', zorder=18)

# ── 오른쪽 설명 ───────────────────────────────────────────────
ax.text(105.0, 71.5, '조립 핵심 5가지', fontsize=13.5, color=MID,
        fontweight='bold', ha='left', va='center')
pts = [
    ('프리즘은 접착하지 말고 클램프',
     'O-링으로 눌러 밀봉합니다. 접착제는 유리에\n응력을 주고 UV 경화형은 자외선에 열화됩니다.'),
    ('두 팔은 반드시 한 덩어리에',
     '별도 마운트 2개면 서로 움직입니다. 알루미늄\n블록 하나에 두 보어를 뚫어 강성을 확보합니다.'),
    ('보어 안에 배플',
     '미광이 검출기에 들어오면 배경이 생겨 경계가\n흐려집니다. 3~4단 조리개를 넣으십시오.'),
    ('센서 렌즈 제거',
     'TSL1401 모듈의 120° 광각 렌즈는 떼어냅니다.\n각도 분포를 그대로 받아야 합니다.'),
    ('열은 물리지 말고 가두기',
     '섬프 침수 대신 단열 + 알루미늄 열용량으로\n표준액과 시료를 같은 온도에 둡니다.'),
]
y = 65.0
for i, (t, b) in enumerate(pts):
    ax.add_patch(Circle((106.4, y), 1.35, facecolor=AMB, edgecolor='none',
                        zorder=5))
    ax.text(106.4, y, str(i+1), fontsize=8.6, color='white', ha='center',
            va='center', fontweight='bold', zorder=6)
    ax.text(109.8, y+0.1, t, fontsize=9.4, color=INK, va='center',
            fontweight='bold', zorder=6)
    ax.text(109.8, y-3.0, b, fontsize=8.1, color=GREY, va='center',
            linespacing=1.55, zorder=6)
    y -= 9.6

# ── 하단 치수 정보 ────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((6, 1.5), 148, 8.6,
    boxstyle='round,pad=0.15,rounding_size=0.7', facecolor='#F2F7FA',
    edgecolor='#D8E3EA', lw=1.0, zorder=3))
info = [('두 팔 사이각', '123.86°', '= 2 × 임계각'),
        ('각 팔의 경사', '28.07°', '수평면에서 아래로'),
        ('검출팔 L', '250 mm', '1 px ≈ 1 PSU'),
        ('입사팔', '30~50 mm', '슬릿-프리즘 거리'),
        ('부채꼴 폭', '± 2°', '경계선이 생기려면 필수')]
x0 = 11.0
for k, v, s in info:
    ax.text(x0, 7.8, k, fontsize=8.2, color=GREY, va='center', zorder=5)
    ax.text(x0, 5.1, v, fontsize=11.5, color=DEEP, fontweight='bold',
            va='center', zorder=5)
    ax.text(x0, 2.7, s, fontsize=7.4, color=GREY, va='center', zorder=5)
    x0 += 29.2

ax.text(6.0, 90.5, '측정 헤드 조립 단면도', fontsize=19, color=INK,
        fontweight='bold', va='center')
ax.text(6.0, 85.6,
        '광학부는 수조 안이 아니라 수조 밖 플로우셀에 있습니다. 프리즘 위쪽만 젖고, 아래쪽 광학계는 완전히 건조 상태로 유지됩니다.',
        fontsize=10, color=GREY, va='center')

plt.savefig(figpath('fig_head.png'), dpi=150, facecolor='white',
            bbox_inches='tight', pad_inches=0.15)
print('ok')
