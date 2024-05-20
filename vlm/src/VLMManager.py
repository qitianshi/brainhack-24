from typing import List
from PIL import Image
from torchvision.transforms.functional import pil_to_tensor
import json
import torch
from transformers import Owlv2Processor, Owlv2ForObjectDetection
from typing import Dict, List, Optional, Tuple, Union
import random
from transformers.image_transforms import center_to_corners_format
from transformers.utils import TensorType
def post_process_object_detection( outputs, threshold: float = 0.1, target_sizes: Union[TensorType, List[Tuple]] = None,n = 1
):
    """
    Converts the raw output of [`OwlViTForObjectDetection`] into final bounding boxes in (top_left_x, top_left_y,
    bottom_right_x, bottom_right_y) format.

    Args:
        outputs ([`OwlViTObjectDetectionOutput`]):
            Raw outputs of the model.
        threshold (`float`, *optional*):
            Score threshold to keep object detection predictions.
        target_sizes (`torch.Tensor` or `List[Tuple[int, int]]`, *optional*):
            Tensor of shape `(batch_size, 2)` or list of tuples (`Tuple[int, int]`) containing the target size
            `(height, width)` of each image in the batch. If unset, predictions will not be resized.
    Returns:
        `List[Dict]`: A list of dictionaries, each dictionary containing the scores, labels and boxes for an image
        in the batch as predicted by the model.
    """
    # TODO: (amy) add support for other frameworks
    logits, boxes = outputs.logits, outputs.pred_boxes

    # if target_sizes is not None:
    #     if len(logits) != len(target_sizes):
    #         raise ValueError(
    #             "Make sure that you pass in as many target sizes as the batch dimension of the logits"
    #         )

    probs = torch.max(logits, dim=-1)
    scores = torch.sigmoid(probs.values)
    labels = probs.indices

    # Convert to [x0, y0, x1, y1] format
    boxes = center_to_corners_format(boxes)

    # Convert from relative [0, 1] to absolute [0, height] coordinates
    if target_sizes is not None:
        scale_fct = torch.tensor([[1520., 1520., 1520., 1520.] for i in range(n)], device='cuda:0')
        boxes = boxes * scale_fct[:, None, :]
        #print(boxes)

    results = []
    for s, l, b in zip(scores, labels, boxes):
        score = s[s > threshold]
        label = l[s > threshold]
        box = b[s > threshold]
        results.append({"scores": score, "labels": label, "boxes": box})

    return results
class VLMManager:
    def __init__(self):
        # initialize the model here
        self.device = torch.device('cuda') 
        self.processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16")
        self.model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16").cuda()
        for i in model.parameters():
            i.requires_grad= False
        pass

    def identify(self, imagebyte: bytes, caption: str) -> List[int]:
        # perform object detection with a vision-language model
        inputs = self.processor(text=caption, images=Image.open(imagebyte), return_tensors="pt").to(self.device)
        outputs=self.model(**inputs)
        results = post_process_object_detection(outputs=outputs, target_sizes=1, threshold=0.1,n=1)
        maxconfidence = 0
        bbox = []
        
        #print(groundtruths)
        for box, confidence, label in zip(boxes, scores, labels):
            box = torch.Tensor.tolist(box)
            #print(labels)
            
            if confidence>maxconfidence:
                bbox= box
                #print(maxscore,findOverlap(box),box)
                maxconfidence = confidence
        bbox = [int(i) for i in bbox]
        bbox[2]-=bbox[0]
        bbox[3]-=bbox[1]
        if bbox !=[]:
            return bbox
        else:
            return [0,0,0,0]
