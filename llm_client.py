import os
from pathlib import Path
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


def _read_custom_knowledge() -> str:
    knowledge_file = Path(__file__).resolve().parent / "custom_llm_knowledge.txt"
    if not knowledge_file.exists():
        return ""
    return knowledge_file.read_text(encoding="utf-8").strip()


class LLMClient:
    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.provider = (provider or os.getenv("LLM_PROVIDER", "ollama")).lower()
        self.model = model or self._get_model_name()
        self.base_url = base_url or self._get_base_url()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    def _get_model_name(self) -> str:
        if self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    def _get_base_url(self) -> str:
        if self.provider == "openai":
            return os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def _inject_custom_knowledge(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        custom_prompt = _read_custom_knowledge()
        if not custom_prompt:
            return messages

        prompt_text = (
            "You are MyBuilder AI, a custom local website and AI product builder. "
            "Use the following memory before answering: "
            f"{custom_prompt}"
        )

        for message in messages:
            if message.get("role") == "system":
                message["content"] = f"{prompt_text}\n\n{message['content']}"
                return messages

        messages.insert(0, {"role": "system", "content": prompt_text})
        return messages

    def chat(self, messages: List[Dict[str, str]]) -> str:
        messages = self._inject_custom_knowledge(messages)
        if self.provider == "ollama":
            return self._chat_with_ollama(messages)
        if self.provider == "openai":
            return self._chat_with_openai(messages)
        raise ValueError(f"Unsupported provider: {self.provider}")

    def _chat_with_ollama(self, messages: List[Dict[str, str]]) -> str:
        payload = {"model": self.model, "messages": messages, "stream": False}
        response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        if "response" in data:
            return str(data["response"]).strip()
        raise ValueError(f"Unexpected Ollama response: {data}")

    def _chat_with_openai(self, messages: List[Dict[str, str]]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "messages": messages, "temperature": 0.7}
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise ValueError(f"Unexpected OpenAI response: {data}")
        return choices[0]["message"]["content"].strip()


if __name__ == "__main__":
    client = LLMClient()
    print(client.chat([{"role": "user", "content": "Say hello in one sentence."}]))
