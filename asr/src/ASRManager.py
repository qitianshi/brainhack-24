from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import io
import soundfile as sf
from os import path
import re
import correction

class ASRManager:
    
    def __init__(self):
        """model initialisation. using a finetuned openai/whisper-small.en model"""
        self.processor = WhisperProcessor.from_pretrained(path.join(path.dirname(path.abspath(__file__)), "model"))
        self.feature_extractor = self.processor.feature_extractor
        self.tokenizer = self.processor.tokenizer
        self.model = WhisperForConditionalGeneration.from_pretrained(path.join(path.dirname(path.abspath(__file__)), "model"))
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

    def transcribe(self, audio_bytes: bytes) -> str:
        """perform ASR transcription on one audio represented as audio bytes"""
        
        # find some way to convert audio bytes into a format we can use
        # data = np.frombuffer(audio_bytes, dtype=np.float64)
        audio_file = io.BytesIO(audio_bytes)
        audio_data, sample_rate = sf.read(audio_file)
        
        # Convert audio to log-Mel spectrogram
        audio_input = self.processor.feature_extractor(audio_data, sampling_rate=sample_rate, return_tensors="pt").input_features
        
        # perform inference on GPU
        audio_input = audio_input.to(self.device)

        # Perform inference
        with torch.no_grad():
            generated_ids = self.model.generate(audio_input)

        # Decode the generated tokens
        transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        transcription = correction.reconstruct_transcript(correction.parse_transcript(transcription))
        
        return transcription
