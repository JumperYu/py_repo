#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms, datasets

data_transform = transforms.Compose([
    transforms.RandomCrop(224),
    transforms.RandomResizedCrop(224),
    transforms.Resize((32, 32)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
my_dataset = datasets.ImageFolder(root=r'/home/zxm/work/repo/py_repo/data/train',
                                  transform=transforms.Compose([
                                      transforms.Resize(256),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor()])
                                  )

data_loader = torch.utils.data.DataLoader(my_dataset, batch_size=36, shuffle=False)
print(len(data_loader))


def imshow(img):
    #    img = img / 2 + 0.5     # unnormalize
    img = torchvision.utils.make_grid(img, nrow=6)
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.title('Batch from dataloader')
    plt.xticks([])
    plt.yticks([])
    plt.show()

# get some random training images
dataiter = iter(data_loader)

images, labels = dataiter.next()
print(images.shape, labels)
# show images
imshow(images)
