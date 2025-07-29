"""
Multi-Model API Client
Supports multiple free/cheap AI models for code evaluation
"""

import json
import requests
import time
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class GradingResponse:
    """Response from grading engine"""

    success: bool
    grade: Optional[float] = None
    percentage: Optional[float] = None
    feedback: Optional[Dict[str, Any]] = None
    raw_response: str = ""
    processing_time: float = 0.0
    error_message: Optional[str] = None


class MultiModelClient:
    """Multi-model API client supporting various free/cheap AI models"""

    def __init__(
        self, api_key: str, model: str = "gpt-3.5-turbo", provider: str = "openai"
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider.lower()

        # Configure based on provider
        if self.provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        elif self.provider == "anthropic":
            self.base_url = "https://api.anthropic.com/v1/messages"
            self.headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }
        elif self.provider == "gemini":
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
            self.model_mapping = {
                "gemini-1.5-flash": "gemini-1.5-flash-latest",
                "gemini-1.5-pro": "gemini-1.5-pro-latest",
                "gemini-pro": "gemini-pro",
            }
        elif self.provider == "groq":
            # Groq offers free API with fast inference
            self.base_url = "https://api.groq.com/openai/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def evaluate_code(self, prompt: str) -> GradingResponse:
        """Send evaluation prompt to AI model and get response"""
        start_time = time.time()

        try:
            if self.provider == "openai":
                return self._call_openai(prompt, start_time)
            elif self.provider == "anthropic":
                return self._call_anthropic(prompt, start_time)
            elif self.provider == "gemini":
                return self._call_gemini(prompt, start_time)
            elif self.provider == "groq":
                return self._call_groq(prompt, start_time)
            else:
                return GradingResponse(
                    success=False,
                    error_message=f"Unsupported provider: {self.provider}",
                    processing_time=time.time() - start_time,
                )

        except Exception as e:
            return GradingResponse(
                success=False,
                error_message=f"Error calling {self.provider} API: {str(e)}",
                processing_time=time.time() - start_time,
            )

    def _call_openai(self, prompt: str, start_time: float) -> GradingResponse:
        """Call OpenAI API (GPT-3.5-turbo is free tier)"""
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 4000,
        }

        response = requests.post(
            self.base_url, json=payload, headers=self.headers, timeout=60
        )
        processing_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return GradingResponse(
                success=True, raw_response=content, processing_time=processing_time
            )
        else:
            return GradingResponse(
                success=False,
                error_message=f"OpenAI API error: {response.status_code} - {response.text}",
                processing_time=processing_time,
            )

    def _call_anthropic(self, prompt: str, start_time: float) -> GradingResponse:
        """Call Anthropic Claude API"""
        payload = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            self.base_url, json=payload, headers=self.headers, timeout=60
        )
        processing_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            content = data["content"][0]["text"]
            return GradingResponse(
                success=True, raw_response=content, processing_time=processing_time
            )
        else:
            return GradingResponse(
                success=False,
                error_message=f"Anthropic API error: {response.status_code} - {response.text}",
                processing_time=processing_time,
            )

    def _call_groq(self, prompt: str, start_time: float) -> GradingResponse:
        """Call Groq API (free and very fast)"""
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 4000,
        }

        response = requests.post(
            self.base_url, json=payload, headers=self.headers, timeout=60
        )
        processing_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return GradingResponse(
                success=True, raw_response=content, processing_time=processing_time
            )
        else:
            return GradingResponse(
                success=False,
                error_message=f"Groq API error: {response.status_code} - {response.text}",
                processing_time=processing_time,
            )

    def _call_gemini(self, prompt: str, start_time: float) -> GradingResponse:
        """Call Gemini API (original implementation)"""
        model_name = self.model_mapping.get(self.model, self.model)
        url = f"{self.base_url}/{model_name}:generateContent?key={self.api_key}"

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            },
        }

        response = requests.post(url, json=payload, timeout=60)
        processing_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            return GradingResponse(
                success=True, raw_response=content, processing_time=processing_time
            )
        else:
            error_msg = f"Gemini API error: {response.status_code} - {response.text}"
            return GradingResponse(
                success=False,
                error_message=error_msg,
                processing_time=processing_time,
            )

    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Gemini"""
        try:
            # Try to extract JSON from response if it's wrapped
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
            elif "```" in response_text:
                # Handle cases where it's just wrapped in code blocks
                start = response_text.find("```") + 3
                end = response_text.rfind("```")
                json_str = response_text[start:end].strip()
            else:
                json_str = response_text.strip()

            # Remove any language markers
            if json_str.startswith("json\n"):
                json_str = json_str[5:]

            return json.loads(json_str)

        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON response: {str(e)}",
                "raw_response": response_text,
            }

    def test_connection(self) -> GradingResponse:
        """Test the API connection"""
        test_prompt = "Respond with exactly: 'Connection successful'"
        response = self.evaluate_code(test_prompt)

        if response.success and "Connection successful" in response.raw_response:
            return GradingResponse(success=True, raw_response="Connection test passed")
        else:
            return GradingResponse(
                success=False,
                error_message=response.error_message or "Connection test failed",
            )


# Legacy alias for backward compatibility
GeminiClient = MultiModelClient
