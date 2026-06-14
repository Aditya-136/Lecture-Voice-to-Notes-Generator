import librosa
from transformers import pipeline

_transcriber = None

def _load_model():
    global _transcriber
    if _transcriber is None:
        _transcriber = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small"
        )
    return _transcriber


def convert_speech_to_text(audio_path: str) -> str:
    # Load audio via librosa so we're not dependent on a system ffmpeg binary.
    # Whisper expects 16 kHz mono float32.
    audio, _ = librosa.load(audio_path, sr=16000, mono=True)

    model = _load_model()
    result = model({"array": audio, "sampling_rate": 16000})
    return result["text"]
