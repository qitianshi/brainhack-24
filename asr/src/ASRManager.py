from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import io
import numpy as np
import soundfile as sf
from os import path

class ASRManager:
    def __init__(self):
        """model initialisation. using a finetuned openai/whisper-small.en model"""
        self.processor = WhisperProcessor.from_pretrained(path.join(path.dirname(path.abspath(__file__)), "model"))
        self.feature_extractor = self.processor.feature_extractor
        self.tokenizer = self.processor.tokenizer
        self.model = WhisperForConditionalGeneration.from_pretrained(path.join(path.dirname(path.abspath(__file__)), "model"))
        
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.model.to(device)

    def transcribe(self, audio_bytes: bytes) -> str:
        """perform ASR transcription on one audio represented as audio bytes"""
        
        # find some way to convert audio bytes into a format we can use
        # data = np.frombuffer(audio_bytes, dtype=np.float64)
        audio_file = io.BytesIO(audio_bytes)
        audio_data, sample_rate = sf.read(audio_file)
        
        # Convert audio to log-Mel spectrogram
        audio_input = self.processor.feature_extractor(audio_data, sampling_rate=sample_rate, return_tensors="pt").input_features

        # Perform inference
        generated_ids = self.model.generate(audio_input)

        # Decode the generated tokens
        transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return transcription
