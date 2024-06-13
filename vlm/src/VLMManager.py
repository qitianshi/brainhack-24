import torch
import clip
from PIL import Image
import random
import os
from os import listdir, path
from os.path import isfile, join
import io
from torchvision import transforms

print([f for f in os.listdir('.') if os.path.isfile(f)])
print(os.getcwd())

from ultralytics import YOLOWorld
class VLMManager:
    def __init__(self):
        # initialize the model here
        self.device = 'cuda'
        self.clippreprocess = transforms.Compose([
            transforms.Resize(size=224, interpolation=transforms.InterpolationMode("bicubic"), max_size=None, antialias=True),
            transforms.CenterCrop(size=(224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.48145466, 0.4578275, 0.40821073), std=(0.26862954, 0.26130258,0.27577711))
        ])
        print(os.getcwd())
        print([f for f in os.listdir('.') if os.path.isfile(f)])
        self.clipmodel= torch.load(path.join(path.dirname(path.abspath(__file__)), "clip_ft_final.pt"))
        self.objects = ["cargo aircraft","light aircraft","commercial aircraft","drone","missile","helicopter","fighter jet","fighter plane"]
        self.model = YOLOWorld(path.join(path.dirname(path.abspath(__file__)), "highdegree60.pt")).to(self.device)
        for i in self.clipmodel.parameters():
            i.requires_grad=False
        for i in self.model.parameters():
            i.requires_grad=False
        pass

    def identify(self, imagebyte: bytes, caption: str):
        # perform object detection with a vision-language model
        inputimage = Image.open(io.BytesIO(imagebyte))
        out = self.model.predict(inputimage,conf=0.01)
        for currindex,i in enumerate(self.objects):
            if i in caption:
                groundcat = currindex
        groundbox = [440, 112, 52, 36]
        classlist = out[0].boxes.cls.tolist()
        possible = []
        for indexx,i in enumerate(classlist):
            if i == groundcat:
                possible.append(indexx)
        bestindex = -1
        bboxlist = out[0].boxes.xyxyn.tolist()
        tokenizedtext = clip.tokenize([caption]).to(self.device)
        clipprob = []
        maxscore = 0
        for chosenindex in range(len(bboxlist)):
            bbox = bboxlist[chosenindex]
            bbox[0]*=1520
            bbox[1]*=870
            bbox[2]*=1520
            bbox[3]*=870
            deltax = bbox[2]-bbox[0]
            deltay = bbox[3]-bbox[1]
            # bbox[0]-=deltax/2
            # bbox[1]-=deltay/2
            # bbox[2]-=deltax/2
            # bbox[3]-=deltay/2
            croppedimage = inputimage.crop(bbox)
            croppedimage = self.clippreprocess(croppedimage).unsqueeze(0).to(self.device)
            logits_per_image, logits_per_text = self.clipmodel(croppedimage, tokenizedtext)
            probs = logits_per_image.cpu().detach().numpy()
            if probs[0][0] > maxscore:
                maxscore = probs[0][0]
                bestindex = chosenindex
                bestbbox = bbox.copy()
        #print(bestbbox,groundbox,bestindex)
        if bestindex == -1:
            bestbbox = random.choice(bboxlist)
        bestbbox[2] -= bestbbox[0]
        bestbbox[3] -= bestbbox[1]
        for i in range(4):
            bestbbox[i] = int(bestbbox[i])
        try:
            return bestbbox
        except:
            return [0,0,0,0]