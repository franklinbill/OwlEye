from PIL import Image,ImageFile
from sklearn import metrics
ImageFile.LOAD_TRUNCATED_IMAGES = True
from network import Net
import torch
import numpy as np
import torch.nn.functional as F
import torch.nn as nn
import os
import getdata

dataset_dir = './data/test/'                    # 数据集路径
model_path = './model/'

def test():

    model_file = model_path + 'model.pth'
    model = Net()
    model.cuda()
    model = nn.DataParallel(model)
    model.load_state_dict(torch.load(model_file))
    model.eval()

    files = os.listdir(dataset_dir)
    imgs_data = []
    out1 = []
    for file in files:
        img = Image.open(dataset_dir + file)
        img_data = getdata.dataTransform(img)
        imgs_data.append(img_data)
        imgs_data = torch.stack(imgs_data)
        out = model(imgs_data)
        out = F.softmax(out, dim=1)
        out = out.data.cpu().numpy()
        out2 = out[0]
        out1.append(out2)
        imgs_data = []
    out3 = np.array(out1)
    x = []
    y = []

    for idx in range(len(files)):
        a = files[idx]
        (filename, extension) = os.path.splitext(a)
        b = int(filename)
        if b <= 900:
            y.append(1)
            if out3[idx, 0] > out3[idx, 1]:
                x.append(1)
            else:
                x.append(0)
        else:
            y.append(0)
            if out3[idx, 0] > out3[idx, 1]:
                x.append(1)
            else:
                x.append(0)


    p = metrics.precision_score(y, x)
    r = metrics.recall_score(y, x)
    f1 = metrics.f1_score(y, x)

    print('-------------test-----------------')
    print('precision: %f' % p)
    print('recall: %f' % r)
    print('f1_score: %f' % f1)


if __name__ == '__main__':
    test()



