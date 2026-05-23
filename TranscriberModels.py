import torch
from faster_whisper import WhisperModel
from openai import OpenAI

def get_model(use_api):
    if use_api:
        return APIWhisperTranscriber()
    else:
        return FasterWhisperTranscriber()

class FasterWhisperTranscriber:
    def __init__(self):
        print(f"[INFO] Loading Faster Whisper model...")
        # تغییر نام مدل به tiny.en و اصلاح کوتیشن‌ها
        # همچنین استفاده از float16 در صورت وجود GPU برای سرعت بیشتر
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if torch.cuda.is_available() else "int8"
        
        self.model = WhisperModel("base.en", device=device, compute_type=compute_type)
        print(f"[INFO] Faster Whisper using GPU: {torch.cuda.is_available()}")

    def get_transcription(self, wav_file_path):
        try:
            # تغییر beam_size به 1 برای رسیدن به حداکثر سرعت (مناسب برای tiny.en)
            segments, _ = self.model.transcribe(wav_file_path, beam_size=1)
            full_text = " ".join(segment.text for segment in segments)
            return full_text.strip()
        except Exception as e:
            print(f"Transcription error: {e}")
            return ''

class APIWhisperTranscriber:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)
    
    def get_transcription(self, wav_file_path):
        try:
            with open(wav_file_path, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return result.text.strip()
        except Exception as e:
            print(f"API Transcription error: {e}")
            return ''
