import pandas as pd
from torch.utils.data import DataLoader

from torch.utils.data.dataset import Dataset  # For custom dataset


class CameraClassDatasetFromDir(Dataset):

    def __init__(self, root_path, csv_path, train=True, augment=None):
        self.root_path = root_path
        self.train = train
        self.augment = augment  # 是否需要图片增强

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

    def __getitem__(self, index):
        data = (self.label_arr[index], self.image_arr[index])
        return data

    def __len__(self):
        return len(self.image_arr)


if __name__ == "__main__":
    dataset = CameraClassDatasetFromDir('C:/work/dev/camera_class_win10/', '../data/manifest.csv')
    data_loader = DataLoader(dataset, batch_size=16, shuffle=False)
    for i, data in enumerate(data_loader):
        print(data)
