from getdata import Dataset as DATA
from torch.utils.data import DataLoader as DataLoader
from network import Net
import torch
from torch.autograd import Variable
import torch.nn as nn
from val import val

dataset_dir = './data/'
model_cp = './model/'
workers = 16
batch_size = 18
lr = 0.0001
nepoch = 200


def train():
    datafile = DATA('train', dataset_dir)
    dataloader = DataLoader(datafile, batch_size=batch_size, shuffle=True, num_workers=workers, drop_last=True)

    print('-------------train-----------------')
    print('Length of train set is {0}'.format(len(datafile)))
    model = Net()
    model = model.cuda()
    model = nn.DataParallel(model)
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    cnt = 0
    count = 0

    for epoch in range(nepoch):
        for img, label in dataloader:
            img, label = Variable(img).cuda(), Variable(label).cuda()
            out = model(img)
            loss = criterion(out, label.squeeze())
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            cnt += 1
            print('Epoch:{0},Frame:{1}, train_loss {2}'.format(epoch, cnt*batch_size, loss/batch_size))

        torch.save(model.state_dict(), '{0}/{1}model.pth'.format(model_cp,count))
        val(count)
        count += 1

if __name__ == '__main__':
    train()










