import os

def rename_util(method, path='./'):
    name_dict = {'m(7)':-7,
                 'm(6)':-6,
                 'm(5)':-5,
                 'm(4)':-4,
                 'm(3)':-3,
                 'm(2)':-2,
                 'm(1)':-1,
                 'p(0)': 0,
                 'p(1)': 1,
                 'p(2)': 2,
                 'p(3)': 3,
                 'p(4)': 4,
                 'p(5)': 5,
                 'p(6)': 6,
                 'p(7)': 7}
    for name in name_dict:
        os.rename(src = os.path.join(path, method + '_' + name + '.tif'), 
                  dst = os.path.join(path, method + str(name_dict[name])) + '.tif')