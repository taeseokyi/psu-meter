exec(open('/home/claude/salinity/kfont.py').read())
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig,ax=plt.subplots(figsize=(12.6,6.6),dpi=200)

# --- Arduino Nano ---
NX,NY,NW,NH=5.05,0.75,2.05,4.85
ax.add_patch(FancyBboxPatch((NX,NY),NW,NH,boxstyle='round,pad=0.03,rounding_size=0.10',
    facecolor='#1F3A4D',edgecolor=MID,lw=2,zorder=5))
ax.text(NX+NW/2,NY+NH-0.28,'Arduino\nNano',fontsize=13,color='white',ha='center',va='center',
        fontweight='bold',linespacing=1.4,zorder=7)
ax.text(NX+NW/2,NY+0.22,'5V · GND\n(로직)',fontsize=8.6,color='#9FC4D8',ha='center',va='center',linespacing=1.4,zorder=7)

def pin(y,name,side):
    x=NX+0.13 if side=='L' else NX+NW-0.13
    ha='left' if side=='L' else 'right'
    ax.text(x,y,name,fontsize=9.0,color='#CFE7F2',ha=ha,va='center',fontweight='bold',zorder=7)
    xt=NX if side=='L' else NX+NW
    ax.plot([xt-0.10 if side=='L' else xt, xt if side=='L' else xt+0.10],[y,y],color='#7FA8BF',lw=1.6,zorder=6)

def mod(x,y,w,h,title,lines,col,anchor_side):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.025,rounding_size=0.08',
        facecolor='white',edgecolor=col,lw=1.9,zorder=5))
    ax.text(x+0.16,y+h-0.24,title,fontsize=10.2,color=col,ha='left',va='center',fontweight='bold',zorder=6)
    yy=y+h-0.56
    for t in lines:
        ax.text(x+0.16,yy,t,fontsize=8.9,color=INK,ha='left',va='center',zorder=6)
        yy-=0.245
    return (x+w,y+h/2) if anchor_side=='R' else (x,y+h/2)

def wire(p,y,col,side):
    xt=NX if side=='L' else NX+NW
    ax.annotate('',xy=(xt-0.10 if side=='L' else xt+0.10,y),xytext=p,
        arrowprops=dict(arrowstyle='-',lw=1.5,color=col,connectionstyle='arc3,rad=0.0'),zorder=4)

# LEFT
p=mod(0.25,4.06,3.15,1.42,'TSL1401CL  리니어 어레이',['SI  → D3      CLK → D4','AO  → A0  (아날로그)','VCC 5V · GND','적분시간 = SI 펄스 간격'],DEEP,'R')
pin(4.90,'D3 / D4','L'); pin(4.62,'A0','L'); wire(p,4.76,DEEP,'L')
p=mod(0.25,2.88,3.15,0.94,'DS18B20  온도센서',['DATA → D2   (OneWire)','4.7 kΩ 풀업 → 5V'],TEAL,'R')
pin(3.55,'D2','L'); wire(p,3.55,TEAL,'L')
p=mod(0.25,1.70,3.15,0.94,'DS3231  RTC',['SDA → A4     SCL → A5','1일 2회 정시 실행'],TEAL,'R')
pin(2.35,'A4 / A5','L'); wire(p,2.35,TEAL,'L')
p=mod(0.25,0.62,3.15,0.84,'누수 감지  (옵션)',['A1  —  플로트/전극'],GREY,'R')
pin(1.30,'A1','L'); wire(p,1.30,GREY,'L')

# RIGHT
p=mod(8.75,4.34,3.55,1.24,'HC-06  블루투스 슬레이브',['TXD → D7   (직결 가능)','RXD ← D8   1k/2k 분압기 필수','VCC 5V  (3.6~6V 필요)'],AMB,'L')
pin(4.96,'D7 / D8','R'); wire(p,4.96,AMB,'R')
ax.add_patch(FancyBboxPatch((8.75,3.62),3.55,0.60,boxstyle='round,pad=0.02,rounding_size=0.06',
    facecolor='#FDF1E0',edgecolor=AMB,lw=1.4,ls='--',zorder=5))
ax.text(8.91,3.92,'D8 ─1kΩ─┬─ HC-06 RXD          Nano TX 5V →',fontsize=8.6,color='#8A5A15',va='center',zorder=6)
ax.text(8.91,3.74,'                    └─2kΩ─ GND          3.3V로 강하',fontsize=8.6,color='#8A5A15',va='center',zorder=6)

p=mod(8.75,2.62,3.55,0.90,'측정 LED  590 nm',['D5 → 정전류 드라이버','스펙트럼 폭 20 nm 이하'],AMB,'L')
pin(3.90,'D5','R'); wire(p,3.90,AMB,'R')
p=mod(8.75,1.62,3.55,0.90,'UVC LED  265 nm',['D6 → MOSFET','유휴 시 간헐 살균'],'#7B4FA8','L')
pin(3.05,'D6','R'); wire(p,3.05,'#7B4FA8','R')
p=mod(8.75,0.40,3.55,1.12,'페리스탈틱 펌프 P1~P4',['D9 D10 D11 D12 → MOSFET ×4','12 V 별도 전원','모터마다 플라이백 다이오드 필수'],MID,'L')
pin(1.90,'D9~D12','R'); wire(p,1.90,MID,'R')

ax.text(0.25,6.16,'아두이노 나노 배선  —  핀 배치',fontsize=14.5,color=MID,fontweight='bold',va='center')
ax.text(0.25,5.80,'SoftwareSerial 은 송신 중 인터럽트를 막으므로, TSL1401 프레임을 읽는 동안에는 블루투스 통신을 하지 않도록 순차 처리합니다.',
        fontsize=9.4,color=GREY,va='center')
ax.set_xlim(0,12.55); ax.set_ylim(0.25,6.40); ax.axis('off')
plt.savefig('fig_wiring.png',dpi=200,facecolor='white',bbox_inches='tight',pad_inches=0.14)
print('ok')
