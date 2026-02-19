"""
analyzer.py - AI-powered resume analysis using OpenRouter API
Supports 100+ models including free and paid options.
"""

import re
import json
import requests
import pdfplumber
from io import BytesIO


# ─────────────────────────────────────────────
# AVAILABLE MODELS ON OPENROUTER
# ─────────────────────────────────────────────

FREE_MODELS = {
    # ── 🏆 Best for Resume Analysis ──
    "🏆 Llama 3.3 70B — Best for Resume (Recommended)":    "meta-llama/llama-3.3-70b-instruct:free",
    "🧠 DeepSeek R1 0528 — Best Reasoning":                "deepseek/deepseek-r1-0528:free",
    "⚡ Mistral Small 3.1 24B — Fast & Smart":             "mistralai/mistral-small-3.1-24b-instruct:free",
    "🌟 Gemma 3 27B — Google Model":                       "google/gemma-3-27b-it:free",

    # ── 🤖 Qwen Models ──
    "🔵 Qwen3 Coder — Best for Coding":                    "qwen/qwen3-coder:free",
    "🔵 Qwen3 4B — Lightweight & Fast":                    "qwen/qwen3-4b:free",

    # ── 🟢 Meta Llama Models ──
    "🟢 Llama 3.2 3B — Fastest Free Model":               "meta-llama/llama-3.2-3b-instruct:free",
    "🟢 Nous Hermes 3 Llama 405B — Huge Model":           "nousresearch/hermes-3-llama-3.1-405b:free",

    # ── 🔴 Google Models ──
    "🔴 Gemma 3 12B — Google Balanced":                    "google/gemma-3-12b-it:free",
    "🔴 Gemma 3 4B — Google Lightweight":                  "google/gemma-3-4b-it:free",
    "🔴 Gemma 3n E4B — Google Nano":                       "google/gemma-3n-e4b-it:free",
    "🔴 Gemma 3n E2B — Google Ultra Nano":                 "google/gemma-3n-e2b-it:free",

    # ── 🟡 NVIDIA Models ──
    "🟡 NVIDIA Nemotron 30B — Powerful":                   "nvidia/nemotron-3-nano-30b-a3b:free",
    "🟡 NVIDIA Nemotron 12B Vision — Multimodal":          "nvidia/nemotron-nano-12b-v2-vl:free",
    "🟡 NVIDIA Nemotron 9B — Balanced":                    "nvidia/nemotron-nano-9b-v2:free",

    # ── 🟠 OpenAI Open Source ──
    "🟠 OpenAI GPT-OSS 120B — OpenAI Free":               "openai/gpt-oss-120b:free",
    "🟠 OpenAI GPT-OSS 20B — OpenAI Lightweight":         "openai/gpt-oss-20b:free",

    # ── 🟣 Other Models ──
    "🟣 StepFun Step 3.5 Flash — 256K Context":           "stepfun/step-3.5-flash:free",
    "🟣 Arcee Trinity Large — Reasoning":                  "arcee-ai/trinity-large-preview:free",
    "🟣 Arcee Trinity Mini — Lightweight":                  "arcee-ai/trinity-mini:free",
    "🟣 Solar Pro 3 — Upstage Model":                      "upstage/solar-pro-3:free",
    "🟣 Z.AI GLM 4.5 Air — 131K Context":                 "z-ai/glm-4.5-air:free",
    "🟣 Dolphin Mistral 24B — Uncensored":                 "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    "🟣 LiquidAI LFM 2.5 Thinking — Reasoning":           "liquid/lfm-2.5-1.2b-thinking:free",
    "🟣 LiquidAI LFM 2.5 Instruct — Fast":                "liquid/lfm-2.5-1.2b-instruct:free",

    # ── 🎲 Auto Router ──
    "🎲 Auto Free Router — Let OpenRouter Pick":           "openrouter/free",
}

PAID_MODELS = {
    "👑 Claude 3.5 Sonnet — Best Overall":   "anthropic/claude-3.5-sonnet",
    "💎 GPT-4o — Top Tier":                  "openai/gpt-4o",
    "🚀 GPT-4o Mini — Fast & Cheap":         "openai/gpt-4o-mini",
    "🌙 Gemini 2.0 Flash — Latest Google":   "google/gemini-2.0-flash-001",
    "🧬 Claude 3 Haiku — Fastest Paid":      "anthropic/claude-3-haiku",
    "🔮 Llama 3.3 70B — Best Open Source":   "meta-llama/llama-3.3-70b-instruct",
}

ALL_MODELS = {**FREE_MODELS, **PAID_MODELS}


def get_model_id(display_name: str) -> str:
    return ALL_MODELS.get(display_name, display_name)


def extract_text_from_pdf(uploaded_file) -> str:
    text = ""
    try:
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not read PDF: {str(e)}")

    if not text.strip():
        raise ValueError("No text found in PDF. Make sure it's not a scanned image.")

    return text.strip()


def analyze_resume(api_key: str, model_id: str, resume_text: str,
                   job_description: str, job_title: str = "", company_name: str = "") -> dict:

    prompt = f"""You are an expert ATS (Applicant Tracking System) and career coach AI.
Analyze the following resume against the job description and provide a detailed evaluation.

JOB TITLE: {job_title or "Not specified"}
COMPANY: {company_name or "Not specified"}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis ONLY as valid JSON (no markdown, no extra text) in this exact format:
{{
  "ats_score": <integer 0-100, how well the resume will pass ATS systems>,
  "match_score": <integer 0-100, overall match to job requirements>,
  "matched_skills": [<list of skills/keywords found in both resume and JD>],
  "missing_skills": [<list of important skills/keywords in JD but missing from resume>],
  "strengths": [<3-5 specific strengths of this resume for this role>],
  "improvements": [<4-6 specific, actionable improvements the candidate should make>],
  "keyword_suggestions": [<5-8 exact keywords/phrases to add to resume for better ATS>],
  "experience_gap": "<brief analysis of experience level match>",
  "education_match": "<brief analysis of education requirements match>",
  "overall_summary": "<2-3 sentence honest assessment of this application chances>",
  "quick_wins": [<2-3 things they can fix in 10 minutes to immediately improve the resume>]
}}

Be specific, honest, and actionable."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-resume-analyzer.streamlit.app",
        "X-Title": "AI Resume Analyzer"
    }

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 401:
            raise ValueError("Invalid OpenRouter API key. Get a free key at: https://openrouter.ai/keys")
        elif response.status_code == 402:
            raise ValueError("Insufficient credits for this paid model. Use a free model or add credits at openrouter.ai")
        elif response.status_code == 429:
            raise ValueError("Rate limit hit. Please wait 30 seconds and try again.")
        elif response.status_code != 200:
            raise ValueError(f"API error {response.status_code}: {response.text[:200]}")

        data = response.json()
        raw = data["choices"][0]["message"]["content"].strip()

        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)

        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            raw = json_match.group()

        result = json.loads(raw)

        defaults = {
            "ats_score": 0, "match_score": 0, "matched_skills": [],
            "missing_skills": [], "strengths": [], "improvements": [],
            "keyword_suggestions": [], "experience_gap": "",
            "education_match": "", "overall_summary": "", "quick_wins": []
        }
        for key, default in defaults.items():
            result.setdefault(key, default)

        result["ats_score"]   = max(0, min(100, int(result["ats_score"])))
        result["match_score"] = max(0, min(100, int(result["match_score"])))

        return result

    except json.JSONDecodeError:
        raise ValueError("AI returned an invalid response. Try again or switch to a different model.")
    except requests.Timeout:
        raise ValueError("Request timed out. Try a faster model like Gemini 2.0 Flash.")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Analysis failed: {str(e)}")


def get_score_color(score: int) -> str:
    if score >= 75: return "#00C851"
    elif score >= 50: return "#ffbb33"
    else: return "#ff4444"


def get_score_label(score: int) -> str:
    if score >= 80: return "Excellent ✅"
    elif score >= 65: return "Good 👍"
    elif score >= 50: return "Fair ⚠️"
    else: return "Needs Work ❌"