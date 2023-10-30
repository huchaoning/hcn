from math import sqrt

point_1 = None
point_2 = None
characteristic_width = 1
mode = '+-'

def photon_number(img):
    return img[point_1[1]][point_1[0]], img[point_2[1]][point_2[0]]

def estimator(img, mode = mode):

    if img[point_2[1]][point_2[0]] == 0:
        return - 2 * characteristic_width
    else:
        if mode == '+-':
            k = sqrt(img[point_1[1]][point_1[0]] / img[point_2[1]][point_2[0]])
            return 2 * characteristic_width * (1-k)/(1+k)
        elif mode == '0001':
            return 2 * characteristic_width * sqrt(img[point_1[1]][point_1[0]] / img[point_2[1]][point_2[0]])

