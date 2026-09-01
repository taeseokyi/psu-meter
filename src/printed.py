# -*- coding: utf-8 -*-
"""3D 프린팅용 측정 헤드 — 분해도"""
import math
from kfont import DEEP, TEAL, MID, AMB, INK, GREY, figpath
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Wedge, Polygon
import numpy as np

INK='#1A2430'; GREY='#78899A'; DEEP='#065A82'; MID='#21295C'
AMB='#E8901F'; RED='#C0392B'; GRN='#1E8E3E'
SHELL='#3E4750'; SHELL2='#4C5761'; CHAN='#20262B'
GLASS='#D9E9F2'; GLASSE='#5F97B5'; GASKET='#C0392B'
PTFE='#EDEFF1'; ALU='#C8CDD2'; WATER='#BFE0EF'

fig, ax = plt.subplots(figsize=(15.8, 10.2), dpi=150)
ax.set_xlim(0, 158); ax.set_ylim(0, 102); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 158, 102, facecolor='white', zorder=0))

TC = 61.928; th = math.radians(TC)

def arrow_down(x, y0, y1, c='#9AA6B2'):
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle='-|>', lw=1.3, color=c, ls=(0,(3,2)),
                                mutation_scale=12), zorder=4)

def tag(x, y, n, t, s, col=AMB):
    ax.add_patch(Circle((x, y), 1.5, facecolor=col, edgecolor='none', zorder=9))
    ax.text(x, y, str(n), fontsize=8.8, color='white', ha='center',
            va='center', fontweight='bold', zorder=10)
    ax.text(x+3.4, y+0.9, t, fontsize=9.4, color=INK, va='center',
            fontweight='bold', zorder=9)
    ax.text(x+3.4, y-2.4, s, fontsize=8.2, color=GREY, va='center',
            zorder=9, linespacing=1.5)

# ══════════════════════════════════════════════════════════════
# 분해도  (왼쪽)
# ══════════════════════════════════════════════════════════════
CX = 32.0

# ── 1. 플로우셀 상판
ax.add_patch(FancyBboxPatch((CX-17, 82), 34, 10,
    boxstyle='round,pad=0.1,rounding_size=0.7', facecolor=PTFE,
    edgecolor='#BFC5CB', lw=1.5, zorder=6))
ax.add_patch(Rectangle((CX-11, 82), 22, 5.4, facecolor=WATER,
                       edgecolor='none', zorder=7))
ax.text(CX, 89.4, '플로우셀 상판', ha='center', va='center', fontsize=8.6,
        color='#4E5A64', fontweight='bold', zorder=8)
for dx_, c, lb in ((-14.5, DEEP, '주입'), (14.5, AMB, '배수')):
    ax.plot([CX+dx_*1.35, CX+dx_], [84.2, 84.2], color=c, lw=2.4, zorder=8,
            solid_capstyle='round')
ax.plot([CX+11, CX+19], [86.6, 86.6], color=GREY, lw=1.8, zorder=8,
        solid_capstyle='round')
arrow_down(CX, 81, 78.0)

# ── 2. 실리콘 가스켓
ax.add_patch(Rectangle((CX-15, 74.6), 30, 2.0, facecolor=GASKET,
                       edgecolor='#8E2B21', lw=1.0, zorder=6))
ax.add_patch(Rectangle((CX-9.5, 74.6), 19, 2.0, facecolor='white',
                       edgecolor='#8E2B21', lw=0.8, zorder=7))
ax.text(CX+17.5, 75.6, '실리콘 시트 1 mm  (가운데를 도려냄)', ha='left',
        va='center', fontsize=8.4, color=GASKET, fontweight='bold', zorder=8)
arrow_down(CX, 73.6, 70.5)

# ── 3. 프리즘
ax.add_patch(Wedge((CX, 68.9), 9.0, 180, 360, facecolor=GLASS,
                   edgecolor=GLASSE, lw=1.6, zorder=7))
ax.plot([CX-9, CX+9], [68.9, 68.9], color=MID, lw=2.2, zorder=8)
ax.text(CX+17.5, 66.5, 'BK7 반원통 (또는 직각/정삼각 프리즘)', ha='left',
        va='center', fontsize=8.4, color=DEEP, fontweight='bold', zorder=8)
arrow_down(CX, 59.4, 56.6)

# ── 4~5. 클램셸 두 짝 (광학면에서 좌우로 분할)
def shell(x0, y0, mirror=False):
    sgn = -1 if mirror else 1
    ax.add_patch(FancyBboxPatch((x0-15, y0-22), 30, 30,
        boxstyle='round,pad=0.1,rounding_size=1.0', facecolor=SHELL,
        edgecolor='#2A3239', lw=1.4, zorder=5))
    # 프리즘 시트
    ax.add_patch(Wedge((x0, y0+5.0), 9.6, 180, 360, facecolor=CHAN,
                       edgecolor='#171C21', lw=1.0, zorder=6))
    ax.plot([x0-11.5, x0+11.5], [y0+5.0, y0+5.0], color='#8A96A2', lw=1.6,
            zorder=7)
    # 반쪽 채널 두 개
    for s in (-1, 1):
        ex = x0 + s*14.5*math.sin(th)*1.42
        ey = y0 + 5.0 - 14.5*math.cos(th)*1.42
        dx_, dy_ = ex-x0, ey-(y0+5.0)
        n = math.hypot(dx_, dy_); px_, py_ = -dy_/n, dx_/n
        hw = 2.6
        ax.add_patch(Polygon([(x0+px_*hw, y0+5.0+py_*hw), (ex+px_*hw, ey+py_*hw),
                              (ex-px_*hw, ey-py_*hw), (x0-px_*hw, y0+5.0-py_*hw)],
                             closed=True, facecolor=CHAN, edgecolor='#171C21',
                             lw=0.8, zorder=6))
        for f in (0.42, 0.66, 0.88):
            bx, by = x0+dx_*f, y0+5.0+dy_*f
            ax.plot([bx+px_*hw, bx+px_*1.0], [by+py_*hw, by+py_*1.0],
                    color='#6E7A85', lw=1.8, zorder=7, solid_capstyle='butt')
            ax.plot([bx-px_*hw, bx-px_*1.0], [by-py_*hw, by-py_*1.0],
                    color='#6E7A85', lw=1.8, zorder=7, solid_capstyle='butt')
    # 볼트 보스
    for bx in (-12.0, 12.0):
        for by in (-18.0, 5.5):
            ax.add_patch(Circle((x0+bx, y0+by), 1.5, facecolor='#2A3239',
                                edgecolor='#1A1F24', lw=0.7, zorder=7))

shell(CX, 44.0)
ax.text(CX, 19.4, '하부 셸', ha='center', va='center',
        fontsize=9, color=INK, fontweight='bold', zorder=8)

# 상부 셸을 옆으로 벌려 배치
shell(CX+40, 44.0, mirror=True)
ax.text(CX+40, 19.4, '상부 셸 (거울상)', ha='center', va='center',
        fontsize=9, color=INK, fontweight='bold', zorder=8)
ax.annotate('', xy=(CX+18.5, 44.0), xytext=(CX+53.5, 44.0),
            arrowprops=dict(arrowstyle='-|>', lw=1.6, color='#9AA6B2',
                            ls=(0,(3,2)), mutation_scale=13), zorder=4)
ax.text(CX+20, 53.5, '맞물려 조립', ha='center', va='bottom', fontsize=8.4,
        color=GREY, zorder=5)

# ── 6. 알루미늄 열용량판
ax.add_patch(Rectangle((CX-15, 15.4), 30, 3.2, facecolor=ALU,
                       edgecolor='#A0A7AE', lw=1.2, zorder=6))
ax.text(CX+17.5, 17.0, '알루미늄 평판 (열용량체)', ha='left', va='center',
        fontsize=8.4, color='#4E5A64', fontweight='bold', zorder=8)
arrow_down(CX, 21.8, 19.2)

ax.text(6.0, 98.0, '3D 프린팅용 측정 헤드 — 분해도', fontsize=17.5, color=INK,
        fontweight='bold', va='center')
ax.text(6.0, 94.2,
        '알루미늄 절삭 대신 클램셸 2분할 출력. 정밀도가 필요한 곳은 작은 허브 한 곳뿐입니다.',
        fontsize=10, color=GREY, va='center')

# ══════════════════════════════════════════════════════════════
# 오른쪽 : 설계 요령
# ══════════════════════════════════════════════════════════════
NX = 104.0
ax.text(NX, 93.5, '3D 프린팅으로 바꾸면서 달라지는 것', fontsize=12.5,
        color=MID, fontweight='bold', va='center')
items = [
    (1, '광학면에서 좌우로 쪼개 출력',
     '경사진 구멍은 FDM 으로 못 뚫습니다. 광선이 지나는\n평면에서 두 쪽으로 갈라 반원 홈을 각각 출력하면\n서포트 없이 매끈한 채널이 나옵니다.'),
    (2, '긴 팔은 출력하지 말고 파이프로',
     '250 mm 를 출력하면 휩니다. 허브에서 각도만 잡고\n검은 PVC · 알루미늄 파이프를 끼우십시오.\n검출기 마운트는 슬라이드식으로 만들어 조정합니다.'),
    (3, 'O-링 홈 대신 실리콘 시트',
     'FDM 으로 O-링 홈은 정밀도가 안 나옵니다. 1 mm\n실리콘 시트를 가위로 오려 평면 가스켓으로 쓰고\n볼트로 눌러 밀봉하는 편이 훨씬 잘 됩니다.'),
    (4, '열용량은 알루미늄 평판으로 보충',
     '플라스틱은 열전도가 알루미늄의 1/1000 이라 온도를\n고르게 못 만듭니다. 철물점 알루미늄 평판을\n셀 밑에 대고 전체를 단열재로 감싸십시오.'),
    (5, '온도 보정을 코드로 처리',
     'DS18B20 은 절대 정확도가 나빠도 됩니다. 표준액과\n시료를 같은 센서로 재니 차이만 정확하면 되고,\n0.0625 °C 분해능이면 0.042 PSU 수준입니다.'),
]
y = 86.0
for n, t, b in items:
    tag(NX, y, n, t, '')
    ax.text(NX+3.4, y-4.6, b, fontsize=8.4, color=GREY, va='center',
            linespacing=1.65, zorder=9)
    y -= 13.6

# ══════════════════════════════════════════════════════════════
# 하단 : 출력 설정
# ══════════════════════════════════════════════════════════════
ax.add_patch(FancyBboxPatch((6.0, 2.0), 94.0, 12.0,
    boxstyle='round,pad=0.15,rounding_size=0.7', facecolor='#F2F7FA',
    edgecolor='#D8E3EA', lw=1.0, zorder=3))
ax.text(9.5, 11.6, '출력 설정 — 이대로 하시면 됩니다', fontsize=10.4,
        color=MID, fontweight='bold', va='center', zorder=5)
specs = [('소재', 'PETG 또는 ASA', 'PLA 는 부적합'),
         ('색상', '검정', '얇으면 빛이 샙니다'),
         ('벽 두께', '≥ 2.5 mm', '외벽 4~5 라인'),
         ('채움', '40 % 이상', '허브는 60 %'),
         ('후처리', '내부 무광 검정 도장', '검은 필라멘트도 반사합니다')]
x0 = 10.0
for k, v, s in specs:
    ax.text(x0, 8.2, k, fontsize=8.2, color=GREY, va='center', zorder=5)
    ax.text(x0, 5.6, v, fontsize=10, color=DEEP, fontweight='bold',
            va='center', zorder=5)
    ax.text(x0, 3.2, s, fontsize=7.4, color=GREY, va='center', zorder=5)
    x0 += 17.8

# 방수 경고
ax.add_patch(FancyBboxPatch((104.0, 2.0), 48.0, 12.0,
    boxstyle='round,pad=0.15,rounding_size=0.7', facecolor='#FBEDEC',
    edgecolor='#E2A9A4', lw=1.0, zorder=3))
ax.text(106.5, 11.6, '젖는 부분은 출력물을 믿지 마십시오', fontsize=9.4,
        color=RED, fontweight='bold', va='center', zorder=5)
ax.text(106.5, 6.4,
        'FDM 은 레이어 사이로 물이 스밉니다. 플로우셀 상판만은\n'
        'PTFE 블록에 구멍을 뚫거나, SLA(레진) 출력 또는\n'
        '내부 에폭시 코팅으로 처리하십시오.',
        fontsize=8.2, color=INK, va='center', linespacing=1.6, zorder=5)

plt.savefig(figpath('fig_printed.png'), dpi=150, facecolor='white',
            bbox_inches='tight', pad_inches=0.15)
print('ok')
