import os
from typing import Dict, Any, Optional

from openai import OpenAI


class LLMExplainer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def explain(self, data: Dict[str, Any]) -> str:
        if not self.client:
            return (
                "I can give you a concise explanation once an API key is configured. "
                f"For now, here is the gist: {data.get('summary', '')}"
            )

        prompt = (
            "You are a coffee brewing coach. "
            "Given the structured brew feedback below, write a short, practical explanation "
            "that helps the user improve their next pour-over. "
            f"Summary: {data.get('summary', '')}\n"
            f"Recommendation: {data.get('recommendation', '')}\n"
            f"Suggested changes: {', '.join(data.get('suggested_changes', []))}"
        )

        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                max_output_tokens=180,
            )
            return response.output_text.strip()
        except Exception:
            return (
                "The AI explanation service was unavailable, so I’m falling back to the structured guidance. "
                f"{data.get('recommendation', '')}"
            )
