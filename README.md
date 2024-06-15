# dingdongs: BrainHack TIL-AI 2024
"dingdongs" can be traced back to Old English and Middle Dutch. The term "ding" originates from the Old English "dingan," meaning to strike or hit, often used to describe the sound of a bell. The term "dong" comes from the Middle Dutch "donckus," which refers to the sound a duck makes when hitting the water at or above the von Plonck ducking velocity. Combining these elements, "dingdongs" represents a harmonious and impactful sound, symbolizing our aim to make a resonant impact at BrainHack 2024.

Here you'll find our submission repo with full inference code and model weights (as [release assets](https://github.com/qitianshi/brainhack-24/releases)). Training code is available at [qitianshi/brainhack-24-training](https://github.com/qitianshi/brainhack-24-training) (invite required).

## Methodology
Competition task:
1. Given a noisy audio input, perform automatic speech recognition to obtain the transcript.
2. Using the transcript, perform natural language processing to extract key information (tool, heading, and target).
3. Using the heading and target, rotate a turret on the robot and use a vision language model to locate the requested target in the field of view.

Testing scores:
* ASR
  * Accuracy: 0.9997
  * Speed: 0.8045
* NLP
  * Accuracy: 1.0000
  * Speed: 0.8636
* VLM
  * Accuracy: 0.9250
  * Speed: 0.7919

### Automatic speech recognition
ASR was performed using the [openai/whisper-small.en](https://huggingface.co/openai/whisper-small.en) model, fine-tuned with audio datasets with moderate noise augmentation. A simple regex-based validation was performed on the ASR output, and non-matching results were error-corrected using a combination of algorithmic and model-based methods.

The heading, being guaranteed to follow a structured format (three numerical words), was corrected algorithmically by looking up the pronunciation of the erroneous text in the CMU Pronouncing Dictionary, and calculating its Levenshtein distance to the pronunciations of of known words, with tuned edit weights to favor maintaining stressed vowel sounds (which are less likely to be misheard than consonants, especially plosives). Because this method directly utilizes phonetic information, it was found to perform better than model-based methods for fitting erroneous ASR outputs to a known set of correct words, including complex multi-word corrections (e.g. "toothy" to "two three").

To correct other errors, the [facebook/bart-base](https://huggingface.co/facebook/bart-base) seq2seq model was fine-tuned using a dataset based on the provided training data, augmented with mispronounced words generated from CMUdict (using the reverse of the correction method), and original datasets generated using ChatGPT-4o. The model effectively restored multiple misheard and missing marker words ("heading is", "tool to deploy is", "target is"). `difflib.SequenceMatcher` was used to preserve the original heading numerals for the more specialized Levenshtein distance-based correction algorithm.

### Natural language processing
The NLP task, being extremely simple for the Novice category, was performed using simple regex parsing:

```regex
/heading\s+is([a-zA-Z\s,\-]+?)\s*(?=tool\s+to\s+deploy\s+is|target\s+is|\.|$)/gi
/tool\s+to\s+deploy\s+is([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|target\s+is|\.|$)/gi
/target\s+is([a-zA-Z\s,\-]+?)\s*(?=heading\s+is|tool\s+to\s+deploy\s+is|\.|$)/gi
```

Because the ASR correction module ensures that all outputs match the above output format, fallback QA model-based approaches, as employed by most other teams, were judged to be unnecessary and not worth the tradeoff in build and inference speed.

### Vision language model
The VLM task was performed using [AILab-CVC/YOLO-World](https://github.com/AILab-CVC/YOLO-World) and [openai/clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14). A fine-tuned YOLO-World model was used for object detection, producing candidate bounding boxes around potential targets; these were passed to a fine-tuned CLIP model to identify the requested target.

The YOLO-World model was fine-tuned using the provided dataset with light augmentations such as blurring, random degree rotation, and flipping, as they were judged to most closely mirror the augmentations used for the competition dataset. YOLO-World was chosen over other evaluated methods (including RT-DETR, DETR, and YOLOv8) for its superior robustness to labeling errors and shorter training times. Our initial approach involved using an OWL-ViT v2 model, which performed well owing to its zero-shot capabilities; however, its recency and the complexity of its loss function posed significant challenges, as it easily collapsed during training.

Due to YOLO-World's tendency to misclassify objects, CLIP was used in conjunction with YOLO-World for target identification. OpenAI's ViT-L/14 pre-trained model was used as the base model for fine-tuning, as it offered a suitable balance of accuracy and speed to fit within the competition's runtime constraints.

## Future work
The impressive accuracy of the phonetic Levenshtein distance-based algorithmic error correction approach suggests it could be effective for other transcript error correction besides the heading, notably the marker words ("heading is", "tool to deploy is", and "target is"), possibly using a rolling window to identify the sequence of phonemes that are closest in edit distance.

For the VLM task, a coded-in but unimplemented color analysis algorithm was devised to identify the prominent colors of the proposed bounding box and verify that they match the requested colors. The bounding box was analyzed pixel-wise by converting their RGB color values to HSV (a more natural and representative color encoding method for our purposes) and matching the constituent colors to a predefined set of color words. For similar future tasks, we conceive of a possible methodology that first performs edge detection to isolate the target from its background, thus making the algorithm more robust to background noise.

To more effectively guard against post-competition depression arising from errors induced by 4am caffeine-influenced coding, linters shall be incorporated into future competition development pipelines. The use of such tools, conceivably via CI/CD services, may assist in ensuring that critical imports, such as `torch`, are not overlooked in the haze of early-morning coding marathons. This strategy is hoped to save ambitious teams from future debugging nightmares and post-competition alcoholism.

## Acknowledgements
Our brilliant and dedicated team &mdash; Qi Tianshi [@qitianshi](https://github.com/qitianshi), Brian Hu [@BrianHuBuyan](https://github.com/BrianHuBuyan), Neo Souw Chuan [@neosouwchuan](https://github.com/neosouwchuan), and Tew En Hao [@tewenhao](https://github.com/tewenhao).

Ryan Nah [@ryan-tribex](https://github.com/ryan-tribex) and the teams at AngelHack and DSTA, for putting together an awesome event.

The open source communities behind the models and code that made this project possible.

## License
Copyright 2024 Qi Tianshi, Brian Hu, Neo Souw Chuan, and Tew En Hao. All rights reserved.

This is proprietary software &mdash; it's neither open source nor freely available. [See the license.](/LICENSE)

---

Built in the small hours by Qi Tianshi, with Brian Hu, Neo Souw Chuan, and Tew En Hao.

<p align="center" markdown="1">🧠</p>
