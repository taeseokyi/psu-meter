exec(open('/home/claude/salinity/kfont.py').read())
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Wedge, Circle
import math

fig,ax=plt.subplots(figsize=(10.8,5.5),dpi=200)
ax.add_patch(FancyBboxPatch((0.20,0.55),5.40,4.05,boxstyle='round,pad=0.06,rounding_size=0.14',
        facecolor='#DCEEF7',edgecolor=TEAL,lw=1.8,ls='--',zorder=0))
ax.text(0.42,4.40,'열재킷  —  섬프 물에 담가 수조 온도로 유지',fontsize=10.5,color=TEAL,fontweight='bold',va='center')

ax.add_patch(FancyBboxPatch((1.62,1.35),3.55,2.50,boxstyle='round,pad=0.03,rounding_size=0.08',
        facecolor='#F7FAFC',edgecolor=MID,lw=2.2,zorder=2))
ax.add_patch(Rectangle((1.76,1.47),3.27,1.78,facecolor='#CFE7F2',edgecolor='none',zorder=3))
ax.text(3.40,3.03,'측정 챔버  ≈ 2 mL',fontsize=11,color=DEEP,fontweight='bold',ha='center',va='center',zorder=6)

ax.plot([2.68,4.12],[1.47,1.47],color=MID,lw=4.0,zorder=7)
ax.add_patch(Wedge((3.40,1.47),0.62,180,360,facecolor='#DEEAF1',edgecolor=DEEP,lw=1.8,zorder=6))
ax.text(3.40,1.16,'BK7 측정면',fontsize=9.4,color=DEEP,ha='center',va='center',fontweight='bold',zorder=8)

for bx,by,r in [(2.32,1.90,.055),(2.55,2.32,.045),(2.20,2.66,.060)]:
    ax.add_patch(Circle((bx,by),r,facecolor='white',edgecolor=DEEP,lw=1.0,zorder=5))
ax.annotate('',xy=(2.30,2.95),xytext=(2.30,1.72),arrowprops=dict(arrowstyle='-|>',lw=1.5,color=DEEP,
            alpha=.6,ls=':',mutation_scale=13),zorder=5)
ax.text(2.62,1.86,'기포는 측정면에서\n멀어지며 상승',fontsize=9.3,color=DEEP,ha='left',va='center',linespacing=1.5,zorder=8)

ax.annotate('',xy=(1.78,1.68),xytext=(0.72,1.68),arrowprops=dict(arrowstyle='-|>',lw=2.4,color=TEAL,mutation_scale=17))
ax.text(0.66,1.68,'주입\n(하부)',fontsize=9.7,color=TEAL,ha='right',va='center',fontweight='bold',linespacing=1.5)
ax.annotate('',xy=(6.10,3.58),xytext=(5.05,3.58),arrowprops=dict(arrowstyle='-|>',lw=2.0,color=GREY,mutation_scale=15))
ax.text(6.22,3.58,'벤트 /\n오버플로',fontsize=9.7,color=GREY,ha='left',va='center',fontweight='bold',linespacing=1.5)
ax.annotate('',xy=(6.10,1.62),xytext=(5.05,1.62),arrowprops=dict(arrowstyle='-|>',lw=2.4,color=AMB,mutation_scale=17))
ax.text(6.22,1.62,'배수 (하부)',fontsize=9.7,color=AMB,ha='left',va='center',fontweight='bold')

ax.add_patch(Circle((4.68,2.52),0.145,facecolor='#7B4FA8',edgecolor='white',lw=1.5,zorder=8))
ax.text(4.68,2.74,'UVC LED  265 nm',fontsize=9.2,color='#6B3F97',ha='center',va='bottom',fontweight='bold',zorder=8)
ax.add_patch(Rectangle((1.90,1.98),0.19,0.34,facecolor='#3A4A5A',edgecolor='white',lw=1.2,zorder=8))
ax.text(1.72,1.30,'DS18B20\n(셀 유로 내부)',fontsize=9.2,color=INK,ha='center',va='top',fontweight='bold',linespacing=1.5,zorder=8)
ax.plot([1.99,1.86],[1.98,1.52],color=INK,lw=0.9,zorder=7)

ax.text(7.62,4.35,'플로우셀 설계 요점',fontsize=14,color=MID,fontweight='bold',va='center')
pts=['측정면을 챔버 하부에 배치 →\n기포가 광로에서 멀어지며 상승',
     '주입은 최하부, 벤트는 최상부 →\n남은 기포가 밀려 올라가 배출',
     '섬프에 담가 시료와 표준액이\n항상 같은 온도  (온도 오차 상쇄)',
     '온도는 수조가 아니라\n셀 유로 안에서 측정']
y=3.78
for i,t in enumerate(pts):
    ax.add_patch(Circle((7.73,y),0.115,facecolor=AMB,edgecolor='none',zorder=5))
    ax.text(7.73,y,str(i+1),fontsize=9,color='white',ha='center',va='center',fontweight='bold',zorder=6)
    ax.text(7.97,y,t,fontsize=10,color=INK,va='center',linespacing=1.6)
    y-=0.85

ax.set_xlim(0,11.6); ax.set_ylim(0.42,4.72); ax.axis('off')
plt.savefig('fig_cell.png',dpi=200,facecolor='white',bbox_inches='tight',pad_inches=0.14)
print('ok')
