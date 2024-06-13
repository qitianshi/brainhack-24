import torch
import clip
from PIL import Image
import random
import os
from os import listdir, path
from os.path import isfile, join
import io
from torchvision import transforms
import numpy as np

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
        self.colours = ['grey', 'green', 'white', 'black', 'red', 'blue', 'yellow', 'silver', 'brown', 'orange',"gws"]
    
    @staticmethod
    def color_distrib(inputimage: Image):
        all_colors = ['gws', 'green', 'black', 'red', 'blue', 'yellow', 'brown', 'orange']

        known_colors = {
            'red': [(205, 255), (0, 10)],
            'orange': [(11, 28)],
            'yellow': [(29, 49)],
            'green': [(50, 120)],
            'blue': [(121, 204)],
        }

        # weird_colors = {
        #     'gws': [(21, 100)],        # grey, white, silver
        #     'black': [(0, 51)],
        #     'brown': [(40, 70)],
        # }

        # black: any hue and saturation with brightness < threshold
        # gws: any hue with low saturation and high brightness
        # orange: hue fits in the orange range and saturation is > threshold and the brightness is in some range

        # Convert image to HSV
        hsv_image = inputimage.convert('HSV')
        hsv_pixels = np.array(hsv_image)

        # print(hsv_pixels)

        # Initialize color counts
        color_counts = {color: 0 for color in all_colors}
        total_pixels = hsv_pixels.shape[0] * hsv_pixels.shape[1]

        # Iterate through each pixel
        for pixel in hsv_pixels.reshape(-1, 3):
            hue, sat, val = pixel

            # print(val, end=' ') #debugging

            if val < 60:                  #check for black
                color_counts['black'] += 1

            elif sat < 15:
                color_counts['gws'] += 1

            else:
                for color, ranges in known_colors.items():
                    for lower, upper in ranges:
                        if lower <= hue <= upper:
                            if color == 'orange':
                                if val < 153:
                                    color_counts['brown'] += 1
                                else:
                                    color_counts['orange'] += 1
                            else:
                                color_counts[color] += 1


        # Calculate the percentage of each color
        color_percentages = {color: count / total_pixels for color, count in color_counts.items()}

        return color_percentages
    
    def identify(self, imagebyte: bytes, caption: str):
        # perform object detection with a vision-language model
        inputimage = Image.open(io.BytesIO(imagebyte))
        out = self.model.predict(inputimage,conf=0.1)
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
        scorearr = []
        for chosenindex in range(len(bboxlist)):
            bbox = bboxlist[chosenindex]
            bbox[0]*=1520
            bbox[1]*=870
            bbox[2]*=1520
            bbox[3]*=870
            deltax = bbox[2]-bbox[0]
            deltay = bbox[3]-bbox[1]
            # bbox[0]+=deltax/2
            # bbox[1]+=deltay/2
            # bbox[2]+=deltax/2
            # bbox[3]+=deltay/2
            croppedimage = inputimage.crop(bbox)
            croppedimage = self.clippreprocess(croppedimage).unsqueeze(0).to(self.device)
            logits_per_image, logits_per_text = self.clipmodel(croppedimage, tokenizedtext)
            probs = logits_per_image.cpu().detach().numpy()
            # if probs[0][0] > maxscore:
            #     maxscore = probs[0][0]
            #     bestindex = chosenindex
            #     bestbbox = bbox.copy()
            
            scorearr.append((bbox.copy(), probs[0][0]))
            
        scorearr.sort(key=lambda x: x[1], reverse=True)
            
        #print(bestbbox,groundbox,bestindex)
        if len(bboxlist) == 0 :
            return [0,0,0,0]
        if bestindex == -1:
            bestbbox = random.choice(bboxlist)
        bestbbox[2] -= bestbbox[0]
        bestbbox[3] -= bestbbox[1]
        for i in range(4):
            bestbbox[i] = int(bestbbox[i])
            
        colourspresent = []        # prompted colors
        for i in self.colours:
            if i in caption:
                if i not in ["grey","white",'silver'] and i not in colourspresent:
                    colourspresent.append(i)
                if i in ["grey","white",'silver'] and "gws" not in colourspresent:
                    colourspresent.append("gws")
                    
        for i in scorearr[:3]:
            
            bestbbox = i[0]
            bestcropped = inputimage.crop((bestbbox[0],bestbbox[1],bestbbox[2]+bestbbox[0],bestbbox[3]+bestbbox[1]))
            foundcolour = self.color_distrib(bestcropped)
        
            weird = ["gws", "black"]
            missingcolour = False
            for i in colourspresent:
                
                if i in weird and foundcolour[i] < 0.08:
                    missingcolour = True

                elif i not in weird and foundcolour[i] < 0.02:
                    missingcolour = True

            if not missingcolour:
                return bestbbox
            
        return scorearr[0][0]
