from kfont import DEEP, TEAL, MID, AMB, INK, GREY, figpath
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
import math

fig,ax=plt.subplots(figsize=(11.0,5.3),dpi=200)
def bottle(x,y,w,h,label,sub,col):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.07',
        facecolor='white',edgecolor=col,lw=2.0,zorder=3))
    ax.add_patch(FancyBboxPatch((x+0.04,y+0.04),w-0.08,(h-0.08)*0.62,boxstyle='round,pad=0.01,rounding_size=0.05',
        facecolor=col,alpha=0.18,edgecolor='none',zorder=4))
    ax.text(x+w/2,y+h*0.72,label,fontsize=10.3,color=col,ha='center',va='center',fontweight='bold',zorder=6)
    ax.text(x+w/2,y+h*0.34,sub,fontsize=8.8,color=GREY,ha='center',va='center',zorder=6)
def pump(cx,cy,tag):
    ax.add_patch(Circle((cx,cy),0.24,facecolor=MID,edgecolor='white',lw=2,zorder=6))
    ax.add_patch(Circle((cx,cy),0.10,facecolor='white',edgecolor='none',zorder=7))
    ax.text(cx,cy-0.40,tag,fontsize=9.2,color=MID,ha='center',va='top',fontweight='bold',zorder=6)

ys=[3.62,2.62,1.62]
src=[('표준액 35.0 PSU','보관 · 보정점 A',TEAL),('RO-DI','헹굼 · 보정점 B',DEEP),('수조물','시료',AMB)]
for (lab,sub,col),y in zip(src,ys):
    bottle(0.25,y-0.42,1.62,0.86,lab,sub,col)
    pump(2.62,y,'P%d'%(ys.index(y)+1))
    ax.annotate('',xy=(2.34,y),xytext=(1.92,y),arrowprops=dict(arrowstyle='-|>',lw=1.9,color=col,mutation_scale=15))
    ax.annotate('',xy=(4.42,2.62),xytext=(2.90,y),arrowprops=dict(arrowstyle='-|>',lw=1.9,color=col,
        mutation_scale=15,connectionstyle='arc3,rad=%.2f'%(0.16 if y>2.62 else (-0.16 if y<2.62 else 0))))

ax.add_patch(FancyBboxPatch((4.46,1.92),1.72,1.42,boxstyle='round,pad=0.03,rounding_size=0.09',
    facecolor='#DCEEF7',edgecolor=MID,lw=2.4,zorder=5))
ax.text(5.32,2.92,'플로우셀',fontsize=11.6,color=MID,ha='center',va='center',fontweight='bold',zorder=7)
ax.text(5.32,2.55,'BK7 + LED\n+ TSL1401',fontsize=9.4,color=DEEP,ha='center',va='center',linespacing=1.5,zorder=7)
ax.text(5.32,2.14,'섬프 열재킷',fontsize=8.8,color=TEAL,ha='center',va='center',fontweight='bold',zorder=7)

pump(7.05,2.62,'P4  배수')
ax.annotate('',xy=(6.78,2.62),xytext=(6.22,2.62),arrowprops=dict(arrowstyle='-|>',lw=2.1,color=GREY,mutation_scale=16))
ax.annotate('',xy=(8.30,3.20),xytext=(7.32,2.75),arrowprops=dict(arrowstyle='-|>',lw=1.9,color=TEAL,mutation_scale=15))
ax.annotate('',xy=(8.30,2.04),xytext=(7.32,2.49),arrowprops=dict(arrowstyle='-|>',lw=1.9,color='#B4453C',mutation_scale=15))
bottle(8.34,2.80,1.72,0.80,'수조 복귀','수조물 · 표준액',TEAL)
bottle(8.34,1.64,1.72,0.80,'폐수','구연산 · 세정액',"#B4453C")

ax.text(0.25,4.62,'유체 회로  —  페리스탈틱 펌프 4개, 밸브 없음',fontsize=13.5,color=MID,fontweight='bold',va='center')
ax.text(0.25,0.62,'페리스탈틱 펌프는 정지 시 튜브가 눌려 있어 사이펀이 원천 차단되고, 자흡이 되며, 액이 튜브 안에만 있어 교차오염이 없습니다.\n'
                  '표백제 등 수조에 위험한 세정액을 쓸 때는 복귀 라인을 물리적으로 분리해 폐수로만 보내십시오.',
        fontsize=9.6,color=INK,va='center',linespacing=1.7)
ax.set_xlim(0,10.35); ax.set_ylim(0.30,4.80); ax.axis('off')
plt.savefig(figpath('fig_fluidics.png'),dpi=200,facecolor='white',bbox_inches='tight',pad_inches=0.14)
print('ok')
