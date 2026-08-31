exec(open('/home/claude/salinity/kfont.py').read())
import matplotlib.pyplot as plt
import numpy as np

fig,ax=plt.subplots(figsize=(10.5,5.4),dpi=200)
PXPP=0.997; BASE=30.0     # RO/DI at px 30
S=np.linspace(-1,38,200); P=BASE+PXPP*S
ax.plot(S,P,color=DEEP,lw=2.6,zorder=3,label='검량선')
ax.fill_between([0,128],0,0,color='none')

pts=[(0.0,'RO-DI  0 PSU','보정점 B',TEAL),(34.1,'수조물  34.1 PSU','시료',AMB),(35.0,'표준액  35.0 PSU','보정점 A',TEAL)]
for s,lab,role,c in pts:
    p=BASE+PXPP*s
    ax.plot([s,s],[0,p],color=c,lw=1.1,ls=':',alpha=.85,zorder=2)
    ax.plot([-1,s],[p,p],color=c,lw=1.1,ls=':',alpha=.85,zorder=2)
    ax.scatter([s],[p],s=140,color=c,edgecolor='white',lw=2,zorder=5)
ax.annotate('RO-DI  0 PSU\n보정점 B',xy=(0,BASE),xytext=(3.2,BASE-9.5),fontsize=10,color=TEAL,fontweight='bold',
            ha='left',va='center',linespacing=1.5,arrowprops=dict(arrowstyle='-',lw=1.2,color=TEAL))
ax.annotate('표준액  35.0 PSU\n보정점 A',xy=(35,BASE+PXPP*35),xytext=(27.0,BASE+PXPP*35+13.0),fontsize=10,color=TEAL,
            fontweight='bold',ha='center',va='bottom',linespacing=1.5,arrowprops=dict(arrowstyle='-',lw=1.2,color=TEAL))
ax.annotate('수조물  34.1 PSU\n(시료)',xy=(34.1,BASE+PXPP*34.1),xytext=(36.6,BASE+PXPP*34.1-8.5),fontsize=10,color=AMB,
            fontweight='bold',ha='left',va='center',linespacing=1.5,arrowprops=dict(arrowstyle='-',lw=1.2,color=AMB))

ax.annotate('',xy=(17,BASE+PXPP*17),xytext=(17,BASE),arrowprops=dict(arrowstyle='<->',lw=1.5,color=MID))
ax.text(18.0,BASE+PXPP*8.5,'기울기 = 0.997 px / PSU\n≈ 1 픽셀당 1 PSU',fontsize=10.3,color=MID,ha='left',va='center',
        fontweight='bold',linespacing=1.6)

ax.axhspan(0,128,color='#F2F7FA',zorder=0)
ax.axhline(0,color=GREY,lw=1.2,ls='--'); ax.axhline(128,color=GREY,lw=1.2,ls='--')
ax.text(38.6,2,'px 0',fontsize=9,color=GREY,va='bottom',ha='right')
ax.text(38.6,124,'px 128  (어레이 끝)',fontsize=9,color=GREY,va='top',ha='right')
ax.text(1.0,116,'두 보정점이 128 px 어레이 안에 여유롭게 공존\n→ 매 측정 사이클마다 완전한 2점 보정',fontsize=10.4,color=DEEP,
        va='top',ha='left',fontweight='bold',linespacing=1.6)

ax.set_xlabel('염도  (PSU)',fontsize=11.5,color=INK,labelpad=8)
ax.set_ylabel('그림자 경계 픽셀 위치',fontsize=11.5,color=INK,labelpad=8)
ax.set_xlim(-1,39); ax.set_ylim(-4,132)
ax.set_xticks([0,5,10,15,20,25,30,35]); ax.set_yticks([0,32,64,96,128])
for sp in ('top','right'): ax.spines[sp].set_visible(False)
for sp in ('left','bottom'): ax.spines[sp].set_color('#C4D0D9')
ax.tick_params(colors=GREY,labelsize=9.5)
ax.grid(axis='y',color='#E3EBF0',lw=0.8,zorder=0)
ax.set_title('검량선:  RO-DI 와 표준액 두 점으로 매 측정마다 자가보정',fontsize=13.5,color=MID,
             fontweight='bold',loc='left',pad=14)
plt.tight_layout(pad=0.6)
plt.savefig('fig_cal.png',dpi=200,facecolor='white',bbox_inches='tight',pad_inches=0.12)
print('ok')
