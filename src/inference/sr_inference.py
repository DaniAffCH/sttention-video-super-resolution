from __future__ import absolute_import
import torch
import tqdm
import cv2
from sr_utils.sr_utils import sanitizeInput, sanitizeGT
import os
from data.REDS_loader import REDS_loader
import albumentations as A
from model.generator import Generator
import numpy
import torchvision.transforms.functional

def inference(conf,num_vid,device,path):
    model = Generator(conf).to(device)
    model.load_state_dict(torch.load("trained_models/second_test_400x300"))

    model.eval()

    loader= REDS_loader(conf,A.Compose([]),"train")


    for i in range(100):
        img=loader. __getitem__(num_vid*100+i)["x"]

        for element,sample in enumerate(img):
            img[element]=torch.Tensor(img[element])
            img[element]=img[element].unsqueeze(1)
            img[element]=img[element].permute(1,3,2,0)
            img[element]=torchvision.transforms.functional.crop(img[element], 0, 0, 300, 400) 
            
        x = torch.stack(img,dim=0)
        x=x.permute(1,0,2,3,4).to(device)
        print(x.shape)
        Ohat = model(x)
        name = str(num_vid)+str(i)+'.png'
        print(name)
        filename=path+name
        cv2.imwrite(filename, numpy.array(Ohat.to("cpu").detach().numpy()))
        print("sweet home alabama")
        del Ohat
    return 
