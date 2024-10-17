# 个人使用 Python 常用函数集合

## 这是什么

用于保存日常用 Python 做科学计算和数据处理的代码, 减少重复造轮子. 主要功能有:

- 画图
- 数据处理
- 实验模拟
- 处理一些简单的数学比如积分、求梯度和归一化等
- 产生 SLM 用的全息图


## 用到的包

numpy, matplotlib, math, scipy, pandas, PIL (pillow), opencv, gitpython, dask

opencv 用于读取 avi 视频, 如果样本比较长的时候用 tif 格式无论是读取还是保存都很慢, 所以使用 avi 视频格式. opencv 只会在调用 `aviread` 函数的时候被导入.

gitpython 用于 `pull` 和 `push`, 相当于 git 在 notebook 里面的快捷方式

dask 用于 `parallelize` 装饰器, 用于在 notebook 里实现简单的并行计算


## 优点

- 比直接调用 Python 更简单, 因为只保留了我认为常用的功能
- 画的图默认矢量图显示 (如果可以的话) 
- 字体默认使用思源黑体和 LM Roman 10. 因为有独立的字体文件所以不需要安装字体
- 简化版的 `plot` 函数, 可以直接输入定义域和函数名画图


## 如何使用

推荐把整个文件夹放到 Anaconda 的 `site-packages` 文件夹下, 可以直接 `import mypy`

- 想知道 `site-packages` 在哪?

```python
import numpy as np
print(np.__file__)
```
