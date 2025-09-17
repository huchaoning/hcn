import numpy as np
import matplotlib.pyplot as plt

from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('retina')
del backend_inline

import os
from matplotlib.font_manager import fontManager
assets_dir = os.path.join(os.path.dirname(__file__), 'assets/')
fontManager.addfont(os.path.join(assets_dir, 'fonts/SourceHanSans.otf'))
fontManager.addfont(os.path.join(assets_dir, 'fonts/lmroman10.otf'))
del fontManager

plt.rcParams['font.size'] = 7
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['xtick.major.width'] = 0.5
plt.rcParams['ytick.major.width'] = 0.5
plt.rcParams['figure.dpi'] = 150
plt.rcParams['figure.figsize'] = (3.3, 2.5)
plt.rcParams['lines.linewidth'] = 1.5

plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 2
plt.rcParams['ytick.major.size'] = 2

plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.prop_cycle'] = \
    plt.cycler('color', ['#0072bd', '#d95319', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f']) + \
    plt.cycler('linestyle', ['-', '--', '-.', ':', '-', '--', '-.'])

plt.rcParams['legend.fancybox'] = False
plt.rcParams['legend.frameon'] = True
plt.rcParams['legend.framealpha'] = 1.0
plt.rcParams['legend.edgecolor'] = 'k'
plt.rcParams['patch.linewidth'] = 0.5


import matplotlib as mpl
parula = mpl.colors.LinearSegmentedColormap.from_list('parula', list(np.load(os.path.join(assets_dir, 'parula_map.npy'))))
mpl.colormaps.register(parula)
plt.rcParams['image.cmap'] = 'parula'
del mpl, parula
