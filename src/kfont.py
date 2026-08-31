import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt, warnings
warnings.filterwarnings('ignore')
for f in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
          '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc']:
    fm.fontManager.addfont(f)
NAME=fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc').get_name()
plt.rcParams['font.family']=NAME
plt.rcParams['axes.unicode_minus']=False
DEEP='#065A82'; TEAL='#1C7293'; MID='#21295C'; AMB='#E8901F'; INK='#1A2430'; GREY='#78899A'
