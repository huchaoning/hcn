import numpy as np

point_1 = None
point_2 = None
characteristic_width = 1

def estimator(img):
    k = np.sqrt(img[point_1[1]][point_1[0]] / img[point_2[1]][point_2[0]])
    return 2 * characteristic_width * (k-1)/(k+1)

if __name__ == "__main__":
    main()
