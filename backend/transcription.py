import numpy as np
import sounddevice as sd
import queue
import threading

from scipy.signal import resample_poly
from math import gcd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
MODEL_SIZE = "base" # "base" is the default, "small" and above are better but take longer to transcribe
CHUNK_SECONDS = 5

model = None

audio_queue = None
microphone = None
worker_thread = None
is_recording = False

state_lock = threading.Lock()

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
            cpu_threads=4,
            num_workers=1
        )

    # Transcribe
    '''
    segments, info = model.transcribe(
        audio,
        language=language,
        beam_size=3,
        best_of=1,
        temperature=0,
        vad_filter=False,
        condition_on_previous_text=False
    )
    '''
    segments, info = model.transcribe(
        audio,
        language=language,
        beam_size=3,
        best_of=1,
        temperature=0,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        no_speech_threshold=0.6,
        condition_on_previous_text=False
    )
    audio = np.clip(audio, -1.0, 1.0)
    if np.sqrt(np.mean(audio ** 2)) < 0.005: # If professor speaks quiet, lower 0.005
        return ""

    text = []

    for segment in segments:
        segment_text = segment.text.strip()

        if segment_text:
            text.append(segment_text)

    return " ".join(text).strip()


def _transcription_worker(audio_queue, sample_rate, on_transcription):
    buffered_audio = []
    buffered_samples = 0
    chunk_size = int(sample_rate * CHUNK_SECONDS)

    def process_chunk(audio):
        try:
            audio_bytes = audio.astype("<f4", copy=False).tobytes()
            result = transcribe_audio(audio_bytes, sample_rate)

            if result:
                on_transcription(result)

        except Exception as error:
            print(f"Transcription error: {error}")

    while True:
        audio = audio_queue.get()

        if audio is None:
            break

        buffered_audio.append(audio)
        buffered_samples += len(audio)

        if buffered_samples >= chunk_size:
            combined = np.concatenate(buffered_audio)
            offset = 0

            while len(combined) - offset >= chunk_size:
                current_chunk = combined[offset:offset + chunk_size]
                process_chunk(current_chunk)
                offset += chunk_size

            leftover = combined[offset:]
            buffered_audio = [leftover] if len(leftover) else []
            buffered_samples = len(leftover)

    if buffered_samples > 0:
        remaining_audio = np.concatenate(buffered_audio)
        process_chunk(remaining_audio)


def start(on_transcription=None, device=None):
    global audio_queue, microphone, worker_thread, is_recording

    if on_transcription is None:
        on_transcription = lambda text: print(text, flush=True)

    with state_lock:
        if is_recording:
            raise RuntimeError("Transcription is already running.")

        device_info = sd.query_devices(device, kind="input")

        if device_info["max_input_channels"] < 1:
            raise RuntimeError("No microphone input is available.")

        sample_rate = int(round(device_info["default_samplerate"]))

        audio_queue = queue.Queue()
        current_queue = audio_queue

        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"Microphone warning: {status}")

            current_queue.put(indata[:, 0].copy())

        microphone = sd.InputStream(
            device=device,
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            callback=audio_callback
        )

        worker_thread = threading.Thread(
            target=_transcription_worker,
            args=(current_queue, sample_rate, on_transcription),
            daemon=True
        )

        is_recording = True
        worker_thread.start()

        try:
            microphone.start()
        except Exception:
            current_queue.put(None)
            worker_thread.join()
            microphone.close()
            microphone = None
            worker_thread = None
            audio_queue = None
            is_recording = False
            raise

    #print("Microphone recording started.")
    return sample_rate


def stop():
    global audio_queue, microphone, worker_thread, is_recording

    with state_lock:
        if not is_recording:
            return

        current_queue = audio_queue
        current_microphone = microphone
        current_worker = worker_thread

        current_microphone.stop()
        current_microphone.close()

        current_queue.put(None)

    current_worker.join()

    with state_lock:
        microphone = None
        audio_queue = None
        worker_thread = None
        is_recording = False

    #print("Microphone recording stopped.")
