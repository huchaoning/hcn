# 个人使用 Python 常用函数集合

## 这是什么

用于保存日常用 Python 做科学计算和数据处理的代码, 减少重复造轮子. 主要功能有:

- 画图
- 数据处理
- 产生 SLM 用的全息图
- 产生 DMD 用的位图


## 优点

- 比直接调用 Python 更简单, 因为只保留了我认为常用的功能
- 画的图默认矢量图显示 (如果可以的话)


## 目标

成为实验室祖传代码


## 如何使用

推荐把整个文件夹放到 Anaconda 的 `site-packages` 文件夹下, 可以直接 `import mypy`

- 想知道 `site-packages` 在哪?

```python
import numpy as np

print(np.__file__)
```