import torch
from torchvision.models import vgg
from torch.autograd import Variable
import torch.nn as nn
import time
import argparse


MODEL_LIST = {
    vgg: vgg.__all__[6:7]
}

precision=["single"]
device_name=torch.cuda.get_device_name(0)




torch.backends.cudnn.benchmark = True

def train(type='single'):
    """use fake image for training speed test"""
    img = Variable(torch.randn(16, 3, 224, 224)).cuda()
    target = Variable(torch.LongTensor(16).random_(args.NUM_CLASSES)).cuda()
    criterion = nn.CrossEntropyLoss()
    benchmark = {}
    for model_type in MODEL_LIST.keys():
        for model_name in MODEL_LIST[model_type]:
            model = getattr(model_type, model_name)(pretrained=False)
            model.cuda()
            model.train()
            for step in range(args.NUM_TEST):
                torch.cuda.synchronize()
                model.zero_grad()
                prediction = model.forward(img)
                loss = criterion(prediction, target)
                loss.backward()
                torch.cuda.synchronize()
            del model

    return benchmark

if __name__ == '__main__':
    train()
