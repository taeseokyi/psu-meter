# -*- coding: utf-8 -*-
"""도해 스크립트 공통 설정 — 한글 폰트 등록과 그림 저장 경로.

사용법 (src/ 안의 도해 스크립트에서):

    from kfont import DEEP, TEAL, MID, AMB, INK, GREY, figpath
    ...
    plt.savefig(figpath('fig_head.png'), dpi=150, ...)

**이 모듈을 matplotlib.pyplot 보다 먼저 import 하십시오.** 백엔드를 Agg 로
고정하고 rcParams 를 잡는 일을 여기서 합니다.

한글 폰트
---------
설치돼 있는 CJK 폰트를 플랫폼별 후보 목록에서 찾아 등록합니다.
윈도우(맑은 고딕·나눔고딕), 리눅스(Noto Sans CJK·나눔고딕), macOS 를 봅니다.
찾지 못하면 경고만 내고 계속합니다 — 그림은 나오되 한글이 두부(□)가 됩니다.
특정 폰트를 강제하려면 환경변수 PSU_FONT 에 파일 경로를 넣으십시오.

    PSU_FONT=/path/to/NanumGothic.ttf python head.py

그림 저장 경로
--------------
기본값은 <저장소>/docs/figures/ 입니다 — GitHub Pages 가 서비스하는 자리입니다.
즉 스크립트를 그냥 실행하면 커밋된 그림을 그 자리에서 덮어씁니다. 시험 삼아 돌려 보고 싶으면 PSU_FIG_DIR 로
다른 곳에 떨구십시오.

    PSU_FIG_DIR=/tmp/fig python head.py
"""

import os
import glob
import warnings

import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# ── 색 팔레트 (설계 문서 pptx 와 동일) ────────────────────────────────
DEEP = '#065A82'
TEAL = '#1C7293'
MID  = '#21295C'
AMB  = '#E8901F'
INK  = '#1A2430'
GREY = '#78899A'

# ── 그림 저장 경로 ────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.environ.get('PSU_FIG_DIR') or os.path.join(os.path.dirname(_HERE), 'docs', 'figures')


def figpath(name):
    """그림 파일의 저장 경로. 디렉터리가 없으면 만든다."""
    if not os.path.isdir(FIGDIR):
        os.makedirs(FIGDIR)
    return os.path.join(FIGDIR, name)


# ── 한글 폰트 ─────────────────────────────────────────────────────────
# 앞에 있는 것부터 시도한다. glob 패턴을 그대로 쓴다.
_FONT_CANDIDATES = [
    # Windows
    r'C:\Windows\Fonts\malgun.ttf',            # 맑은 고딕
    r'C:\Windows\Fonts\NanumGothic.ttf',
    r'C:\Windows\Fonts\NGULIM.TTF',            # 새굴림
    r'C:\Windows\Fonts\gulim.ttc',
    # Linux
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/**/NotoSansCJK*.ttc',
    '/usr/share/fonts/**/NanumGothic*.ttf',
    # macOS
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    '/Library/Fonts/NanumGothic.ttf',
    # cygwin 에서 본 윈도우 폰트 디렉터리
    '/cygdrive/c/Windows/Fonts/malgun.ttf',
]


def _find_font():
    forced = os.environ.get('PSU_FONT')
    if forced:
        if os.path.isfile(forced):
            return forced
        warnings.warn('PSU_FONT 가 가리키는 파일이 없습니다: %s' % forced)
    for pat in _FONT_CANDIDATES:
        if '*' in pat:
            hits = sorted(glob.glob(pat, recursive=True))
            if hits:
                return hits[0]
        elif os.path.isfile(pat):
            return pat
    return None


def _setup():
    path = _find_font()
    if path is None:
        print('[kfont] 경고: 한글 폰트를 찾지 못했습니다. 한글이 깨져 나옵니다.\n'
              '        PSU_FONT 환경변수로 폰트 파일을 직접 지정하십시오.')
        return None
    try:
        fm.fontManager.addfont(path)                       # matplotlib >= 3.2
    except AttributeError:                                  # 구버전 폴백
        fm.fontManager.ttflist.extend(fm.createFontList([path]))
    name = fm.FontProperties(fname=path).get_name()
    plt.rcParams['font.family'] = name
    return name


NAME = _setup()
plt.rcParams['axes.unicode_minus'] = False
