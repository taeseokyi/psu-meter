exec(open('/home/claude/salinity/kfont.py').read())
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle, Circle
import numpy as np, math

fig,ax=plt.subplots(figsize=(11.5,5.6),dpi=200)
TC=61.9279; R=1.0; th=math.radians(TC)

ax.add_patch(Rectangle((-1.55,0),3.1,0.80,facecolor='#CFE7F2',edgecolor='none',zorder=1))
ax.text(-1.45,0.62,'시료  (해수 / RO-DI / 표준액)',ha='left',va='center',fontsize=11,color=DEEP,fontweight='bold')
ax.add_patch(Wedge((0,0),R,180,360,facecolor='#DEEAF1',edgecolor=DEEP,lw=2.0,zorder=2))
ax.text(0,-1.16,'BK7 반원통 렌즈   n = 1.5168',ha='center',va='center',fontsize=10.5,color=DEEP,fontweight='bold',zorder=8)
ax.plot([-R,R],[0,0],color=MID,lw=3.2,zorder=4)
ax.text(1.06,-0.09,'측정면',fontsize=10,color=MID,va='top',ha='left',fontweight='bold')

L_in=1.75
xi,yi=-L_in*math.sin(th),-L_in*math.cos(th)
ax.annotate('',xy=(0,0),xytext=(xi,yi),arrowprops=dict(arrowstyle='-|>',lw=2.6,color=AMB,mutation_scale=19),zorder=5)
L_out=2.45
xo,yo=L_out*math.sin(th),-L_out*math.cos(th)
ax.annotate('',xy=(xo,yo),xytext=(0,0),arrowprops=dict(arrowstyle='-|>',lw=2.6,color=AMB,mutation_scale=19),zorder=5)
for dd in (-2.4,2.4):
    t2=math.radians(TC+dd)
    ax.plot([-L_in*math.sin(t2),0],[-L_in*math.cos(t2),0],color=AMB,lw=0.9,ls=':',alpha=.8,zorder=4)
    ax.plot([0,L_out*math.sin(t2)],[0,-L_out*math.cos(t2)],color=AMB,lw=0.9,ls=':',alpha=.8,zorder=4)
ax.annotate('',xy=(0.42,0.55),xytext=(0,0),arrowprops=dict(arrowstyle='-|>',lw=1.4,color=GREY,ls='--',mutation_scale=12),zorder=5)
ax.text(0.50,0.40,'임계각 미만 →\n시료로 투과(손실)',fontsize=9,color=GREY,va='center',ha='left',linespacing=1.4)

ax.plot([0,0],[-0.16,0.80],color=GREY,lw=1.0,ls='-.',zorder=3)
ax.text(-0.05,0.78,'법선',fontsize=9,color=GREY,va='top',ha='right')
for sgn in (-1,1):
    a=np.linspace(0,th,60)
    ax.plot(sgn*0.50*np.sin(a),-0.50*np.cos(a),color=MID,lw=1.5,zorder=6)
ax.text(-0.30,-0.31,'61.93°',fontsize=10.5,color=MID,fontweight='bold',ha='center',zorder=8)
ax.text( 0.30,-0.31,'61.93°',fontsize=10.5,color=MID,fontweight='bold',ha='center',zorder=8)

ax.add_patch(Circle((xi,yi),0.125,facecolor=AMB,edgecolor='white',lw=2,zorder=7))
ax.text(xi,yi-0.20,'단색 LED 590nm + 슬릿\n입사팔 ≈ 40 mm',fontsize=10,color=INK,ha='center',va='top',fontweight='bold',linespacing=1.5)
ax.plot([xo-0.09,xo+0.09],[yo+0.15,yo-0.15],color=MID,lw=7,solid_capstyle='butt',zorder=7)
ax.text(xo+0.19,yo,'TSL1401CL 리니어 어레이\n128 px × 63.5 µm\n검출팔 = 250 mm',fontsize=10,color=INK,ha='left',va='center',fontweight='bold',linespacing=1.5)

ax.text(-3.05,0.72,'임계각 원리',fontsize=15.5,color=MID,fontweight='bold',va='top')
ax.text(-3.05,0.42,'염도 ↑  →  굴절률 ↑  →  임계각 ↑\n→  그림자 경계가 어레이 위에서 이동',fontsize=10.3,color=INK,va='top',linespacing=1.7)
ax.text(-3.05,-1.02,'감도',fontsize=9.5,color=GREY,va='top')
ax.text(-3.05,-1.16,'253 µrad / PSU',fontsize=13,color=AMB,va='top',fontweight='bold')
ax.text(-3.05,-1.44,'250 mm 검출팔에서',fontsize=9.5,color=GREY,va='top')
ax.text(-3.05,-1.58,'1 px  ≈  1 PSU',fontsize=13,color=DEEP,va='top',fontweight='bold')

ax.set_xlim(-3.15,3.55); ax.set_ylim(-1.80,0.86); ax.set_aspect('equal'); ax.axis('off')
plt.savefig('fig_optics.png',dpi=200,facecolor='white',bbox_inches='tight',pad_inches=0.12)
print('ok')
