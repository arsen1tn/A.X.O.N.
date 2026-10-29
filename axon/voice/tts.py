import os
import re
import tempfile
import wave
from pathlib import Path

from langdetect import DetectorFactory, detect
from piper import PiperVoice

from axon.core.logger import logger

try:
    import winsound
except ImportError:
    winsound = None

DetectorFactory.seed = 0

MODELS_DIR = Path(__file__).parent / "models"

# language code -> Piper voice file in axon/voice/models/
# To add a language: download its voice (.onnx and .onnx.json) and add one line here.
VOICES = {
    "en": "en_GB-northern_english_male-medium.onnx",
    "ru": "ru_RU-ruslan-medium.onnx",
}
DEFAULT_LANG = "en"


class TextToSpeech:
    def __init__(self, voices=None, default_lang=DEFAULT_LANG):
        self.voices = voices or VOICES
        self.default_lang = default_lang
        self._loaded = {}

    def _clean(self, text: str) -> str:
        # Remove things that sound bad when read aloud
        text = re.sub(r"```.*?```", " ", text, flags=re.S)      # code blocks
        text = re.sub(r"`([^`]*)`", r"\1", text)                 # inline code
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)     # [text](url) -> text
        text = re.sub(r"https?://\S+", " ", text)                # bare links
        text = re.sub(r"^\s*[-*]\s+", ", ", text, flags=re.M)    # bullet points
        text = re.sub(r"[*#_>~|]", " ", text)                    # markdown symbols
        return re.sub(r"\s+", " ", text).strip()

    def _detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return self.default_lang

    def _get_voice(self, lang: str):
        if lang not in self.voices:
            logger.info(f"No voice for language '{lang}', using '{self.default_lang}'")
            lang = self.default_lang

        if lang not in self._loaded:
            model_path = MODELS_DIR / self.voices[lang]
            if not model_path.exists():
                raise FileNotFoundError(f"Voice file not found: {model_path}")
            self._loaded[lang] = PiperVoice.load(str(model_path))
        return self._loaded[lang]

    def speak(self, text: str) -> None:
        if winsound is None:
            raise RuntimeError("Playback uses winsound, which is Windows-only.")

        text = self._clean(text)
        if not text:
            return

        lang = self._detect_language(text)
        voice = self._get_voice(lang)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav_path = f.name
        try:
            with wave.open(wav_path, "wb") as wav_file:
                voice.synthesize_wav(text, wav_file)
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        finally:
            os.remove(wav_path)


if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak("Hello, sir, I am AXON. Voice is working.")
    tts.speak("Приветствую, сэр, я AXON. Голос работает.")