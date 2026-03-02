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
    # ── ⭐ Auto Router ──
    "🎲 Auto Free Router — Let OpenRouter Pick Best (Recommended)": "openrouter/free",

    # ── 🦙 Meta Llama ──
    "🦙 Llama 3.3 70B — Reliable & Fast (128K)":                   "meta-llama/llama-3.3-70b-instruct:free",
    "🦙 Llama 3.2 3B — Ultra Fast (131K)":                         "meta-llama/llama-3.2-3b-instruct:free",
    "🦙 Nous Hermes 3 Llama 405B — Huge Model (131K)":             "nousresearch/hermes-3-llama-3.1-405b:free",

    # ── 🧠 DeepSeek ──
    "🧠 DeepSeek R1 — Best Reasoning (Free)":                      "deepseek/deepseek-r1:free",

    # ── 🌟 Google ──
    "🌟 Gemma 3 27B — Best Google Free (131K)":                    "google/gemma-3-27b-it:free",
    "🌸 Gemma 3 12B — Google Balanced (33K)":                      "google/gemma-3-12b-it:free",
    "🌸 Gemma 3 4B — Google Lightweight (33K)":                    "google/gemma-3-4b-it:free",
    "🌸 Gemma 3n E4B — Google Nano (8K)":                          "google/gemma-3n-e4b-it:free",
    "🌸 Gemma 3n E2B — Google Ultra Nano (8K)":                    "google/gemma-3n-e2b-it:free",

    # ── 🔵 Qwen ──
    "🔵 Qwen3 Coder 480B — Best for Coding (262K)":               "qwen/qwen3-coder:free",
    "🔵 Qwen3 Next 80B — Latest Qwen (262K)":                     "qwen/qwen3-next-80b-a3b-instruct:free",
    "🔵 Qwen3 4B — Fast & Lightweight (41K)":                     "qwen/qwen3-4b:free",

    # ── 🟠 OpenAI Open Source ──
    "🟠 OpenAI GPT-OSS 120B — OpenAI Free Flagship (131K)":       "openai/gpt-oss-120b:free",
    "🟠 OpenAI GPT-OSS 20B — OpenAI Free Light (131K)":           "openai/gpt-oss-20b:free",

    # ── ⚡ Mistral ──
    "⚡ Mistral Small 3.1 24B — Fast & Multimodal (128K)":         "mistralai/mistral-small-3.1-24b-instruct:free",

    # ── 🟡 NVIDIA ──
    "🟡 NVIDIA Nemotron 30B — Powerful (256K)":                    "nvidia/nemotron-3-nano-30b-a3b:free",
    "🟡 NVIDIA Nemotron 12B Vision — Multimodal (128K)":           "nvidia/nemotron-nano-12b-v2-vl:free",
    "🟡 NVIDIA Nemotron 9B — Balanced (128K)":                     "nvidia/nemotron-nano-9b-v2:free",

    # ── 🟣 Other ──
    "🟣 StepFun Step 3.5 Flash — Huge Context (256K)":            "stepfun/step-3.5-flash:free",
    "🟣 Solar Pro 3 — Upstage Model (128K)":                       "upstage/solar-pro-3:free",
    "🟣 Z.AI GLM 4.5 Air — Long Context (131K)":                   "z-ai/glm-4.5-air:free",
    "🟣 Arcee Trinity Large — Reasoning (131K)":                   "arcee-ai/trinity-large-preview:free",
    "🟣 Arcee Trinity Mini — Lightweight (131K)":                  "arcee-ai/trinity-mini:free",
    "🟣 LiquidAI LFM 2.5 Thinking — Reasoning (33K)":             "liquid/lfm-2.5-1.2b-thinking:free",
    "🟣 LiquidAI LFM 2.5 Instruct — Fast (33K)":                  "liquid/lfm-2.5-1.2b-instruct:free",
    "🟣 Dolphin Mistral 24B — Uncensored (33K)":                   "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
}

PAID_MODELS = {
    # ── 👑 Anthropic Claude ──
    "👑 Claude Sonnet 4.6 — Best Mid-Range ($3/$15)":              "anthropic/claude-sonnet-4-6",
    "💜 Claude Opus 4.6 — Most Powerful ($5/$25)":                 "anthropic/claude-opus-4-6",
    "🧬 Claude Haiku 4.5 — Fastest Claude ($1/$5)":               "anthropic/claude-haiku-4-5",
    "🔵 Claude 3.5 Sonnet — Proven Reliable ($3/$15)":            "anthropic/claude-3.5-sonnet",

    # ── 💎 OpenAI ──
    "💎 GPT-5.2 — OpenAI Flagship ($1.75/$14)":                   "openai/gpt-5.2",
    "🚀 GPT-4o — Top Tier Stable ($2.5/$10)":                     "openai/gpt-4o",
    "⚡ GPT-4o Mini — Fast & Cheap ($0.15/$0.6)":                  "openai/gpt-4o-mini",
    "🔮 GPT-5 Mini — Budget GPT-5 ($0.25/$2)":                    "openai/gpt-5-mini",

    # ── 🌙 Google Gemini ──
    "🌙 Gemini 3.1 Pro — Latest Google ($2/$12)":                  "google/gemini-3.1-pro",
    "🌙 Gemini 2.5 Pro — Google Premium ($1.25/$10)":              "google/gemini-2.5-pro",
    "⚡ Gemini 2.5 Flash — Fast Google ($0.15/$0.6)":              "google/gemini-2.5-flash",
    "💫 Gemini 2.0 Flash — Stable Google ($0.1/$0.4)":            "google/gemini-2.0-flash-001",

    # ── 🧠 DeepSeek ──
    "🧠 DeepSeek R1 — Best Reasoning Paid ($0.55/$2.19)":         "deepseek/deepseek-r1",
    "💬 DeepSeek V3.2 — Frontier at Low Cost ($0.25/$0.38)":      "deepseek/deepseek-v3.2",

    # ── ⚡ xAI Grok ──
    "⚡ Grok 4 Fast — Ultra Cheap ($0.2/$1)":                      "x-ai/grok-4-fast",
    "🔥 Grok 4 — xAI Flagship ($3/$15)":                          "x-ai/grok-4",

    # ── 🔵 Qwen Paid ──
    "🔵 Qwen3 235B — Best Open Source Paid":                      "qwen/qwen3-235b-a22b",

    # ── ⚡ Mistral Paid ──
    "⚡ Mistral Large — Powerful ($2/$6)":                          "mistralai/mistral-large",
    "⚡ Mistral Small — Cheap ($0.1/$0.3)":                        "mistralai/mistral-small",
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

    prompt = f"""You are a senior technical recruiter and career coach with 15+ years of experience at top MNC companies (Google, Amazon, Microsoft, TCS, Infosys). You have deep knowledge of:
- How ATS (Applicant Tracking Systems) like Workday, Greenhouse, Lever, and Taleo score resumes
- What hiring managers actually look for in tech candidates in 2025
- Real salary and hiring trends from job market data
- Common reasons candidates get rejected at each stage
- What separates candidates who get interviews from those who don't

Analyze this resume against the job description with the precision of a real recruiter making a hiring decision today.

JOB TITLE: {job_title or "Not specified"}
COMPANY: {company_name or "Not specified"}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Apply these real-world recruiter insights in your analysis:
1. ATS systems reject 75% of resumes before human review - check for exact keyword matches
2. Recruiters spend avg 6-7 seconds on first resume scan - check if key info is immediately visible
3. Quantified achievements (numbers, %, $) are 40% more likely to pass screening
4. Skills listed but not demonstrated in experience are red flags
5. Job hopping (< 1 year at multiple companies) raises concerns
6. GitHub/portfolio links dramatically increase callbacks for tech roles
7. GPA matters less than projects and internships for experienced candidates
8. F1 visa / work authorization status affects hiring - US companies need OPT/CPT mention
9. Buzzwords without context (e.g. "passionate", "hardworking") waste valuable space
10. Cloud certifications (AWS, GCP, Azure) significantly boost tech resume scores in 2025

Based on this expert knowledge, provide ONLY valid JSON (no markdown, no extra text):
{{
  "ats_score": <integer 0-100, strict ATS keyword + format score>,
  "match_score": <integer 0-100, holistic match including experience depth, not just keywords>,
  "hire_probability": <integer 0-100, realistic chance of getting an interview callback>,
  "matched_skills": [<exact skills/keywords present in BOTH resume and JD>],
  "missing_skills": [<critical skills in JD completely absent from resume>],
  "strengths": [<3-5 genuine strengths with specific evidence from the resume>],
  "improvements": [<4-6 specific improvements with exact wording suggestions where possible>],
  "keyword_suggestions": [<6-8 exact ATS keywords to add, taken directly from the JD>],
  "experience_gap": "<honest assessment: does experience level/years match what JD requires?>",
  "education_match": "<does education match requirements? note if overqualified/underqualified>",
  "red_flags": [<1-3 specific things a recruiter would immediately notice negatively, be honest>],
  "overall_summary": "<2-3 sentences: honest realistic assessment, mention visa/OPT if F1 relevant, give actual interview chances>",
  "quick_wins": [<3 specific things to fix TODAY that will immediately improve callback rate>],
  "salary_insight": "<based on role/location/experience, estimated salary range this resume would command>"
}}

Be brutally honest like a real recruiter. Candidates need truth, not false hope. If the match is poor, say so clearly with specific reasons. If strong, explain exactly why."""

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
            raise ValueError(
                "Rate limit hit! Free tier = 20 requests/minute & 200/day. "
                "Fix: (1) Wait 1 minute and retry, "
                "(2) Switch to a different free model in sidebar, "
                "(3) Use '🎲 Auto Free Router' — picks whichever model has capacity now!"
            )
        elif response.status_code == 404:
            error_body = response.text
            if "data policy" in error_body.lower() or "privacy" in error_body.lower() or "publication" in error_body.lower():
                raise ValueError(
                    "⚙️ OpenRouter Privacy Setting Required!\n\n"
                    "Free models need a one-time account setting:\n"
                    "1. Go to: https://openrouter.ai/settings/privacy\n"
                    "2. Enable 'Allow free model usage' / Data Collection toggle\n"
                    "3. Save and come back here\n\n"
                    "This is a one-time fix — all free models will work after!"
                )
            else:
                raise ValueError(f"Model not found (404). Try a different model from the dropdown.\nDetails: {response.text[:200]}")
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
            "ats_score": 0, "match_score": 0, "hire_probability": 0,
            "matched_skills": [], "missing_skills": [], "strengths": [],
            "improvements": [], "keyword_suggestions": [], "experience_gap": "",
            "education_match": "", "overall_summary": "", "quick_wins": [],
            "red_flags": [], "salary_insight": ""
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