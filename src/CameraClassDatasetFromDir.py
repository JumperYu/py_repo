import torch
import torchvision
from torchvision import datasets, models, transforms
import pandas as pd
from torch.utils.data.dataset import Dataset  # For custom dataset

import os

data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.456, 0.456, 0.406], [0.229, 0.224, 0.225])

    ])
}


class CameraClassDatasetFromDir(Dataset):

    def __init__(self, root_path, csv_path, train=True, transform=None):
        self.root_path = root_path
        self.train = train
        self.transform = transform

        self.dict = {'0_little_round': 0, '1_triangle': 1, '2_none': 2, '3_big_round': 3, '4_square': 4,
                     '5_right_round': 5}

        df = pd.read_csv(csv_path)

        self.df = df
        self.label_arr = []
        self.image_arr = []

        for index, row in df.iterrows():
            self.label_arr.append(self.dict[row['className']])
            self.image_arr.append(row['fileName'])

        self.data_len = len(self.image_arr)

        self.image_data_sets = {x: datasets.ImageFolder(os.path.join(root_path, x),
                                                        data_transforms[x])
                                for x in ['train', 'val']}
        self.data_loaders = {
            x: torch.utils.data.DataLoader(self.image_data_sets[x], batch_size=4, shuffle=True, num_workers=4)
            for x in ['trains', 'val']}


    def __getitem__(self, index):
        label = self.label_arr[index]
        image = self.image_arr[index]
        return label, image

    def __len__(self):
        return len(self.image_arr)


if __name__ == "__main__":
    dataset = CameraClassDatasetFromDir('C:/work/dev/camera_class_win10/', '../data/manifest.csv')
    print(dataset[0])
