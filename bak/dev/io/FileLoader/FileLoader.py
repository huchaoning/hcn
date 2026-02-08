import numpy as np

import os
import json as Json
import cv2

import pandas as pd
from PIL import Image

__all__ = ['FileLoader']

class FileLoader:
    def __init__(self, file):
        self.file = os.path.abspath(os.path.expanduser(file))
        if os.path.exists(self.file):
            self.basename = os.path.basename(self.file)
            self.extension = os.path.splitext(self.basename)[-1].lower()
        else:
            raise FileExistsError(f'{file} is not exists')



    def tiff(self):
        img = Image.open(self.file)
        arr = []
        for i in range(img.n_frames):
            img.seek(i)
            arr.append(img)
        arr = np.array(arr, dtype=float)
        if arr.shape[0] == 1:
            return arr[0]
        else:
            return arr



    def avi(self):
        avi = cv2.VideoCapture(self.file)
        arr = []
        while True:
            ret, frame = avi.read()
            if not ret:
                break
            arr.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        avi.release()
        return np.array(arr).astype(float)



    def npy(self):
        return np.load(self.file)



    def npz(self):
        dic = dict(np.load(self.file))
        for key in dic.keys():
            dic[key] = dic[key].astype(float)
        return dic



    def csv(self):
        return np.array(pd.read_csv(self.file, header=None))



    def json(self):
        with open(self.file, 'r') as f:
            return Json.load(f)



    def any(self):
        ext = self.extension
        
        if ext in ('.tiff'):
            return self.tiff()
        
        if ext in ('.avi'):
            return self.avi()
        
        if ext in ('.npy'):
            return self.npy()
        
        if ext in ('.npz'):
            return self.npz()

        if ext in ('.csv'):
            return self.csv()

        if ext in ('.json'):
            return self.json()
        
        else:
            raise NotImplementedError(f'{ext} file(s) is not supported yet')



