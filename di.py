import numpy as np
from mypy import imread

def get_zero_point(point_list):
    temp = []
    criterion = (point_list.max() + point_list.min()) / 2
    for i in range(np.size(point_list)):
        if point_list[i] < criterion:
            temp.append(point_list[i])
    temp = np.array(temp)
    return temp.sum() / np.size(temp)


def get_point_list(img_list):
    point_list = []
    for img in img_list:
        array = imread(img)
        index = np.arange(np.sqrt(np.size(array)))
        new_array = array / array.sum()
        point_list.append((index @ new_array).sum())
    return np.array(point_list)


def di_estimator(img_list, mmpp=None):
    point_list = get_point_list(img_list)
    zero_point = get_zero_point(point_list)
    return (point_list - zero_point) * mmpp

if __name__ == "__main__":
    main()
