"""
providers.py — All AI API Providers
Supports: OpenRouter, OpenAI, Anthropic, Google Gemini, Groq, Mistral, DeepSeek,
          Together AI, xAI Grok, Perplexity, Cohere
"""

import requests
import json

# ─────────────────────────────────────────────────────────
# PROVIDER DEFINITIONS
# ─────────────────────────────────────────────────────────

PROVIDERS = {

    # ═══════════════════════════════════════════
    # 🔀 OPENROUTER  (aggregates ALL providers)
    # ═══════════════════════════════════════════
    "🔀 OpenRouter": {
        "description": "Access 200+ models via one API key — Free & Paid",
        "get_key_url": "https://openrouter.ai/keys",
        "free_tier": "✅ 20 req/min · 200 req/day — No credit card",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-or-v1-...",
        "free_models": {
            "🎲 Auto Router ★ BEST — Never 404":                   "openrouter/free",
            "🦙 Llama 3.3 70B — Most Reliable":                    "meta-llama/llama-3.3-70b-instruct:free",
            "🟠 OpenAI GPT-OSS 120B — OpenAI Free":                "openai/gpt-oss-120b:free",
            "🔵 Qwen3 Coder 480B — Best for Tech":                 "qwen/qwen3-coder:free",
            "🔵 Qwen3 Next 80B — Latest Qwen":                     "qwen/qwen3-next-80b-a3b-instruct:free",
            "🟡 NVIDIA Nemotron 30B — MoE Powerful":               "nvidia/nemotron-3-nano-30b-a3b:free",
            "🟡 NVIDIA Nemotron 9B — Fast":                        "nvidia/nemotron-nano-9b-v2:free",
            "🌟 Gemma 3 27B — Best Google Free":                   "google/gemma-3-27b-it:free",
            "🌸 Gemma 3 12B — Google Balanced":                    "google/gemma-3-12b-it:free",
            "⚡ Mistral Small 3.1 24B — Fast":                     "mistralai/mistral-small-3.1-24b-instruct:free",
            "🟠 OpenAI GPT-OSS 20B — Light":                      "openai/gpt-oss-20b:free",
            "🦙 Llama 3.2 3B — Ultra Fast":                        "meta-llama/llama-3.2-3b-instruct:free",
            "🟣 StepFun Step 3.5 Flash — 256K Context":            "stepfun/step-3.5-flash:free",
            "🟣 Z.AI GLM 4.5 Air — Agent Model":                   "z-ai/glm-4.5-air:free",
            "🟣 Arcee Trinity Large — 400B MoE":                   "arcee-ai/trinity-large-preview:free",
            "🟣 Arcee Trinity Mini — Efficient":                   "arcee-ai/trinity-mini:free",
            "🟣 Solar Pro 3 — Upstage 102B":                       "upstage/solar-pro-3:free",
        },
        "paid_models": {
            "👑 Claude 3.5 Sonnet — Best Overall":                  "anthropic/claude-3.5-sonnet",
            "🧬 Claude 3.5 Haiku — Fastest Claude":                 "anthropic/claude-3.5-haiku",
            "💎 GPT-4o — Top Tier OpenAI":                         "openai/gpt-4o",
            "🚀 GPT-4o Mini — Fast & Cheap":                       "openai/gpt-4o-mini",
            "🌙 Gemini 2.0 Flash — Fast Google":                   "google/gemini-2.0-flash-001",
            "🧠 DeepSeek R1 — Best Reasoning":                     "deepseek/deepseek-r1",
            "💬 DeepSeek Chat — Low Cost":                         "deepseek/deepseek-chat",
            "⚡ Mistral Large — Powerful":                          "mistralai/mistral-large",
            "🔵 Qwen3 235B — Best Open Source":                    "qwen/qwen3-235b-a22b",
        },
        "headers_extra": {
            "HTTP-Referer": "https://ai-career-suite.streamlit.app",
            "X-Title": "AI Career Suite"
        }
    },

    # ═══════════════════════════════════════════
    # 💎 OPENAI  (GPT models)
    # ═══════════════════════════════════════════
    "💎 OpenAI": {
        "description": "Official OpenAI API — GPT-4o, GPT-4o Mini",
        "get_key_url": "https://platform.openai.com/api-keys",
        "free_tier": "⚠️ No free tier — ~$5 free credits for new accounts",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-proj-...",
        "free_models": {},
        "paid_models": {
            "💎 GPT-4o — Most Capable (~$2.5/$10 per M)":          "gpt-4o",
            "🚀 GPT-4o Mini — Fast & Cheap (~$0.15/$0.6 per M)":   "gpt-4o-mini",
            "🔮 GPT-4 Turbo — Reliable (~$10/$30 per M)":          "gpt-4-turbo",
            "🧠 o1 Mini — Reasoning Model (~$1.1/$4.4 per M)":     "o1-mini",
            "⚡ GPT-3.5 Turbo — Budget (~$0.5/$1.5 per M)":        "gpt-3.5-turbo",
        },
    },

    # ═══════════════════════════════════════════
    # 👑 ANTHROPIC  (Claude models)
    # ═══════════════════════════════════════════
    "👑 Anthropic (Claude)": {
        "description": "Official Claude API — Best for writing & analysis",
        "get_key_url": "https://console.anthropic.com/",
        "free_tier": "⚠️ No free tier — pay per use",
        "endpoint": "https://api.anthropic.com/v1/messages",
        "type": "anthropic",
        "placeholder": "sk-ant-api03-...",
        "free_models": {},
        "paid_models": {
            "👑 Claude 3.5 Sonnet — Best Overall (~$3/$15 per M)":  "claude-3-5-sonnet-20241022",
            "🧬 Claude 3.5 Haiku — Fastest (~$0.8/$4 per M)":      "claude-3-5-haiku-20241022",
            "💜 Claude 3 Opus — Most Powerful (~$15/$75 per M)":    "claude-3-opus-20240229",
            "⚡ Claude 3 Haiku — Budget (~$0.25/$1.25 per M)":      "claude-3-haiku-20240307",
        },
    },

    # ═══════════════════════════════════════════
    # 🌙 GOOGLE GEMINI
    # ═══════════════════════════════════════════
    "🌙 Google Gemini": {
        "description": "Official Gemini API — Free tier available!",
        "get_key_url": "https://aistudio.google.com/app/apikey",
        "free_tier": "✅ Free: 15 req/min · 1M tokens/day — No credit card",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
        "type": "gemini",
        "placeholder": "AIza...",
        "free_models": {
            "⚡ Gemini 2.0 Flash — FREE Fast & Smart":              "gemini-2.0-flash",
            "🌟 Gemini 1.5 Flash — FREE Reliable":                  "gemini-1.5-flash",
            "💡 Gemini 1.5 Flash 8B — FREE Ultra Fast":             "gemini-1.5-flash-8b",
        },
        "paid_models": {
            "🌙 Gemini 1.5 Pro — Long Context (~$1.25/$5 per M)":  "gemini-1.5-pro",
            "💫 Gemini 2.0 Flash Thinking — Reasoning":             "gemini-2.0-flash-thinking-exp",
        },
    },

    # ═══════════════════════════════════════════
    # ⚡ GROQ  (Ultra-fast inference, free tier)
    # ═══════════════════════════════════════════
    "⚡ Groq": {
        "description": "Ultra-fast inference — 10x faster than others, Free tier!",
        "get_key_url": "https://console.groq.com/keys",
        "free_tier": "✅ Free: 30 req/min · 14,400 req/day — No credit card",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "gsk_...",
        "free_models": {
            "🦙 Llama 3.3 70B — FREE Best Quality":                 "llama-3.3-70b-versatile",
            "🦙 Llama 3.1 8B — FREE Ultra Fast":                    "llama-3.1-8b-instant",
            "🌸 Gemma2 9B — FREE Google Model":                     "gemma2-9b-it",
            "⚡ Mixtral 8x7B — FREE MoE Model":                     "mixtral-8x7b-32768",
            "🦙 Llama 3.2 90B Vision — FREE Multimodal":            "llama-3.2-90b-vision-preview",
            "🦙 Llama 3.2 11B Vision — FREE Fast Vision":           "llama-3.2-11b-vision-preview",
            "🔮 DeepSeek R1 — FREE Reasoning":                      "deepseek-r1-distill-llama-70b",
        },
        "paid_models": {
            "🦙 Llama 3.1 70B — Paid Higher Limits":                "llama-3.1-70b-versatile",
        },
    },

    # ═══════════════════════════════════════════
    # 🧠 DEEPSEEK  (Best value, dirt cheap)
    # ═══════════════════════════════════════════
    "🧠 DeepSeek": {
        "description": "Best value AI — R1 reasoning & V3 chat, very cheap",
        "get_key_url": "https://platform.deepseek.com/api_keys",
        "free_tier": "⚠️ ~$5 free credits for new accounts",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-...",
        "free_models": {},
        "paid_models": {
            "🧠 DeepSeek R1 — Best Reasoning (~$0.55/$2.19 per M)": "deepseek-reasoner",
            "💬 DeepSeek V3 — Great Chat (~$0.27/$1.1 per M)":      "deepseek-chat",
        },
    },

    # ═══════════════════════════════════════════
    # ⚡ MISTRAL AI  (European AI, free tier)
    # ═══════════════════════════════════════════
    "⚡ Mistral AI": {
        "description": "European AI — Fast models, free trial available",
        "get_key_url": "https://console.mistral.ai/api-keys/",
        "free_tier": "✅ Free trial credits available",
        "endpoint": "https://api.mistral.ai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "...",
        "free_models": {},
        "paid_models": {
            "⚡ Mistral Large — Most Powerful (~$2/$6 per M)":       "mistral-large-latest",
            "🚀 Mistral Small — Fast (~$0.1/$0.3 per M)":           "mistral-small-latest",
            "💡 Mistral Nemo — Lightweight (~$0.15/$0.15 per M)":   "open-mistral-nemo",
            "🧠 Codestral — Best for Code (~$0.3/$0.9 per M)":      "codestral-latest",
        },
    },

    # ═══════════════════════════════════════════
    # 🔥 TOGETHER AI  (Open source models, cheap)
    # ═══════════════════════════════════════════
    "🔥 Together AI": {
        "description": "Run open-source models — $25 free credits!",
        "get_key_url": "https://api.together.xyz/settings/api-keys",
        "free_tier": "✅ $25 free credits on signup — No credit card",
        "endpoint": "https://api.together.xyz/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "...",
        "free_models": {},
        "paid_models": {
            "🦙 Llama 3.3 70B — Best Quality (~$0.88 per M)":       "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "🦙 Llama 3.2 3B — Ultra Cheap (~$0.06 per M)":         "meta-llama/Llama-3.2-3B-Instruct-Turbo",
            "🔵 Qwen 2.5 72B — Great (~$1.2 per M)":               "Qwen/Qwen2.5-72B-Instruct-Turbo",
            "🧠 DeepSeek R1 — Reasoning (~$2.19 per M)":            "deepseek-ai/DeepSeek-R1",
            "⚡ Mixtral 8x7B — Fast MoE (~$0.6 per M)":             "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "🌸 Gemma 2 27B — Google (~$0.8 per M)":               "google/gemma-2-27b-it",
        },
    },

    # ═══════════════════════════════════════════
    # 🌐 PERPLEXITY  (with web search!)
    # ═══════════════════════════════════════════
    "🌐 Perplexity": {
        "description": "AI with real-time web search built in!",
        "get_key_url": "https://www.perplexity.ai/settings/api",
        "free_tier": "⚠️ No free tier — pay per use (~$5 min)",
        "endpoint": "https://api.perplexity.ai/chat/completions",
        "type": "openai_compat",
        "placeholder": "pplx-...",
        "free_models": {},
        "paid_models": {
            "🌐 Sonar Pro — Best with Web Search (~$3/$15 per M)":  "sonar-pro",
            "🚀 Sonar — Fast with Web Search (~$1/$1 per M)":       "sonar",
            "🧠 Sonar Reasoning — Think + Search (~$1/$5 per M)":   "sonar-reasoning",
        },
    },

    # ═══════════════════════════════════════════
    # 🔥 XAI GROK  (Elon's AI)
    # ═══════════════════════════════════════════
    "🔥 xAI Grok": {
        "description": "xAI's Grok — Real-time X/Twitter knowledge",
        "get_key_url": "https://console.x.ai/",
        "free_tier": "✅ $25 free credits on signup",
        "endpoint": "https://api.x.ai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "xai-...",
        "free_models": {},
        "paid_models": {
            "🔥 Grok 3 — Most Capable (~$3/$15 per M)":             "grok-3",
            "⚡ Grok 3 Mini — Fast Reasoning (~$0.3/$0.5 per M)":   "grok-3-mini",
            "🚀 Grok 2 — Stable (~$2/$10 per M)":                   "grok-2-1212",
        },
    },

    # ═══════════════════════════════════════════
    # 🌊 COHERE  (Enterprise RAG, free tier)
    # ═══════════════════════════════════════════
    "🌊 Cohere": {
        "description": "Enterprise AI — Best for RAG & document analysis, Free!",
        "get_key_url": "https://dashboard.cohere.com/api-keys",
        "free_tier": "✅ Free trial — 20 req/min · 1000 req/month",
        "endpoint": "https://api.cohere.ai/v2/chat",
        "type": "cohere",
        "placeholder": "...",
        "free_models": {
            "🌊 Command R — FREE Best for RAG":                     "command-r",
            "💡 Command R7B — FREE Fast":                           "command-r7b-12-2024",
        },
        "paid_models": {
            "🌊 Command R+ — Best Quality (~$2.5/$10 per M)":       "command-r-plus",
            "⚡ Command Light — Ultra Fast (~$0.3/$0.6 per M)":     "command-light",
        },
    },

    # ═══════════════════════════════════════════
    # 🤗 HUGGING FACE  (Open source, free)
    # ═══════════════════════════════════════════
    "🤗 Hugging Face": {
        "description": "Open source models — Serverless Inference API, Free!",
        "get_key_url": "https://huggingface.co/settings/tokens",
        "free_tier": "✅ Free Inference API — Limited but no credit card",
        "endpoint": "https://api-inference.huggingface.co/models",
        "type": "huggingface",
        "placeholder": "hf_...",
        "free_models": {
            "🦙 Llama 3.1 8B — FREE Fast Meta Model":               "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "🌸 Gemma 2 9B — FREE Google Model":                    "google/gemma-2-9b-it",
            "🔵 Qwen 2.5 7B — FREE Qwen Model":                    "Qwen/Qwen2.5-7B-Instruct",
            "⚡ Mistral 7B — FREE Classic":                         "mistralai/Mistral-7B-Instruct-v0.3",
            "🧠 Phi 3.5 Mini — FREE Microsoft":                     "microsoft/Phi-3.5-mini-instruct",
        },
        "paid_models": {},
    },
}


def get_all_models_for_provider(provider_name: str):
    """Return (free_models_dict, paid_models_dict) for a provider."""
    p = PROVIDERS.get(provider_name, {})
    return p.get("free_models", {}), p.get("paid_models", {})


def call_api(provider_name: str, api_key: str, model_id: str,
             prompt: str, temperature: float = 0.7, max_tokens: int = 2500) -> str:
    """Universal API caller — handles all provider formats."""
    p = PROVIDERS[provider_name]
    ptype = p["type"]

    # ── OpenAI-Compatible (OpenRouter, Groq, DeepSeek, Mistral, Together, Perplexity, xAI) ──
    if ptype == "openai_compat":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        # Extra headers for OpenRouter
        if "headers_extra" in p:
            headers.update(p["headers_extra"])

        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["choices"][0]["message"]["content"].strip()

    # ── Anthropic Claude ──
    elif ptype == "anthropic":
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_id,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["content"][0]["text"].strip()

    # ── Google Gemini ──
    elif ptype == "gemini":
        url = f"{p['endpoint']}/{model_id}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
        }
        r = requests.post(url, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # ── Cohere ──
    elif ptype == "cohere":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["message"]["content"][0]["text"].strip()

    # ── Hugging Face Inference API ──
    elif ptype == "huggingface":
        url = f"{p['endpoint']}/{model_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": temperature, "return_full_text": False},
        }
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        _check_errors(r, provider_name)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)

    raise ValueError(f"Unknown provider type: {ptype}")


def _check_errors(r, provider_name: str):
    """Unified error handler for all providers."""
    if r.status_code == 200:
        return
    msg = ""
    try:
        err = r.json()
        msg = err.get("error", {}).get("message", "") or err.get("message", "") or str(err)
    except Exception:
        msg = r.text[:200]

    p = PROVIDERS.get(provider_name, {})

    if r.status_code == 401:
        raise ValueError(f"Invalid API key for {provider_name}. Get one at: {p.get('get_key_url','')}")
    elif r.status_code == 402:
        raise ValueError(f"No credits for {provider_name}. Add credits at: {p.get('get_key_url','')}")
    elif r.status_code == 404:
        raise ValueError(f"Model not found (404). Try a different model or use 🔀 OpenRouter Auto Router.")
    elif r.status_code == 429:
        raise ValueError(
            f"Rate limit hit on {provider_name}! "
            f"{p.get('free_tier','')}\n"
            "→ Wait 1 min, switch model, or use 🔀 OpenRouter Auto Router."
        )
    elif r.status_code == 503:
        raise ValueError(f"Model loading (503) — Try again in 20 seconds or switch to a different model.")
    else:
        raise ValueError(f"API error {r.status_code} from {provider_name}: {msg[:150]}")