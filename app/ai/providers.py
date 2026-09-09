"""
AI Provider Interface + Free implementations.

Бесплатные провайдеры:
- Groq (Llama 3.3) — лучший выбор, быстрый и качественный
- Google Gemini — бесплатный tier
- OpenRouter — есть бесплатные модели
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator
import os


class LLMProvider(ABC):
    """Interface for LLM providers."""
    
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Send messages and get response."""
        pass
    
    @abstractmethod
    async def check_answer(
        self,
        user_answer: str,
        correct_answer: str,
        context: str = "",
    ) -> dict:
        """Check if user's answer is acceptable."""
        pass
    
    @abstractmethod
    async def explain_error(
        self,
        user_input: str,
        expected: str,
        user_level: str = "A2",
    ) -> str:
        """Explain user's error in simple terms."""
        pass


class GroqProvider(LLMProvider):
    """
    Groq provider — БЕСПЛАТНЫЙ, быстрый, качественный.
    
    Получи API ключ: https://console.groq.com/
    Бесплатно: 30 req/min, 14400 req/day
    Модель: llama-3.3-70b-versatile (как GPT-4)
    """
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
        self.base_url = "https://api.groq.com/openai/v1"
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not set. "
                "Get free key at https://console.groq.com/"
            )
    
    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Chat with Groq."""
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    
    async def check_answer(
        self,
        user_answer: str,
        correct_answer: str,
        context: str = "",
    ) -> dict:
        """Check if answer is acceptable (allows minor variations)."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an English teacher checking student answers. "
                    "Accept minor spelling/grammar variations if meaning is clear. "
                    "Respond in JSON: {\"correct\": bool, \"feedback\": str}"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Expected: {correct_answer}\n"
                    f"Student answered: {user_answer}\n"
                    f"Context: {context or 'general'}\n\n"
                    "Is this acceptable? Reply in JSON only."
                ),
            },
        ]
        
        response = await self.chat(messages, temperature=0.1, max_tokens=100)
        
        try:
            import json
            # Try to extract JSON from response
            if "{" in response:
                json_str = response[response.index("{"):response.rindex("}") + 1]
                return json.loads(json_str)
        except Exception:
            pass
        
        # Fallback: simple string comparison
        return {
            "correct": user_answer.lower().strip() == correct_answer.lower().strip(),
            "feedback": response,
        }
    
    async def explain_error(
        self,
        user_input: str,
        expected: str,
        user_level: str = "A2",
    ) -> str:
        """Explain error in simple terms matching user's level."""
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a friendly English teacher. "
                    f"Student level: {user_level}. "
                    "Explain errors briefly (2-3 sentences max). "
                    "Use simple words. Give one example. "
                    "Write in Russian with English examples."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Student wrote: '{user_input}'\n"
                    f"Correct: '{expected}'\n\n"
                    "Explain the mistake briefly."
                ),
            },
        ]
        
        return await self.chat(messages, temperature=0.3, max_tokens=200)
    
    async def converse(
        self,
        messages: list[dict],
        user_level: str = "A2",
        known_words: list[str] | None = None,
    ) -> str:
        """AI conversation partner."""
        system_prompt = f"""
You are a friendly English conversation partner for a Russian speaker.
Student level: {user_level}

RULES:
1. Use simple vocabulary matching their level
2. Keep responses short (1-3 sentences)
3. Ask follow-up questions to keep conversation going
4. If they make a mistake, gently correct it like this:
   "Better: [correct version]"
   Then continue the conversation naturally
5. Don't lecture — just chat!
6. Use common phrases and contractions (I'm, you're, gonna)
"""
        
        if known_words:
            system_prompt += f"\n\nStudent knows these words: {', '.join(known_words[:50])}"
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        return await self.chat(full_messages, temperature=0.8, max_tokens=150)


class GeminiProvider(LLMProvider):
    """
    Google Gemini — бесплатный tier.
    
    Получи API ключ: https://aistudio.google.com/apikey
    Бесплатно: 15 RPM, 1M tokens/day (Gemini 1.5 Flash)
    """
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = "gemini-1.5-flash"
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")
    
    async def chat(self, messages: list[dict], **kwargs) -> str:
        import aiohttp
        
        # Convert to Gemini format
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                continue  # Gemini doesn't support system
            contents.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}],
            })
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"contents": contents}) as resp:
                data = await resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def check_answer(self, user_answer, correct_answer, context=""):
        # Simple implementation
        return {
            "correct": user_answer.lower().strip() == correct_answer.lower().strip(),
            "feedback": "",
        }
    
    async def explain_error(self, user_input, expected, user_level="A2"):
        return f"Correct: {expected}"


def get_llm_provider() -> LLMProvider:
    """Get configured LLM provider."""
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    if provider == "groq":
        return GroqProvider()
    elif provider == "gemini":
        return GeminiProvider()
    else:
        raise ValueError(f"Unknown provider: {provider}")
