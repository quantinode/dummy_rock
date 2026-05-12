import json
import requests
from django.conf import settings


class LLMClient:
    """Multi-provider LLM client with fallback: Groq → OpenRouter → Gemini"""

    def __init__(self):
        self.providers = []
        if settings.GROQ_API_KEY:
            self.providers.append(('groq', settings.GROQ_API_KEY))
        if settings.OPENROUTER_API_KEY:
            self.providers.append(('openrouter', settings.OPENROUTER_API_KEY))
        if settings.GEMINI_API_KEY:
            self.providers.append(('gemini', settings.GEMINI_API_KEY))

    def chat(self, messages: list, system: str = '', max_tokens: int = 1024,
             temperature: float = 0.7) -> dict:
        """Try each provider in order until one succeeds."""
        last_error = None
        for provider, api_key in self.providers:
            try:
                if provider == 'groq':
                    return self._call_groq(api_key, messages, system, max_tokens, temperature)
                elif provider == 'openrouter':
                    return self._call_openrouter(api_key, messages, system, max_tokens, temperature)
                elif provider == 'gemini':
                    return self._call_gemini(api_key, messages, system, max_tokens, temperature)
            except Exception as e:
                last_error = e
                continue
        raise last_error or Exception("No LLM providers configured")

    def stream_chat(self, messages: list, system: str = '', max_tokens: int = 1024,
                    temperature: float = 0.7):
        """Stream from first available provider. Yields text chunks."""
        last_error = None
        for provider, api_key in self.providers:
            try:
                if provider == 'groq':
                    yield from self._stream_groq(api_key, messages, system, max_tokens, temperature)
                    return
                elif provider == 'openrouter':
                    yield from self._stream_openrouter(api_key, messages, system, max_tokens, temperature)
                    return
                elif provider == 'gemini':
                    # Gemini doesn't stream easily via REST, do full call and yield
                    result = self._call_gemini(api_key, messages, system, max_tokens, temperature)
                    yield result['text']
                    return
            except Exception as e:
                last_error = e
                continue
        raise last_error or Exception("No LLM providers configured")

    # ─── Groq ─────────────────────────────────────────────────────────────────

    def _build_messages(self, messages, system):
        msgs = []
        if system:
            msgs.append({'role': 'system', 'content': system})
        msgs.extend(messages)
        return msgs

    def _call_groq(self, api_key, messages, system, max_tokens, temperature):
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': self._build_messages(messages, system),
                'max_tokens': max_tokens,
                'temperature': temperature,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        choice = data['choices'][0]
        usage = data.get('usage', {})
        return {
            'text': choice['message']['content'],
            'input_tokens': usage.get('prompt_tokens', 0),
            'output_tokens': usage.get('completion_tokens', 0),
            'stop_reason': choice.get('finish_reason', ''),
        }

    def _stream_groq(self, api_key, messages, system, max_tokens, temperature):
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'llama-3.1-8b-instant',
                'messages': self._build_messages(messages, system),
                'max_tokens': max_tokens,
                'temperature': temperature,
                'stream': True,
            },
            stream=True,
            timeout=30,
        )
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: ') and line != 'data: [DONE]':
                    chunk = json.loads(line[6:])
                    delta = chunk['choices'][0].get('delta', {})
                    if 'content' in delta and delta['content']:
                        yield delta['content']

    # ─── OpenRouter ───────────────────────────────────────────────────────────

    def _call_openrouter(self, api_key, messages, system, max_tokens, temperature):
        resp = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                'messages': self._build_messages(messages, system),
                'max_tokens': max_tokens,
                'temperature': temperature,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        choice = data['choices'][0]
        usage = data.get('usage', {})
        return {
            'text': choice['message']['content'],
            'input_tokens': usage.get('prompt_tokens', 0),
            'output_tokens': usage.get('completion_tokens', 0),
            'stop_reason': choice.get('finish_reason', ''),
        }

    def _stream_openrouter(self, api_key, messages, system, max_tokens, temperature):
        resp = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                'messages': self._build_messages(messages, system),
                'max_tokens': max_tokens,
                'temperature': temperature,
                'stream': True,
            },
            stream=True,
            timeout=30,
        )
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: ') and line != 'data: [DONE]':
                    chunk = json.loads(line[6:])
                    delta = chunk['choices'][0].get('delta', {})
                    if 'content' in delta and delta['content']:
                        yield delta['content']

    # ─── Gemini ───────────────────────────────────────────────────────────────

    def _call_gemini(self, api_key, messages, system, max_tokens, temperature):
        # Build Gemini contents format
        contents = []
        for msg in messages:
            role = 'user' if msg['role'] == 'user' else 'model'
            contents.append({'role': role, 'parts': [{'text': msg['content']}]})

        body = {
            'contents': contents,
            'generationConfig': {
                'maxOutputTokens': max_tokens,
                'temperature': temperature,
            },
        }
        if system:
            body['systemInstruction'] = {'parts': [{'text': system}]}

        resp = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}',
            headers={'Content-Type': 'application/json'},
            json=body,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data['candidates'][0]['content']['parts'][0]['text']
        usage = data.get('usageMetadata', {})
        return {
            'text': text,
            'input_tokens': usage.get('promptTokenCount', 0),
            'output_tokens': usage.get('candidatesTokenCount', 0),
            'stop_reason': 'stop',
        }


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Estimate cost — most of these providers are free/cheap, return minimal cost."""
    return 0.0


# Singleton client
_llm_client = None


def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


# Backward-compatible alias
get_bedrock_client = get_llm_client


# ─── System Prompts per AI topic ──────────────────────────────────────────────
SYSTEM_PROMPTS = {
    'default': """You are an AI learning assistant for AI Lab — an interactive platform teaching 
AI from basics to agentic systems. You explain concepts clearly, use analogies, 
and provide code examples. Be concise, educational, and engaging.""",

    'ai_basics': """You are an AI expert teaching AI fundamentals. Explain neural networks, 
ML concepts, and deep learning with clear analogies and visual explanations. 
Use beginner-friendly language but include technical depth when asked.""",

    'rag': """You are a RAG architecture expert. Help users understand retrieval-augmented 
generation, vector databases, chunking strategies, re-ranking, and how to build 
production RAG systems. Include practical examples and real-world considerations.""",

    'agent': """You are an agentic AI expert. Explain multi-agent systems, planning, 
tool use, memory management, ReAct patterns, and CrewAI-style frameworks. 
Help users understand autonomous AI agent design.""",

    'llm': """You are an LLM systems expert. Help users understand transformer architecture, 
attention mechanisms, tokenization, fine-tuning, prompt engineering, and LLM optimization. 
Discuss production concerns like latency, cost, and reliability.""",
}
