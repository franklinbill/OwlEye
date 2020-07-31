import cv2
import numpy as np
import torch
from torch.autograd import Variable
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from network import Net
import torch.nn as nn
import getdata
import os

image_dir = './input_pic/'
model_dir = './model/model.pth'

class FeatureExtractor():

    def __init__(self, model, target_layers):
        self.model = model
        self.target_layers = target_layers
        self.gradients = []

    def save_gradient(self, grad):
        self.gradients.append(grad)

    def __call__(self, x):
        outputs = []
        self.gradients = []

        for name, module in self.model.module.features._modules.items():
            x = module(x)
            if name in self.target_layers:
                x.register_hook(self.save_gradient)
                outputs += [x]
        return outputs, x

class ModelOutputs():

    def __init__(self, model, target_layers):
        self.model = model
        self.feature_extractor = FeatureExtractor(self.model, target_layers)

    def get_gradients(self):
        return self.feature_extractor.gradients

    def __call__(self, x):
        target_activations, output = self.feature_extractor(x)
        output = output.view(output.size(0), -1)

        return target_activations, output


def preprocess_image(image_file):

    imgs_data = []
    img = Image.open(image_file)
    img_data = getdata.dataTransform(img)

    imgs_data.append(img_data)
    imgs_data = torch.stack(imgs_data)
    input = Variable(imgs_data, requires_grad = True)
    return input

def localization_result(img, mask,image_num):
    heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
    heatmap = np.float32(heatmap) / 255
    cam = heatmap + np.float32(img)
    cam = cam / np.max(cam)
    cv2.imwrite("./output_pic/{0}.jpg".format(image_num), np.uint8(255 * cam))

class GradCam:
    def __init__(self, model, target_layer_names):
        self.model = model
        self.model.eval()
        self.model = model.cuda()

        self.extractor = ModelOutputs(self.model, target_layer_names)

    def forward(self, input):
        return self.model(input)

    def __call__(self, input, index=None):
        features, output = self.extractor(input.cuda())

        if index == None:
            index = np.argmax(output.cpu().data.numpy())

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0][index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        one_hot = torch.sum(one_hot.cuda() * output)

        self.model.zero_grad()
        one_hot.backward(retain_graph=True)

        grads_val = self.extractor.get_gradients()[-1].cpu().data.numpy()

        target = features[-1]
        target = target.cpu().data.numpy()[0, :]

        weights = np.mean(grads_val, axis=(2, 3))[0, :]
        cam = np.zeros(target.shape[1:], dtype=np.float32)

        for i, w in enumerate(weights):
            cam += w * target[i, :, :]

        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (448, 768))
        cam = cam - np.min(cam)
        cam = cam / np.max(cam)
        return cam

if __name__ == '__main__':

    files = os.listdir(image_dir)

    for file in files:
        print(file)
        (filename, extension) = os.path.splitext(file)
        image_num = filename
        image_name = image_dir + file

        model = Net()
        model.cuda()
        model = nn.DataParallel(model)
        model.load_state_dict(torch.load(model_dir))

        grad_cam = GradCam(model=model, target_layer_names=["40"])
        img = cv2.imread(image_name, 1)
        img = np.float32(cv2.resize(img, (448, 768))) /255

        input = preprocess_image(image_name)
        target_index = None
        mask = grad_cam(input, target_index)
        localization_result(img, mask, image_num)
