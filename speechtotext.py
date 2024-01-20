import logging
from transformers import AutoProcessor, pipeline, AutoModelForSpeechSeq2Seq
import torch
import os
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpeechToTextPipeline:
    def __init__(self, model_id: str = "openai/whisper-large-v3", language: str = "english"):
        self.model = None
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Using device: {self.device}")

        if self.model is None:
            self.load_model(model_id)
        else:
            logging.info("Model already loaded.")

        self.language = language

    def load_model(self, model_id: str = "openai/whisper-large-v3"):
        logging.info("Loading model...")
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch.float16, low_cpu_mem_usage=False, use_safetensors=True)
        self.model.to(self.device)
        logging.info("Model loaded successfully.")

    def transcribe_audio(self, audio_path: str):
        processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
        pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            torch_dtype=torch.float16,
            chunk_length_s=30,
            max_new_tokens=128,
            batch_size=24,
            return_timestamps=True,
            device=self.device,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            model_kwargs={"use_flash_attention_2": True},
            generate_kwargs={"language": self.language},
        )
        logging.info("Transcribing audio...")
        result = pipe(audio_path)["text"]
        return result


audio_path = "audio/deneme.mp3"
speech_to_text = SpeechToTextPipeline(language="english")
transcribed_text = speech_to_text.transcribe_audio(audio_path)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
file_path = f'texts/transcription_{timestamp}.txt'

with open(file_path, 'w', encoding='utf-8') as file:
    # Metni dosyaya yaz
    file.write(transcribed_text)

