import numpy as np

zero_point = 0
pixel_size = 1

def estimator(img):
    index = np.arange(np.shape(img)[0])
    normalized_img = img / img.sum()
    return ((index @ normalized_img).sum() - zero_point) * pixel_size

if __name__ == "__main__":
    main()
