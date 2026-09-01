# -*- coding: utf-8 -*-
"""MOSFET 펌프 구동 회로 상세"""
import math
from kfont import DEEP, TEAL, MID, AMB, INK, GREY, figpath
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
import numpy as np

INK='#1A2430'; GREY='#78899A'; DEEP='#065A82'; MID='#21295C'
AMB='#E8901F'; RED='#C0392B'; GRN='#1E8E3E'; LINE='#2B3238'

fig, ax = plt.subplots(figsize=(15.6, 9.2), dpi=150)
ax.set_xlim(0, 156); ax.set_ylim(0, 92); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 156, 92, facecolor='white', zorder=0))

def w(pts, c=LINE, lw=2.0, z=5):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    ax.plot(xs, ys, color=c, lw=lw, zorder=z, solid_capstyle='round',
            solid_joinstyle='round')

def dot(p, c=LINE, r=0.85, z=8):
    ax.add_patch(Circle(p, r, facecolor=c, edgecolor='none', zorder=z))

def res(x, y, label, horiz=True, z=6):
    if horiz:
        ax.add_patch(Rectangle((x, y-2.0), 11.0, 4.0, facecolor='white',
                               edgecolor=LINE, lw=1.8, zorder=z))
        ax.text(x+5.5, y+3.6, label, ha='center', va='bottom', fontsize=9.4,
                color=INK, fontweight='bold', zorder=z+1)
    else:
        ax.add_patch(Rectangle((x-2.0, y), 4.0, 11.0, facecolor='white',
                               edgecolor=LINE, lw=1.8, zorder=z))
        ax.text(x+3.4, y+5.5, label, ha='left', va='center', fontsize=9.4,
                color=INK, fontweight='bold', zorder=z+1)

def gnd(p, z=6, label=None):
    x, y = p
    for i, hw in enumerate((5.0, 3.2, 1.5)):
        ax.plot([x-hw, x+hw], [y-i*1.7, y-i*1.7], color=LINE, lw=2.2, zorder=z,
                solid_capstyle='round')
    if label:
        ax.text(x, y-7.4, label, ha='center', va='top', fontsize=8.6,
                color=GREY, zorder=z)

def diode(p, up=True, z=6):
    """세로 다이오드. up=True 면 전류가 위로 흐르는 방향(캐소드가 위)."""
    x, y = p
    if up:
        ax.add_patch(Polygon([(x-4.0, y-3.4), (x+4.0, y-3.4), (x, y+2.2)],
                             closed=True, facecolor=LINE, edgecolor=LINE,
                             lw=1.2, zorder=z))
        ax.plot([x-4.6, x+4.6], [y+2.4, y+2.4], color=LINE, lw=2.8, zorder=z,
                solid_capstyle='round')

def nmos(cx, cy, z=6):
    """N채널 MOSFET (게이트 왼쪽, 드레인 위, 소스 아래)"""
    w([(cx-8.0, cy), (cx-3.6, cy)], z=z)                       # 게이트 리드
    ax.plot([cx-3.6, cx-3.6], [cy-7.0, cy+7.0], color=LINE, lw=2.6, zorder=z)
    for dy_ in (-4.6, 0.0, 4.6):                                # 채널 3분할
        ax.plot([cx-1.4, cx-1.4], [cy+dy_-2.0, cy+dy_+2.0], color=LINE,
                lw=2.6, zorder=z)
    w([(cx-1.4, cy+4.6), (cx+5.0, cy+4.6), (cx+5.0, cy+11.0)], z=z)  # 드레인
    w([(cx-1.4, cy-4.6), (cx+5.0, cy-4.6), (cx+5.0, cy-11.0)], z=z)  # 소스
    w([(cx-1.4, cy), (cx+5.0, cy), (cx+5.0, cy-4.6)], z=z)           # 바디
    ax.add_patch(Polygon([(cx+1.0, cy-1.8), (cx+1.0, cy+1.8), (cx+3.4, cy)],
                         closed=True, facecolor=LINE, zorder=z))       # 바디다이오드 화살표
    ax.text(cx-6.0, cy+2.0, 'G', fontsize=9, color=GREY, ha='center', zorder=z)
    ax.text(cx+7.2, cy+9.0, 'D', fontsize=9, color=GREY, ha='center', zorder=z)
    ax.text(cx+7.2, cy-9.0, 'S', fontsize=9, color=GREY, ha='center', zorder=z)

# ══════════════════════════════════════════════════════════════
# 1채널 상세 회로
# ══════════════════════════════════════════════════════════════
X12, Y12 = 20.0, 78.0        # +12V 레일
XM, YM   = 62.0, 44.0        # MOSFET 중심
XG       = 20.0              # 게이트 라인 왼쪽 끝

# +12V 레일
w([(X12, Y12), (108.0, Y12)], c=RED, lw=2.6)
ax.text(X12-2.0, Y12, '+12 V', ha='right', va='center', fontsize=11,
        color=RED, fontweight='bold')
ax.text(108.0, Y12+3.0, 'SMPS  12 V 2~3 A', ha='right', va='bottom',
        fontsize=9, color=GREY)

# 펌프 (모터)
PX, PY = 84.0, 62.0
ax.add_patch(Circle((PX, PY), 7.4, facecolor='white', edgecolor=LINE, lw=2.2,
                    zorder=6))
ax.text(PX, PY, 'M', ha='center', va='center', fontsize=13, color=INK,
        fontweight='bold', zorder=7)
ax.text(PX+10.5, PY, '페리스탈틱 펌프\n(12 V DC 모터)', ha='left', va='center',
        fontsize=9.4, color=INK, fontweight='bold', linespacing=1.5)
w([(PX, Y12), (PX, PY+7.4)], c=RED)
w([(PX, PY-7.4), (PX, 49.0), (XM+5.0, 49.0), (XM+5.0, YM+11.0)])
dot((PX, Y12), c=RED)

# 플라이백 다이오드
DX = 70.0
diode((DX, 62.0))
w([(DX, Y12), (DX, 64.4)], c=RED)
w([(DX, 58.6), (DX, 49.0)])
dot((DX, Y12), c=RED); dot((DX, 49.0))
ax.text(DX-6.8, 63.6, '1N4007', ha='right', va='center', fontsize=9.4,
        color=INK, fontweight='bold')
ax.text(DX-6.8, 59.4, '밴드(캐소드)가\n+12V 쪽', ha='right', va='center',
        fontsize=8.4, color=RED, fontweight='bold', linespacing=1.5)

# MOSFET
nmos(XM, YM)
ax.text(XM+7.2, YM, 'IRLZ44N', ha='left', va='center', fontsize=10.5,
        color=INK, fontweight='bold')
ax.text(XM+7.2, YM-3.6, '로직레벨 필수', ha='left', va='center', fontsize=8.6,
        color=RED, fontweight='bold')

# 게이트 회로
GY = YM
w([(XG, GY), (XG+12.0, GY)])
res(XG+12.0, GY, '220 Ω')
w([(XG+23.0, GY), (XM-8.0, GY)])
ax.text(XG-2.0, GY, 'Nano  D9', ha='right', va='center', fontsize=10.5,
        color=DEEP, fontweight='bold')
# 풀다운
PDX = XM-14.0
dot((PDX, GY))
w([(PDX, GY), (PDX, GY-9.0)])
res(PDX, GY-20.0, '10 kΩ', horiz=False)
w([(PDX, GY-20.0), (PDX, GY-9.0)])
w([(PDX, GY-20.0), (PDX, 16.0)])

# 소스 → GND
w([(XM+5.0, YM-11.0), (XM+5.0, 16.0)])
# 공통 GND 레일
w([(PDX, 16.0), (108.0, 16.0)])
w([(X12, 16.0), (PDX, 16.0)])
dot((PDX, 16.0)); dot((XM+5.0, 16.0))
gnd((44.0, 16.0))
ax.text(X12-2.0, 16.0, 'GND', ha='right', va='center', fontsize=11,
        color=INK, fontweight='bold')
ax.text(108.0+2.0, 16.0, 'Nano GND 와 12V GND 를\n반드시 한 점에서 공통',
        ha='left', va='center', fontsize=9, color=RED, fontweight='bold',
        linespacing=1.5)

# 전류 경로 화살표
ax.annotate('', xy=(PX, PY+11.0), xytext=(PX, Y12-2.0),
            arrowprops=dict(arrowstyle='-|>', lw=1.6, color=RED,
                            mutation_scale=13), zorder=9)

ax.text(6.0, 88.0, 'MOSFET 펌프 구동 회로  —  1채널 상세', fontsize=17,
        color=INK, fontweight='bold', va='center')
ax.text(6.0, 84.0, '로우사이드 스위칭. 이 회로를 D9~D12 로 네 번 반복하면 됩니다.',
        fontsize=10, color=GREY, va='center')

# ══════════════════════════════════════════════════════════════
# 오른쪽 주석
# ══════════════════════════════════════════════════════════════
NX = 116.0
ax.text(NX, 78.0, '빠뜨리면 안 되는 것', fontsize=12.5, color=MID,
        fontweight='bold', va='center')
notes = [
    ('10 kΩ 풀다운이 핵심',
     '없으면 전원을 켜는 순간, 그리고 리셋 중에\n게이트가 공중에 떠서 펌프가 제멋대로\n돕니다. 물난리의 가장 흔한 원인입니다.', RED),
    ('220 Ω 게이트 저항',
     '게이트 용량을 충전할 때 순간 전류가\n아두이노 핀 한계를 넘지 않게 막습니다.', GREY),
    ('다이오드 방향',
     '밴드가 그려진 쪽(캐소드)이 +12V.\n거꾸로 달면 전원 투입 즉시 단락됩니다.', RED),
    ('GND 공통',
     '12V 전원의 −와 아두이노 GND 를 한 점에서\n묶지 않으면 게이트 전압 기준이 없어\n동작하지 않습니다.', RED),
]
y = 71.0
for t, b, c in notes:
    ax.add_patch(Circle((NX+1.3, y), 1.3, facecolor=c, edgecolor='none', zorder=5))
    ax.text(NX+1.3, y, '!', fontsize=8.6, color='white', ha='center',
            va='center', fontweight='bold', zorder=6)
    ax.text(NX+4.6, y+0.1, t, fontsize=10, color=INK, va='center',
            fontweight='bold')
    ax.text(NX+4.6, y-4.4, b, fontsize=8.6, color=GREY, va='center',
            linespacing=1.6)
    y -= 13.6

# ══════════════════════════════════════════════════════════════
# 하단 : 4채널 확장 + 모듈 경고
# ══════════════════════════════════════════════════════════════
ax.add_patch(FancyBboxPatch((6.0, 1.5), 68.0, 10.5,
    boxstyle='round,pad=0.15,rounding_size=0.7', facecolor='#F2F7FA',
    edgecolor='#D8E3EA', lw=1.0, zorder=3))
ax.text(9.0, 9.6, '4채널 확장 — 위 회로를 그대로 4벌', fontsize=10,
        color=MID, fontweight='bold', va='center', zorder=5)
chans = [('D9', 'Q1', '표준액'), ('D10', 'Q2', 'RO-DI'),
         ('D11', 'Q3', '수조물'), ('D12', 'Q4', '배수')]
x0 = 10.0
for pin, q, nm in chans:
    ax.text(x0, 6.2, f'{pin} → {q}', fontsize=9.6, color=DEEP,
            fontweight='bold', va='center', zorder=5)
    ax.text(x0, 3.4, nm, fontsize=8.6, color=GREY, va='center', zorder=5)
    x0 += 16.0

ax.add_patch(FancyBboxPatch((78.0, 1.5), 72.0, 10.5,
    boxstyle='round,pad=0.15,rounding_size=0.7', facecolor='#FBEDEC',
    edgecolor='#E2A9A4', lw=1.0, zorder=3))
ax.text(81.0, 9.6, '기성 모듈을 살 때 — IRF520 모듈은 피하십시오', fontsize=10,
        color=RED, fontweight='bold', va='center', zorder=5)
ax.text(81.0, 5.0,
        'IRF520 은 로직레벨이 아닙니다. 완전히 켜려면 게이트에 약 10 V 가 필요한데 아두이노는 5 V 도 못 미치는 전압을 냅니다.\n'
        '반쯤 켜진 상태로 발열하다 고장납니다.  →  IRLZ44N · IRL520 · IRLB8721 · D4184 모듈처럼 로직레벨을 고르십시오.',
        fontsize=8.8, color=INK, va='center', linespacing=1.7, zorder=5)

plt.savefig(figpath('fig_mosfet.png'), dpi=150, facecolor='white',
            bbox_inches='tight', pad_inches=0.15)
print('ok')
