import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 用矢量图来显示
from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')
del backend_inline

from tqdm import tqdm
import os


'''
-----------------------------------------------------------------
考虑 DI, 假设高斯型 PSF
考虑无噪声的情况下, 点光源静止不动的情况
在这种情况下简单的求质心的估计子 (矩估计子) 等同于 MLE

SciPy 提供的 fit 方法只能对标准的几种分布做 MLE, 在这里为了简单起见直接调用
在实际实验过程中有人为引入噪声的时候该方法不适用, 所以用的是自己写的版本 
自己写的算法计算结果和 fit 方法的计算结果一致

采用面向对象的写法目的是改变参数方便, 在逻辑上也会更加清晰
Simulator 的参数即为点光源的参数, genr 方法的参数即为相机的参数
如果使用超参数的方法来写需要不停重定义函数比较麻烦
-----------------------------------------------------------------

-----------------------------------------------------------------
实验上的真实参数 (单位: um)
ROI 以高斯的 3 sigma 原则为标准, 可以理解为是使用尽可能少的探测器

sigma: 103
photons: 450
pixel_size: 4.6

roi: 6 * (103 / 4.6) 约 134
-----------------------------------------------------------------
'''

class Simulator:
    def __init__(self, loc, sigma, photons):
        '''
        loc (float): 点光源偏离中心的距离 (单位: um)
        sigma (float): 特征宽度 (单位: um)
        photons (int): 点光源发射的光子数, 也可以理解为一次曝光的光子数
        '''
        self.loc = loc
        self.sigma = sigma
        self.photons = photons


    # def genr(self, pixel_size=None, detectors=None, roi=None):
    def genr(self, pixel_size, roi):
        '''
        参数: (三者给定两个即可, 如果都给定了则默认忽视 detectors)
        pixel_size (float): 像素的大小 (单位: um)
        detector (int): 所使用的像素个数
        roi (tuple): 探测区域的大小 (单位: um)

        返回:
        x_axis (numpy.ndarray): x 轴坐标 (单位: um)
        raw (numpy.ndarray): 光子计数
        '''
        # 创建 bin 边界数组, 并将其调整为以 0 为中心, 转化为 float 降低上下溢风险
        # if pixel_size is None:
        #     bins = (np.linspace(*roi, ))
        # elif roi is None:
        #     bins = (np.arange(detectors+1) * pixel_size).astype(float)
        # else:
        #     bins

        bins = (np.arange(roi+1) * pixel_size).astype(float)
        bins -= bins.mean()

        # 创建 x 轴坐标数组, 并将其调整为以 0 为中心
        x_axis = (np.arange(roi) * pixel_size).astype(float)
        x_axis -= x_axis.mean()

        # 用计算统计直方的办法生成数据, 相当于像素点在做光子计数
        raw = np.histogram(np.random.normal(self.loc, self.sigma, self.photons), bins=bins)[0].astype(float)

        return x_axis, raw



# 对于高斯分布, 没有噪声的情况下 MLE 等同于矩估计子
def estimator(x_axis, raw, method='mle'):
    '''
    参数:
    x_axis (numpy.ndarray): x 轴坐标
    raw (numpy.ndarray): 光子计数, 也可理解为相机采集到的图像
    method (str): mle 或 simple

    返回:
    float: 估计值, 单位等同于 x_axis 的单位
    '''
    if method.lower() == 'simple':
        return x_axis @ raw / raw.sum()
    
    elif method.lower() == 'mle':
        # 用 repeat 方法把每个光子所在的位置记录到一个数组里面
        x = np.repeat(x_axis, raw.astype(int))
        return norm.fit(x)[0]