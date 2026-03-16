import numpy as np
import pandas as pd
from PIL import Image
import imageio.v3 as iio
import json

import os
import inspect
import platform
import subprocess


__all__ = [
    "code",
    "open",
    "load",
    "save"
]


COMPRESS_CONFIG = {
    "png": {
        "key": "compression",
        "map": {"xs": 1, "sm": 3, "md": 6, "lg": 8, "xl": 9}
    },

    "tif": {
        "key": "compression",
        "fixed": {"compression": "zlib"},
        "map": {"xs": 1, "sm": 3, "md": 6, "lg": 8, "xl": 9}
    },
    "tiff": "tif",

    "jpg": {
        "key": "quality",
        "map": {"xs": 98, "sm": 95, "md": 90, "lg": 80, "xl": 70}
    },
    "jpeg": "jpg",
}


def code(input_):
    if inspect.isfunction(input_) or inspect.ismodule(input_) or inspect.isclass(input_):
        file_path = inspect.getfile(input_)
    else:
        file_path = os.path.expanduser(input_)

    if platform.system() == "Darwin":
        subprocess.run(["code", file_path], check=True)
    elif platform.system() == "Windows":
        subprocess.run(["powershell.exe", "-Command", rf"code '{file_path}'"], check=True)
    else:
        raise NotImplementedError("This function is supported on Windows and macOS only.")
    
    return os.path.abspath(file_path)



def open(input_):
    if inspect.isfunction(input_) or inspect.ismodule(input_) or inspect.isclass(input_):
        file_dir = os.path.dirname(inspect.getfile(input_))
    else:
        file_dir = os.path.expanduser(input_)

    if platform.system() == "Darwin":
        subprocess.run(["open", file_dir], check=True)
    elif platform.system() == "Windows":
        subprocess.run(["start", "", file_dir], shell=True, check=True)
    else:
        raise NotImplementedError("This function is supported on Windows and macOS only.")
    
    return os.path.abspath(file_dir)



class _FileReader:
    def __init__(self, path):
        self.path = os.path.expanduser(path)

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"{path} does not exists")
        
        self.path = path
        self.ext = os.path.splitext(path)[-1].lower()[1:]
        self.name = os.path.basename(path)
        self.stem = os.path.splitext(self.name)[0]

    
    def _iio(self):
        return np.squeeze(iio.imread(self.path, extension=f".{self.ext}"))


    def _json(self):
        with open(self.path, "r") as f:
            dic = json.load(f)
        return dic


    def _csv(self):
        return np.array(pd.read_csv(self.path, header=None))


    def _npy(self):
        return np.load(self.path)


    def _npz(self):
        dic = dict(np.load(self.path))
        for key in dic.keys():
            dic[key] = dic[key]
        return dic


    def _other(self):
        msg = f"No implemented method for '.{self.ext}', nothing to return."
        if os.path.exists(self.path):
            msg += f"The file '{self.name}' exists, you may use finder() to open it."
        print(msg)
        return None


    def load(self):
        if self.ext == "npz":
            data = self._npz()

        elif self.ext == "npy":
            data = self._npy()

        elif self.ext in ["jpg", "jpeg", "png", "bmp", "tif", "tiff", "avi"]:
            data = self._iio()

        elif self.ext == "csv":
            data = self._csv()

        elif self.ext == "json":
            data = self._json()

        else:
            data = self._other()

        return data



class _FileWriter:
    def __init__(self, path, data, compress):
        self.path = os.path.abspath(os.path.expanduser(path))
        self.data = data
        self.compress = compress

        self.ext = os.path.splitext(self.path)[-1].lower()[1:]
        self.name = os.path.basename(self.path)
        self.stem = os.path.splitext(self.name)[0]


    def _json(self):
        if isinstance(self.data, dict):
            with open(self.path, "w") as f:
                json.dump(self.data, f, indent=2)
        else:
            raise TypeError("'.json' format requires a dict of arrays")


    def _csv(self):
        arr = np.array(self.data)
        pd.DataFrame(arr).to_csv(self.path, index=False, header=False)


    def _npy(self):
        np.save(self.path, np.array(self.data))

    def _npz(self):
        if isinstance(self.data, dict):
            np.savez_compressed(self.path, **{k: np.array(v) for k, v in self.data.items()})
            return self.path
        else:
            raise TypeError("'.npz' format requires a dict of arrays")
        
    def _iio(self):
        cfg = COMPRESS_CONFIG.get(self.ext)
        if isinstance(cfg, str): 
            cfg = COMPRESS_CONFIG.get(cfg)

        lvl = "md" if self.compress is True else self.compress
        params = {cfg["key"]: cfg["map"].get(lvl, lvl)} if (self.compress and cfg) else {}

        if cfg and "fixed" in cfg: 
            params.update(cfg["fixed"])

        return iio.imwrite(self.path, self.data, extension=f".{self.ext}", **params)


    def _other(self):
        msg = f"No implemented method for '.{self.ext}', nothing saved."
        print(msg)


    def save(self):
        if self.ext == "npz":
            self._npz()
        
        elif self.ext == "npy":
            self._npy()

        elif self.ext in ["jpg", "jpeg", "png", "bmp", "tif", "tiff", "avi"]:
            self._iio()
        
        elif self.ext == "csv":
            self._csv()
        
        elif self.ext == "json":
            self._json()
        
        else:
            self._other()



def load(path, dtype=None):
    target = _FileReader(path)
    return target.load() if dtype is None else target.load().astype(dtype)



def save(path, data, dtype=None, compress=False):
    data = np.asarray(data) if dtype is None else np.asarray(data).astype(dtype)
    target = _FileWriter(path, data, compress)
    target.save()
    return target.path

