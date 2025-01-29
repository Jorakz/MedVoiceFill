import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
import numpy as np
import librosa
import warnings
warnings.filterwarnings('ignore')

class WhisperTranscriber:
    def __init__(self):
        # Інціалізація моделі та процесора
        model_name = "openai/whisper-large-v3-turbo"
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)

        # Переміщення моделі на GPU якщо доступно
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

        # Встановлення розміру сегмента (30 секунд)
        self.segment_length = 30 * 16000  # 30 секунд при частоті 16кГц

    def split_audio(self, audio):
        """Розділення аудіо на сегменти з невеликим перекриттям"""
        segments = []
        overlap = 1 * 16000  # 1 секунда перекриття

        num_segments = len(audio) // self.segment_length + (1 if len(audio) % self.segment_length > 0 else 0)

        for i in range(num_segments):
            start = max(0, i * self.segment_length - overlap)
            end = min(len(audio), (i + 1) * self.segment_length + overlap)
            segment = audio[start:end]
            segments.append(segment)

        return segments

    def transcribe_segment(self, audio_segment):
        """Транскрибація окремого сегмента"""
        input_features = self.processor(
            audio_segment,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(self.device)

        forced_decoder_ids = self.processor.get_decoder_prompt_ids(
            language="ukrainian",
            task="transcribe"
        )

        predicted_ids = self.model.generate(
            input_features,
            forced_decoder_ids=forced_decoder_ids
        )

        transcription = self.processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]

        return transcription.strip()

    def transcribe(self, audio_path):
        try:
            print(f"Завантаження аудіофайлу: {audio_path}")
            # Завантаження аудіо з потрібною частотою дискретизації
            audio, _ = librosa.load(audio_path, sr=16000)

            print("Розділення аудіо на сегменти...")
            segments = self.split_audio(audio)

            print(f"Знайдено {len(segments)} сегментів. Починаємо транскрибацію...")

            # Транскрибація кожного сегмента
            transcriptions = []
            for i, segment in enumerate(segments, 1):
                print(f"Обробка сегменту {i}/{len(segments)}...")
                trans = self.transcribe_segment(segment)
                if trans:  # Додаємо тільки непусті транскрипції
                    transcriptions.append(trans)

            # Об'єднання всіх транскрипцій
            full_transcription = " ".join(transcriptions)

            return full_transcription
        except Exception as e:
            return f"Помилка при обробці аудіо: {str(e)}"

def audio_analize(audio_path):
    # Ініціалізація транскрайбера

    transcriber = WhisperTranscriber()

    # Отримання транскрипції
    print("Початок транскрибації...")
    transcription = transcriber.transcribe(audio_path)

    print("\nРезультат транскрибації:")
    print("-" * 50)
    print(transcription)
    print("-" * 50)
    return transcription