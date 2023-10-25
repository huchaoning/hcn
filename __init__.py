import numpy as np
import scipy as sp
import pandas as pd

import cv2 as cv

import matplotlib.pyplot as plt
from matplotlib_inline import backend_inline

import di
import spade
import laser

# # SPADE 估计子
# def midpoint_mean(array, midpoint):
#     temp = []
#     y = midpoint[0]
#     x = midpoint[1]
#     for i in (-1, 0, 1):
#         temp.append(array[x+i][y-1:y+2])
#     return np.array(temp, dtype=int).sum() / 9


# def spade_estimator(img_list, sigma=None, midpoint_1=None, midpoint_2=None):
#     data = []
#     for img in img_list:
#         array = tif_to_np(img)
#         k = np.sqrt(midpoint_mean(array, midpoint_1) / midpoint_mean(array, midpoint_2))
#         data.append(2 * sigma * (k-1)/(k+1))
#     return np.array(data)


# # -----------------------------
# # DI 估计子
# def get_zero_point(point_list):
#     temp = []
#     criterion = (point_list.max() + point_list.min()) / 2
#     for i in range(np.size(point_list)):
#         if point_list[i] < criterion:
#             temp.append(point_list[i])
#     temp = np.array(temp)
#     return temp.sum() / np.size(temp)


# def get_point_list(img_list):
#     point_list = []
#     for img in img_list:
#         array = tif_to_np(img)
#         index = np.arange(np.sqrt(np.size(array)))
#         new_array = array / array.sum()
#         point_list.append((index @ new_array).sum())
#     return np.array(point_list)


# def di_estimator(img_list, mmpp=None):
#     point_list = get_point_list(img_list)
#     zero_point = get_zero_point(point_list)
#     return (point_list - zero_point) * mmpp


# # -----------------------------
# # 批量生成tif路径
# def gen_img_list(fixes=None, raw_path=None, frames=None, fix_rule=None):
#     cmd = 'raw_path.format'+fix_rule
#     img_list = []
#     for fix in fixes:
#         for frame in range(1, frames+1):
#             img_list.append(eval(cmd))
#     return np.array(img_list).reshape(np.size(fixes), frames)


# # -----------------------------
# # 读取全部数据, 保存在data数组中并返回
# def read_all(fixes=None, raw_path=None, frames=None, fix_rule=None,
#              SPADE=True, sigma=None, midpoint_1=None, midpoint_2=None, 
#              mmpp=None):

#     img_list = gen_img_list(fixes=fixes, raw_path=raw_path, frames=frames, fix_rule=fix_rule)
#     data = []
#     if SPADE:
#         for index in range(np.size(fixes)):
#             data.append(spade_estimator(img_list[index], sigma=sigma, midpoint_1=midpoint_1, midpoint_2=midpoint_2))
#     elif not SPADE:
#         for index in range(np.size(fixes)):
#             data.append(classical_estimator(img_list[index], mmpp=mmpp))
#     else:
#         pass

#     return np.array(data)



# def delete_zeros(point_list):
#     temp = []
#     criterion = (point_list.max() + point_list.min()) / 2
#     for i in range(np.size(point_list)):
#         if point_list[i] > criterion:
#             temp.append(point_list[i])
#     temp = np.array(temp)
#     return temp
# # -----------------------------------------------

def abs_fft(array):
    return np.abs(sp.fft(array))


def imread(img_path):
    return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH)


def read_csv(path):
    return np.array(pd.read_csv(path, header=None))


# def tif_to_np(path):
#     img = Image.open(path)
#     Matrix = np.array(img.getdata()).reshape(img.size[1], img.size[0])
#     return Matrix


def save_as_csv(array, filename):
    pd.DataFrame(array).to_csv(filename, header=None, index=None)


def show_all_fonts():
    from matplotlib.font_manager import FontManager
    all_fonts = set(f.name for f in FontManager().ttflist)
    print('All font list get from matplotlib.font_manager:')
    for f in sorted(all_fonts):
        print('\t' + f)


def plot(X, Y, fmts='-',
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         show=True, save=None):

    backend_inline.set_matplotlib_formats('svg')

    if font is None:
        plt.rcdefaults()
    else:
        plt.rc('font', family=font)

    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    if title is not None:
        plt.title(title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    if xlim is not None:
        plt.xlim(xlim)

    if ylim is not None:
        plt.ylim(ylim)

    if label is None:
        plt.plot(X, Y, fmts)
    else:
        plt.plot(X, Y, fmts, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if save is not None:
        plt.savefig(save)

    if show:
        plt.show()
    

def hist(X, bins=300, histtype='step', density=True,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         save=None):

    backend_inline.set_matplotlib_formats('svg')

    if font is None:
        plt.rcdefaults()
    else:
        plt.rc('font', family=font)

    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    if title is not None:
        plt.title(title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    if xlim is not None:
        plt.xlim(xlim)

    if ylim is not None:
        plt.ylim(ylim)

    if label is None:
        plt.hist(X, bins=bins, histtype=histtype, density=density)
    else:
        plt.hist(X, bins=bins, histtype=histtype, density=density, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if save is not None:
        plt.savefig(save)

    plt.show()


def imshow(X, cmap=None, title=None, colorbar=True, axis=False, font=None, save=None):
    backend_inline.set_matplotlib_formats('svg')
    if font is None:
        plt.rcdefaults()
    else:
        plt.rc('font', family=font)

    if not axis:
        plt.xticks(())
        plt.yticks(())

    if title is not None:
        plt.title(title)

    if cmap is None:
        plt.imshow(X)
    else:
        plt.imshow(X, cmap=cmap)

    if colorbar:
        plt.colorbar()

    if save is not None:
        plt.savefig(save)

    plt.show()


if __name__ == "__main__":
    main()
