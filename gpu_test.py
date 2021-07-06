#! /usr/bin/python3
import torch
from torchvision.models import vgg
from torch.autograd import Variable
import torch.nn as nn
import time
import argparse
import os

MODEL_LIST = {
    vgg: vgg.__all__[6:7]
}

precision=["single"]
device_name=torch.cuda.get_device_name(0)

# Training settings
parser = argparse.ArgumentParser(description='PyTorch Benchmarking')

parser.add_argument('--NUM_TEST','-n', type=int,default=2000000,required=False, help="Num of Test")
parser.add_argument('--BATCH_SIZE','-b', type=int, default=60, required=False, help='Num of batch size')
parser.add_argument('--NUM_CLASSES','-c', type=int, default=1000, required=False, help='Num of class')

args = parser.parse_args()
torch.backends.cudnn.benchmark = True
def train(type='single'):
    """use fake image for training speed test"""
    img = Variable(torch.randn(args.BATCH_SIZE, 3, 224, 224)).cuda()
    target = Variable(torch.LongTensor(args.BATCH_SIZE).random_(args.NUM_CLASSES)).cuda()
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

def inference(type='single'):
    benchmark = {}
    img = Variable(torch.randn(args.BATCH_SIZE, 3, 224, 224), requires_grad=True).cuda()
    with torch.no_grad():
        for model_type in MODEL_LIST.keys():
            for model_name in MODEL_LIST[model_type]:
                model = getattr(model_type, model_name)(pretrained=False)
                if type is 'double':
                    model=model.double()
                    img=img.double()
                elif type is 'single':
                    model=model.float()
                    img=img.float()
                elif type is 'half':
                    model=model.half()
                    img=img.half()
                model.cuda()
                model.eval()
                durations = []
                print('Benchmarking Inference '+type+' precision type %s ' % (model_name))
                for step in range(args.WARM_UP + args.NUM_TEST):
                    torch.cuda.synchronize()
                    start = time.time()
                    model.forward(img)
                    torch.cuda.synchronize()
                    end = time.time()
                    if step >= args.WARM_UP:
                        durations.append((end - start)*1000)
                del model
                benchmark[model_name] = durations
    return benchmark



if __name__ == '__main__':
    train()
