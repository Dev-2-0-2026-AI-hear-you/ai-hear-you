import numpy as np
from scipy.signal import resample_poly
from math import gcd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
MODEL_SIZE = "base" # "base" is the default, "small" and above are better but take longer to transcribe

model = None

def transcribe_audio(audio_bytes, sample_rate=SAMPLE_RATE, language="en", initial_prompt=None):
    global model

    if sample_rate <= 0:
        raise ValueError("Invalid sample rate")

    audio = np.frombuffer(audio_bytes, dtype="<f4").copy()

    if audio.size == 0:
        return ""

    if not np.all(np.isfinite(audio)):
        raise ValueError("Audio contains invalid values")

    audio = np.clip(audio, -1.0, 1.0)

    if sample_rate != SAMPLE_RATE:
        divisor = gcd(sample_rate, SAMPLE_RATE)

        audio = resample_poly(
            audio,
            SAMPLE_RATE // divisor,
            sample_rate // divisor
        ).astype(np.float32)

    # Initialize model once
    if model is None:
        model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8",
            cpu_threads = 4,
            num_workers = 1
        )

    # Transcribe
    segments, info = model.transcribe(
        audio,
        language="en",
        beam_size=3,
        best_of=1,
        temperature=0,
        vad_filter=False,
        condition_on_previous_text=False
    )

    text = []

    for segment in segments:
        segment_text = segment.text.strip()

        if segment_text:
            text.append(segment_text)

    return " ".join(text).strip()
