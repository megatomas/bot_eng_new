"""
Speech providers — TTS (Text-to-Speech) and STT (Speech-to-Text).

Бесплатные решения:
- TTS: edge-tts (Microsoft Edge) — бесплатный, качественный, много голосов
- TTS: gTTS (Google) — простой, но роботизированный
- STT: Whisper (OpenAI) — локальный, бесплатный, очень точный
- STT: Vosk — офлайн, лёгкий
"""

from abc import ABC, abstractmethod
from pathlib import Path
import asyncio
import os
import tempfile


# ============================================================
# TTS PROVIDERS
# ============================================================

class TTSProvider(ABC):
    """Interface for Text-to-Speech providers."""
    
    @abstractmethod
    async def synthesize(self, text: str, lang: str = "en") -> bytes:
        """Convert text to audio bytes (MP3)."""
        pass
    
    @abstractmethod
    async def synthesize_to_file(self, text: str, filepath: str, lang: str = "en") -> str:
        """Convert text to audio file."""
        pass


class EdgeTTSProvider(TTSProvider):
    """
    Microsoft Edge TTS — ЛУЧШИЙ бесплатный вариант.
    
    Преимущества:
    - Полностью бесплатный
    - Очень качественное произношение
    - Много голосов (мужские/женские)
    - Нейросетевые голоса
    - Поддержка SSML
    
    Голоса:
    - en-US-JennyNeural (женский, американский)
    - en-US-GuyNeural (мужской, американский)
    - en-GB-SoniaNeural (женский, британский)
    - en-GB-RyanNeural (мужской, британский)
    """
    
    def __init__(self, voice: str = "en-US-JennyNeural"):
        self.voice = voice
        self.rate = "+0%"  # Скорость: -50% до +100%
        self.volume = "+0%"
    
    async def synthesize(self, text: str, lang: str = "en") -> bytes:
        """Convert text to audio bytes."""
        try:
            import edge_tts
        except ImportError:
            raise ImportError(
                "edge-tts not installed. Run: pip install edge-tts"
            )
        
        # Choose voice based on language
        voice = self._get_voice(lang)
        
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=self.rate,
            volume=self.volume,
        )
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    
    async def synthesize_to_file(self, text: str, filepath: str, lang: str = "en") -> str:
        """Convert text to audio file."""
        audio_data = await self.synthesize(text, lang)
        
        with open(filepath, "wb") as f:
            f.write(audio_data)
        
        return filepath
    
    def _get_voice(self, lang: str) -> str:
        """Get appropriate voice for language."""
        voices = {
            "en": self.voice,
            "en-US": "en-US-JennyNeural",
            "en-GB": "en-GB-SoniaNeural",
            "ru": "ru-RU-SvetlanaNeural",
        }
        return voices.get(lang, self.voice)
    
    async def list_voices(self, lang: str = "en") -> list[dict]:
        """List available voices."""
        try:
            import edge_tts
            voices = await edge_tts.list_voices()
            return [v for v in voices if v["Locale"].startswith(lang)]
        except Exception:
            return []


class GTTSProvider(TTSProvider):
    """
    Google TTS — простой, но роботизированный.
    Уже используется в старом боте.
    """
    
    async def synthesize(self, text: str, lang: str = "en") -> bytes:
        try:
            from gtts import gTTS
        except ImportError:
            raise ImportError("gTTS not installed. Run: pip install gTTS")
        
        tts = gTTS(text=text, lang=lang, slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            tmp_path = tmp.name
        
        with open(tmp_path, "rb") as f:
            audio_data = f.read()
        
        os.unlink(tmp_path)
        return audio_data
    
    async def synthesize_to_file(self, text: str, filepath: str, lang: str = "en") -> str:
        try:
            from gtts import gTTS
        except ImportError:
            raise ImportError("gTTS not installed")
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        return filepath


# ============================================================
# STT PROVIDERS
# ============================================================

class STTProvider(ABC):
    """Interface for Speech-to-Text providers."""
    
    @abstractmethod
    async def transcribe(self, audio_data: bytes, lang: str = "en") -> str:
        """Convert audio to text."""
        pass
    
    @abstractmethod
    async def transcribe_file(self, filepath: str, lang: str = "en") -> str:
        """Convert audio file to text."""
        pass


class WhisperProvider(STTProvider):
    """
    OpenAI Whisper — ЛУЧШИЙ бесплатный STT.
    
    Преимущества:
    - Полностью бесплатный (локальный)
    - Очень точный
    - Поддерживает много языков
    - Разные модели (tiny, base, small, medium, large)
    
    Модели:
    - tiny: ~39 MB, быстрый, менее точный
    - base: ~74 MB, хороший баланс
    - small: ~244 MB, точный
    - medium: ~769 MB, очень точный
    - large: ~1550 MB, максимальная точность
    
    Для бота рекомендую: base или small
    """
    
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self._model = None
    
    def _load_model(self):
        """Lazy load Whisper model."""
        if self._model is None:
            try:
                import whisper
            except ImportError:
                raise ImportError(
                    "Whisper not installed. Run: pip install openai-whisper"
                )
            
            self._model = whisper.load_model(self.model_name)
        
        return self._model
    
    async def transcribe(self, audio_data: bytes, lang: str = "en") -> str:
        """Convert audio bytes to text."""
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name
        
        try:
            result = await self.transcribe_file(tmp_path, lang)
            return result
        finally:
            os.unlink(tmp_path)
    
    async def transcribe_file(self, filepath: str, lang: str = "en") -> str:
        """Convert audio file to text."""
        model = self._load_model()
        
        # Run in thread to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: model.transcribe(filepath, language=lang)
        )
        
        return result["text"].strip()


class VoskProvider(STTProvider):
    """
    Vosk — лёгкий офлайн STT.
    
    Преимущества:
    - Полностью офлайн
    - Очень быстрый
    - Лёгкий (модели ~50 MB)
    
    Недостатки:
    - Менее точный чем Whisper
    """
    
    def __init__(self, model_path: str = "vosk-model-small-en-us-0.15"):
        self.model_path = model_path
        self._model = None
    
    def _load_model(self):
        if self._model is None:
            try:
                from vosk import Model
            except ImportError:
                raise ImportError("Vosk not installed. Run: pip install vosk")
            
            self._model = Model(self.model_path)
        
        return self._model
    
    async def transcribe(self, audio_data: bytes, lang: str = "en") -> str:
        # Vosk requires WAV format
        # For simplicity, save to file and transcribe
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name
        
        try:
            return await self.transcribe_file(tmp_path, lang)
        finally:
            os.unlink(tmp_path)
    
    async def transcribe_file(self, filepath: str, lang: str = "en") -> str:
        import json
        import wave
        from vosk import KaldiRecognizer
        
        model = self._load_model()
        recognizer = KaldiRecognizer(model, 16000)
        
        wf = wave.open(filepath, "rb")
        
        result_text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                result_text += result.get("text", "") + " "
        
        final = json.loads(recognizer.FinalResult())
        result_text += final.get("text", "")
        
        return result_text.strip()


# ============================================================
# FACTORY
# ============================================================

def get_tts_provider() -> TTSProvider:
    """Get configured TTS provider."""
    provider = os.getenv("TTS_PROVIDER", "edge").lower()
    
    if provider == "edge":
        return EdgeTTSProvider()
    elif provider == "gtts":
        return GTTSProvider()
    else:
        raise ValueError(f"Unknown TTS provider: {provider}")


def get_stt_provider() -> STTProvider:
    """Get configured STT provider."""
    provider = os.getenv("STT_PROVIDER", "whisper").lower()
    
    if provider == "whisper":
        return WhisperProvider(model_name="base")
    elif provider == "vosk":
        return VoskProvider()
    else:
        raise ValueError(f"Unknown STT provider: {provider}")
