# -*- coding: utf-8 -*-
import math
"""Fritzing 스타일 브레드보드 배선도 생성"""
exec(open('/home/claude/salinity/kfont.py').read())
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, PathPatch, Polygon
from matplotlib.path import Path
import numpy as np

# ── Fritzing 팔레트 ────────────────────────────────────────────
BB_BODY  = '#F2EEE3'; BB_EDGE = '#D6CFBE'; HOLE = '#8E8878'
RED_RAIL = '#D64541'; BLU_RAIL = '#4A7EBB'
PCB_NANO = '#1F3A5F'; PCB_BT = '#1E5A8E'; PCB_CCD = '#14415C'
PCB_RTC  = '#2F6F4E'; PCB_MOS = '#0B6E4F'; PCB_DRV = '#7A2E2E'
HDR      = '#232323'; GOLD = '#D9B441'; SILVER = '#B9BEC4'
W_RED='#D93025'; W_BLK='#202124'; W_YEL='#F2A900'; W_GRN='#1E8E3E'
W_BLU='#1A73E8'; W_ORG='#E8710A'; W_WHT='#DDE1E6'; W_PUR='#8430CE'; W_CYN='#12A5B8'
INK2='#1A2430'; GREY2='#6E7C8A'

fig, ax = plt.subplots(figsize=(16.2, 11.4), dpi=150)
ax.set_xlim(0, 162); ax.set_ylim(0, 114); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((0, 0), 162, 114, facecolor='white', zorder=0))


def shadow(x, y, w, h, r=0.6, z=1):
    ax.add_patch(FancyBboxPatch((x+0.35, y-0.42), w, h,
        boxstyle=f'round,pad=0.02,rounding_size={r}', facecolor='#00000018',
        edgecolor='none', zorder=z))


def board(x, y, w, h, color, label, sub=None, fs=8.6, r=0.55, z=6, tc='white'):
    shadow(x, y, w, h, r, z-1)
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f'round,pad=0.02,rounding_size={r}', facecolor=color,
        edgecolor='#00000055', lw=0.8, zorder=z))
    ax.text(x+w/2, y+h-1.15, label, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', zorder=z+2)
    if sub:
        ax.text(x+w/2, y+h-2.55, sub, ha='center', va='center', fontsize=fs-2.1,
                color='#C9D8E4', zorder=z+2)


def header(x, y, n, horiz=True, pitch=1.0, z=8):
    """검은 핀헤더 + 금색 핀"""
    if horiz:
        ax.add_patch(Rectangle((x-0.42, y-0.42), n*pitch, 0.84, facecolor=HDR,
                               edgecolor='none', zorder=z))
        for i in range(n):
            ax.add_patch(Circle((x+i*pitch, y), 0.2, facecolor=GOLD,
                                edgecolor='none', zorder=z+1))
    else:
        ax.add_patch(Rectangle((x-0.42, y-0.42), 0.84, n*pitch, facecolor=HDR,
                               edgecolor='none', zorder=z))
        for i in range(n):
            ax.add_patch(Circle((x, y+i*pitch), 0.2, facecolor=GOLD,
                                edgecolor='none', zorder=z+1))


def wire(p0, p1, color, bow=0.30, lw=2.6, z=20, dash=None):
    """Fritzing 풍 곡선 점퍼선"""
    x0, y0 = p0; x1, y1 = p1
    dx, dy = x1-x0, y1-y0
    L = math.hypot(dx, dy) or 1
    mx, my = (x0+x1)/2 - dy/L*L*bow*0.5, (y0+y1)/2 + dx/L*L*bow*0.5
    pth = Path([(x0, y0), (mx, my), (x1, y1)],
               [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(PathPatch(pth, fill=False, edgecolor='#00000022', lw=lw+1.6,
                           capstyle='round', zorder=z-1))
    ax.add_patch(PathPatch(pth, fill=False, edgecolor=color, lw=lw,
                           capstyle='round', zorder=z,
                           linestyle=dash if dash else 'solid'))
    for p in (p0, p1):
        ax.add_patch(Circle(p, 0.34, facecolor=color, edgecolor='#00000055',
                            lw=0.5, zorder=z+1))


def resistor(x, y, bands, label, horiz=True, z=12):
    """축방향 저항 (컬러밴드)"""
    Lw, Lh = (5.2, 1.5) if horiz else (1.5, 5.2)
    ax.plot([x-1.6, x+Lw+1.6] if horiz else [x+0.75]*2,
            [y+0.75]*2 if horiz else [y-1.6, y+Lh+1.6],
            color='#9AA0A6', lw=1.5, zorder=z-1, solid_capstyle='round')
    ax.add_patch(FancyBboxPatch((x, y), Lw, Lh,
        boxstyle='round,pad=0.02,rounding_size=0.5', facecolor='#D9C9A3',
        edgecolor='#8A7A55', lw=0.7, zorder=z))
    for i, c in enumerate(bands):
        bx = x + 0.85 + i*0.95
        ax.add_patch(Rectangle((bx, y+0.06), 0.42, Lh-0.12, facecolor=c,
                               edgecolor='none', zorder=z+1))
    ax.text(x+Lw/2, y+Lh+0.95, label, ha='center', va='bottom', fontsize=7.6,
            color=INK2, fontweight='bold', zorder=z+2)


# ══════════════════════════════════════════════════════════════
# 브레드보드
# ══════════════════════════════════════════════════════════════
BX, BY, BW, BH = 25.0, 36.0, 96.0, 34.0
shadow(BX, BY, BW, BH, 1.0, 2)
ax.add_patch(FancyBboxPatch((BX, BY), BW, BH,
    boxstyle='round,pad=0.02,rounding_size=1.0', facecolor=BB_BODY,
    edgecolor=BB_EDGE, lw=1.4, zorder=3))

NC = 46                      # 컬럼 수
CX0 = BX + 4.0               # 첫 컬럼 x
CP  = (BW - 8.0) / (NC - 1)  # 컬럼 피치


def col_x(i): return CX0 + i * CP


def rail(y, color, sign):
    ax.plot([BX+3.0, BX+BW-3.0], [y+2.3, y+2.3], color=color, lw=1.0,
            zorder=4, alpha=.9)
    ax.text(BX+1.6, y+1.15, sign, fontsize=7.5, color=color, ha='center',
            va='center', fontweight='bold', zorder=5)
    for i in range(0, NC):
        if i % 6 == 5:
            continue
        ax.add_patch(Circle((col_x(i), y+1.15), 0.30, facecolor=HOLE,
                            edgecolor='none', zorder=4, alpha=.55))


# 상단 레일 (+ / -)
rail(BY+BH-3.4, RED_RAIL, '+')
rail(BY+BH-6.0, BLU_RAIL, '−')
# 하단 레일
rail(BY+3.4, RED_RAIL, '+')
rail(BY+0.8, BLU_RAIL, '−')

# 메인 홀 영역 (위 5행 / 아래 5행)
ROW_TOP = [BY+BH-8.6-1.55*k for k in range(5)]     # a~e (위 뱅크)
ROW_BOT = [BY+6.2+1.55*k for k in range(5)]        # f~j (아래 뱅크)
for ys in (ROW_TOP, ROW_BOT):
    for y in ys:
        for i in range(NC):
            ax.add_patch(Circle((col_x(i), y), 0.30, facecolor=HOLE,
                                edgecolor='none', zorder=4, alpha=.55))
# 중앙 채널
ax.add_patch(Rectangle((BX+2.4, BY+13.4), BW-4.8, 2.0, facecolor='#E4DECF',
                       edgecolor='#D2CBB8', lw=0.6, zorder=4))

ax.text(BX+BW/2, BY+BH+1.6, '브레드보드 (830 타이포인트)', ha='center',
        va='bottom', fontsize=9, color=GREY2, zorder=6)

# ══════════════════════════════════════════════════════════════
# Arduino Nano  (브레드보드 중앙 채널에 걸침)
# ══════════════════════════════════════════════════════════════
NX, NY, NW_, NH_ = col_x(4)-1.4, BY+11.0, 24.0, 7.4
board(NX, NY, NW_, NH_, PCB_NANO, '', z=10)
ax.text(NX+NW_/2, NY+NH_/2+0.5, 'Arduino  NANO', ha='center', va='center',
        fontsize=9.2, color='white', fontweight='bold', zorder=13)
ax.text(NX+NW_/2, NY+NH_/2-1.35, 'ATmega328P · 5V', ha='center', va='center',
        fontsize=6.8, color='#9FC4D8', zorder=13)
# USB 커넥터
ax.add_patch(Rectangle((NX-1.5, NY+NH_/2-1.5), 1.9, 3.0, facecolor=SILVER,
                       edgecolor='#8B9096', lw=0.6, zorder=13))
# 핀헤더 (상/하)
header(col_x(4), NY+NH_+0.25, 15, horiz=True, pitch=CP, z=14)
header(col_x(4), NY-0.25, 15, horiz=True, pitch=CP, z=14)

# 나노 핀 라벨 (사용하는 것만)
TOP_PINS = {5:'D2', 6:'D3', 7:'D4', 8:'D5', 9:'D6', 10:'D7', 11:'D8'}
BOT_PINS = {5:'D9', 6:'D10', 7:'D11', 8:'D12', 12:'A0', 14:'A4', 15:'A5'}
for i, nm in TOP_PINS.items():
    ax.text(col_x(i), NY+NH_+2.1, nm, ha='center', va='bottom', fontsize=6.4,
            color=INK2, fontweight='bold', zorder=15, rotation=90)
for i, nm in BOT_PINS.items():
    ax.text(col_x(i), NY-2.1, nm, ha='center', va='top', fontsize=6.4,
            color=INK2, fontweight='bold', zorder=15, rotation=90)

TOPROW = ROW_TOP[-1]      # 나노 위쪽 배선용 행
BOTROW = ROW_BOT[0]       # 나노 아래쪽 배선용 행
VCC_T  = BY+BH-3.4+1.15   # 상단 + 레일 y
GND_T  = BY+BH-6.0+1.15   # 상단 − 레일 y
VCC_B  = BY+3.4+1.15
GND_B  = BY+0.8+1.15

# 나노 5V / GND → 레일
wire((col_x(19), NY+NH_+0.25), (col_x(21), VCC_T), W_RED, bow=0.18)
wire((col_x(18), NY+NH_+0.25), (col_x(16), GND_T), W_BLK, bow=-0.18)
# 레일 간 브릿지
wire((col_x(43), VCC_T), (col_x(43), VCC_B), W_RED, bow=0.05, lw=2.2)
wire((col_x(44), GND_T), (col_x(44), GND_B), W_BLK, bow=0.05, lw=2.2)

# ══════════════════════════════════════════════════════════════
# 주변 모듈
# ══════════════════════════════════════════════════════════════
# TSL1401 (좌상단)
T_X, T_Y, T_W, T_H = 6.0, 84.0, 30.0, 12.0
board(T_X, T_Y, T_W, T_H, PCB_CCD, 'TSL1401CL  리니어 CCD',
      '128 px × 63.5 µm', fs=9)
ax.add_patch(Rectangle((T_X+4, T_Y+2.2), T_W-8, 2.6, facecolor='#0B0B0B',
                       edgecolor='#3A3A3A', lw=0.6, zorder=8))
ax.text(T_X+T_W/2, T_Y+3.5, '─ 감광 어레이 ─', ha='center', va='center',
        fontsize=6.4, color='#6C7A85', zorder=9)
header(T_X+4.2, T_Y-0.3, 5, pitch=4.4, z=9)
for i, nm in enumerate(['VCC', 'GND', 'AO', 'SI', 'CLK']):
    ax.text(T_X+4.2+i*4.4, T_Y-1.6, nm, ha='center', va='top', fontsize=6.2,
            color=INK2, fontweight='bold', zorder=10)

# HC-06 (우상단)
H_X, H_Y, H_W, H_H = 118.0, 84.0, 26.0, 12.0
board(H_X, H_Y, H_W, H_H, PCB_BT, 'HC-06  (ZS-040)', '블루투스 슬레이브', fs=9)
ax.add_patch(Rectangle((H_X+3, H_Y+2.4), 9, 3.0, facecolor='#111', zorder=8))
ax.text(H_X+7.5, H_Y+3.9, 'BT', ha='center', va='center', fontsize=6.4,
        color='#7FB2D4', zorder=9)
header(H_X+5.0, H_Y-0.3, 4, pitch=4.2, z=9)
for i, nm in enumerate(['VCC', 'GND', 'TXD', 'RXD']):
    ax.text(H_X+5.0+i*4.2, H_Y-1.5, nm, ha='center', va='top', fontsize=6.2,
            color=INK2, fontweight='bold', zorder=10)

# DS3231 RTC (우측)
R_X, R_Y, R_W, R_H = 128.0, 60.0, 22.0, 9.0
board(R_X, R_Y, R_W, R_H, PCB_RTC, 'DS3231  RTC', '1일 2회 정시 실행', fs=8.6)
header(R_X+4.0, R_Y-0.3, 4, pitch=3.6, z=9)
for i, nm in enumerate(['VCC', 'GND', 'SDA', 'SCL']):
    ax.text(R_X+4.0+i*3.6, R_Y-1.5, nm, ha='center', va='top', fontsize=6.2,
            color=INK2, fontweight='bold', zorder=10)

# DS18B20 (좌측, 케이블형)
D_X, D_Y = 6.0, 60.0
ax.add_patch(FancyBboxPatch((D_X, D_Y), 9.0, 3.4,
    boxstyle='round,pad=0.02,rounding_size=1.4', facecolor='#8C9299',
    edgecolor='#6A7076', lw=0.8, zorder=7))
ax.text(D_X+4.5, D_Y+1.7, 'DS18B20', ha='center', va='center', fontsize=7,
        color='white', fontweight='bold', zorder=9)
ax.text(D_X+4.5, D_Y+4.6, '방수형 온도센서', ha='center', va='bottom',
        fontsize=7.4, color=INK2, fontweight='bold', zorder=9)
ax.text(D_X+4.5, D_Y-1.2, '셀 유로 내부', ha='center', va='top', fontsize=6.6,
        color=GREY2, zorder=9)

# 측정 LED (브레드보드 위)
LED_C = col_x(30)
ax.add_patch(Circle((LED_C, TOPROW+4.6), 1.5, facecolor='#F5B324',
                    edgecolor='#B8811A', lw=0.9, zorder=12))
ax.add_patch(Circle((LED_C-0.5, TOPROW+5.1), 0.5, facecolor='#FFE9A8',
                    edgecolor='none', zorder=13))
ax.plot([LED_C-0.55, LED_C-0.55], [TOPROW+3.2, TOPROW], color='#9AA0A6',
        lw=1.4, zorder=11, solid_capstyle='round')
ax.plot([LED_C+0.55, LED_C+0.55], [TOPROW+3.2, TOPROW], color='#9AA0A6',
        lw=1.4, zorder=11, solid_capstyle='round')
ax.text(LED_C, TOPROW+6.6, '측정 LED  590nm', ha='center', va='bottom',
        fontsize=7.4, color=INK2, fontweight='bold', zorder=13)

# 저항: HC-06 분압기 1k / 2k, DS18B20 풀업 4.7k
BR, RD, OR_, YL, VI, GY = '#7A4A1E', '#C0392B', '#E8710A', '#F1C40F', '#8E44AD', '#95A5A6'
resistor(col_x(35)-1.0, TOPROW+3.0, [BR, W_BLK, RD, GY], '1 kΩ')
resistor(col_x(40)-1.0, TOPROW+3.0, [RD, W_BLK, RD, GY], '2 kΩ')
resistor(col_x(24)-1.0, BOTROW-6.6, [YL, VI, RD, GY], '4.7 kΩ')

# ── 배선 : TSL1401 ────────────────────────────────────────────
wire((T_X+4.2,  T_Y-0.3), (col_x(0), VCC_T), W_RED, bow=-0.16)         # VCC
wire((T_X+8.6,  T_Y-0.3), (col_x(1), GND_T), W_BLK, bow=-0.13)         # GND
wire((T_X+13.0, T_Y-0.3), (col_x(12), BOTROW), W_CYN, bow=-0.24)       # AO  → A0
wire((T_X+17.4, T_Y-0.3), (col_x(6), TOPROW), W_GRN, bow=-0.15)        # SI  → D3
wire((T_X+21.8, T_Y-0.3), (col_x(7), TOPROW), W_YEL, bow=-0.09)        # CLK → D4

# ── 배선 : HC-06 ─────────────────────────────────────────────
wire((H_X+5.0, H_Y-0.3), (col_x(45), VCC_T), W_RED, bow=0.16)          # VCC
wire((H_X+9.2, H_Y-0.3), (col_x(44), GND_T), W_BLK, bow=0.13)          # GND
wire((H_X+13.4, H_Y-0.3), (col_x(10), TOPROW), W_ORG, bow=0.16)        # TXD → D7
wire((H_X+17.6, H_Y-0.3), (col_x(40)+3.2, TOPROW+3.75), W_PUR, bow=0.14)  # RXD ← 분압기 중점
# 분압기 결선
wire((col_x(11), TOPROW), (col_x(35)-1.0, TOPROW+3.75), W_PUR, bow=-0.12)   # D8 → 1k
wire((col_x(35)+4.2, TOPROW+3.75), (col_x(40)-1.0, TOPROW+3.75), W_PUR, bow=0.10)
wire((col_x(40)+4.2, TOPROW+3.75), (col_x(42), GND_T), W_BLK, bow=0.16)     # 2k → GND

# ── 배선 : DS18B20 / DS3231 / LED ────────────────────────────
wire((D_X+9.0, D_Y+2.6), (col_x(2), VCC_T), W_RED, bow=0.22)
wire((D_X+9.0, D_Y+1.7), (col_x(3), GND_T), W_BLK, bow=0.15)
wire((D_X+9.0, D_Y+0.8), (col_x(5), TOPROW), W_WHT, bow=-0.16)              # DATA → D2
wire((col_x(24)+4.2, BOTROW-5.85), (col_x(5), TOPROW), W_RED, bow=0.30, lw=2.0)
wire((col_x(24)-1.0, BOTROW-5.85), (col_x(26), VCC_B), W_RED, bow=-0.14, lw=2.0)

wire((R_X+4.0, R_Y-0.3), (col_x(45), VCC_B), W_RED, bow=0.20)
wire((R_X+7.6, R_Y-0.3), (col_x(44), GND_B), W_BLK, bow=0.17)
wire((R_X+11.2, R_Y-0.3), (col_x(14), BOTROW), W_BLU, bow=0.24)             # SDA → A4
wire((R_X+14.8, R_Y-0.3), (col_x(15), BOTROW), W_GRN, bow=0.20)             # SCL → A5

resistor(col_x(26)-1.0, TOPROW+3.0, [RD, RD, BR, GY], '220 Ω')
wire((col_x(8), TOPROW), (col_x(26)-1.0, TOPROW+3.75), W_YEL, bow=-0.12)   # D5 → 220Ω
wire((col_x(26)+4.2, TOPROW+3.75), (LED_C-0.55, TOPROW+3.2), W_YEL, bow=0.08)
wire((LED_C+0.55, TOPROW), (col_x(33), GND_T), W_BLK, bow=0.12)

# ══════════════════════════════════════════════════════════════
# 전력부 : MOSFET 4채널 + 펌프 + 12V
# ══════════════════════════════════════════════════════════════
M_X, M_Y, M_W, M_H = 32.0, 12.0, 46.0, 13.0
board(M_X, M_Y, M_W, M_H, PCB_MOS, 'MOSFET 4채널 드라이버  (IRLZ44N ×4)',
      '각 채널에 플라이백 다이오드 1N4007', fs=9)
for i in range(4):
    fx = M_X + 5.0 + i*10.5
    ax.add_patch(Rectangle((fx, M_Y+2.6), 4.2, 5.4, facecolor='#1A1A1A',
                           edgecolor='#3A3A3A', lw=0.6, zorder=8))
    ax.add_patch(Rectangle((fx+0.6, M_Y+7.2), 3.0, 1.2, facecolor=SILVER,
                           edgecolor='none', zorder=9))
    ax.text(fx+2.1, M_Y+5.2, f'Q{i+1}', ha='center', va='center', fontsize=6.4,
            color='#9AA6B2', zorder=10, rotation=90)
header(M_X+6.0, M_Y-0.3, 4, pitch=10.5, z=9)
for i in range(4):
    ax.text(M_X+6.0+i*10.5, M_Y-1.5, f'IN{i+1}', ha='center', va='top',
            fontsize=6.4, color=INK2, fontweight='bold', zorder=10)

# 펌프 4개
for i in range(4):
    px = 86.0 + i*17.0
    py = 13.0
    ax.add_patch(Circle((px+5.5, py+5.5), 5.2, facecolor='#4A5560',
                        edgecolor='#2E363E', lw=1.0, zorder=7))
    ax.add_patch(Circle((px+5.5, py+5.5), 3.0, facecolor='#8C939B',
                        edgecolor='#5C646C', lw=0.8, zorder=8))
    ax.add_patch(Circle((px+5.5, py+5.5), 1.1, facecolor='#2E363E', zorder=9))
    ax.text(px+5.5, py-1.4, f'P{i+1}', ha='center', va='top', fontsize=8,
            color=INK2, fontweight='bold', zorder=9)
    lbl = ['표준액', 'RO-DI', '수조물', '배수'][i]
    ax.text(px+5.5, py-3.6, lbl, ha='center', va='top', fontsize=6.8,
            color=GREY2, zorder=9)
    oy = M_Y + M_H - 2.6 - i*2.6
    ax.add_patch(Rectangle((M_X+M_W-2.2, oy-0.55), 2.2, 1.1, facecolor='#1A1A1A',
                           edgecolor='none', zorder=8))
    wire((M_X+M_W, oy), (px+1.0, py+6.8), W_RED, bow=0.02, lw=2.2)
    wire((M_X+M_W, oy-1.05), (px+1.0, py+4.2), W_BLK, bow=0.02, lw=2.2)

ax.text(86.0, 26.5, '페리스탈틱 펌프  ×4   (12 V)', fontsize=9, color=INK2,
        fontweight='bold', zorder=9)

# 12V 전원
S_X, S_Y = 6.0, 12.0
board(S_X, S_Y, 20.0, 13.0, PCB_DRV, '12 V  전원', 'SMPS 2 A 이상', fs=9)
ax.text(S_X+10.0, S_Y+3.2, '＋      －', ha='center', va='center', fontsize=9,
        color='white', fontweight='bold', zorder=9)
wire((S_X+20.0, S_Y+7.0), (M_X, M_Y+9.0), W_RED, bow=0.10, lw=3.0)
wire((S_X+20.0, S_Y+4.0), (M_X, M_Y+5.0), W_BLK, bow=-0.10, lw=3.0)

# D9~D12 → MOSFET IN
for i, c in enumerate([W_GRN, W_BLU, W_PUR, W_CYN]):
    wire((col_x(5+i), BOTROW), (M_X+6.0+i*10.5, M_Y+M_H+0.3), c, bow=0.12, lw=2.3)
# 로직 GND 공통
wire((col_x(20), GND_B), (M_X+M_W-3.0, M_Y+M_H+0.3), W_BLK, bow=-0.14, lw=2.3)

# UVC LED
U_X, U_Y = 128.0, 40.0
ax.add_patch(FancyBboxPatch((U_X, U_Y), 16.0, 8.0,
    boxstyle='round,pad=0.02,rounding_size=0.5', facecolor='#4A2E6B',
    edgecolor='#00000055', lw=0.8, zorder=6))
ax.text(U_X+8.0, U_Y+5.6, 'UVC LED', ha='center', va='center', fontsize=8.6,
        color='white', fontweight='bold', zorder=8)
ax.text(U_X+8.0, U_Y+3.6, '265 nm · MOSFET 구동', ha='center', va='center',
        fontsize=6.4, color='#C9B6E0', zorder=8)
ax.add_patch(Circle((U_X+8.0, U_Y+1.6), 1.0, facecolor='#B98CE8',
                    edgecolor='#7B4FA8', lw=0.8, zorder=8))
wire((U_X+2.0, U_Y), (col_x(9), TOPROW), W_PUR, bow=0.30, lw=2.3)
wire((U_X+14.0, U_Y), (col_x(45), GND_B), W_BLK, bow=-0.22, lw=2.2)

# ══════════════════════════════════════════════════════════════
# 제목 · 범례
# ══════════════════════════════════════════════════════════════
ax.text(6.0, 110.0, '해수 염도계  —  배선도', fontsize=21, color=INK2,
        fontweight='bold', va='center')
ax.text(6.0, 105.6, 'Arduino Nano 기준 · 브레드보드 배선 · 신호부와 전력부 전원 분리',
        fontsize=10.5, color=GREY2, va='center')

LG = [(W_RED, '5 V / 12 V'), (W_BLK, 'GND'), (W_GRN, 'D3 · A5 · D9'),
      (W_YEL, 'D4 · D5'), (W_ORG, 'D7'), (W_PUR, 'D8 · D6 · D11'),
      (W_BLU, 'A4 · D10'), (W_CYN, 'A0 · D12'), (W_WHT, 'D2 (1-Wire)')]
lx = 62.0
for i, (c, t) in enumerate(LG):
    cx = lx + (i % 5) * 20.0
    cy = 108.6 - (i // 5) * 3.4
    ax.plot([cx, cx+3.4], [cy, cy], color=c, lw=3.0, solid_capstyle='round',
            zorder=9)
    ax.text(cx+4.4, cy, t, fontsize=8.4, color=INK2, va='center', zorder=9)

# 주의 박스
ax.add_patch(FancyBboxPatch((6.0, 1.5), 150.0, 4.6,
    boxstyle='round,pad=0.02,rounding_size=0.5', facecolor='#FDF4E8',
    edgecolor='#E8B871', lw=1.0, zorder=5))
ax.text(8.0, 3.8, '주의', fontsize=8.6, color='#8A5A15', fontweight='bold',
        va='center', zorder=7)
ax.text(14.0, 3.8,
        'HC-06 RXD 는 5V 내성이 없어 1kΩ/2kΩ 분압기 필수  ·  펌프 12V 와 로직 5V 는 전원 분리하되 GND 는 공통  ·  '
        '모터마다 플라이백 다이오드 없으면 역기전력이 MCU 를 리셋',
        fontsize=8.6, color=INK2, va='center', zorder=7)

plt.savefig('/home/claude/salinity/fig_breadboard.png', dpi=150,
            facecolor='white', bbox_inches='tight', pad_inches=0.15)
print('ok')
