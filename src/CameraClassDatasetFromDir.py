import os

import pandas as pd
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
from torch.utils.data.dataset import Dataset  # For custom datasets

from cnn_model import MnistCNNModel


class CameraClassDatasetFromDir(Dataset):
    def __init__(self, dir_path):

        self.label_arr = []
        self.image_arr = []

        for root, dirs, files in os.walk(dir_path):
            if root == dir_path:
                continue

            for index, file in enumerate(files):
                # # 获取文件所属目录
                self.label_arr.insert(index, root[root.rfind("\\") + 1:])
                # # 获取文件路径
                self.image_arr.insert(index, os.path.join(root, file))

        print(self.label_arr)
        print(self.image_arr)

    def __getitem__(self, index):
        return ()

    def __len__(self):
        return len(self.image_arr)


if __name__ == "__main__":
    cameraClassDatasetFromDir = CameraClassDatasetFromDir('C:\\work\\dev\\camera_class_win10\\')
