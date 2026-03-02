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
    # ── ⭐ Top Recommended ──
    "🎲 Auto Free Router — Let OpenRouter Pick Best":    "openrouter/free",
    "🦙 Llama 4 Maverick — Latest Meta (Best Free)":    "meta-llama/llama-4-maverick:free",
    "🦙 Llama 4 Scout — Meta Fast & Smart":             "meta-llama/llama-4-scout:free",
    "🧠 DeepSeek R1 — Best Reasoning":                  "deepseek/deepseek-r1:free",
    "💬 DeepSeek V3 — Great Quality":                   "deepseek/deepseek-chat-v3-0324:free",
    "🌟 Gemini 2.5 Pro Exp — Google Latest":            "google/gemini-2.5-pro-exp-03-25:free",
    "⚡ Mistral Small 3.1 24B — Fast":                  "mistralai/mistral-small-3.1-24b-instruct:free",
    "🦙 Llama 3.3 70B — Reliable & Proven":             "meta-llama/llama-3.3-70b-instruct:free",
    "🌟 Qwen 2.5 72B — Good Quality":                   "qwen/qwen-2.5-72b-instruct:free",
    "🟠 OpenAI GPT-OSS 120B — OpenAI Free Model":       "openai/gpt-oss-120b:free",
    "🔵 Qwen3 Coder — Best for Technical Roles":        "qwen/qwen3-coder:free",
    "🟡 NVIDIA Nemotron 30B — Powerful":                "nvidia/nemotron-3-nano-30b-a3b:free",
    "🌸 Gemma 3 27B — Google Balanced":                 "google/gemma-3-27b-it:free",
}

PAID_MODELS = {
    "👑 Claude 3.5 Sonnet — Best Overall":       "anthropic/claude-3.5-sonnet",
    "💎 GPT-4o — Top Tier OpenAI":               "openai/gpt-4o",
    "🚀 GPT-4o Mini — Fast & Affordable":        "openai/gpt-4o-mini",
    "🌙 Gemini 2.0 Flash — Google Stable":       "google/gemini-2.0-flash-001",
    "🧬 Claude 3.5 Haiku — Fastest Claude":      "anthropic/claude-3.5-haiku",
    "🔮 DeepSeek R1 — Best Paid Reasoning":      "deepseek/deepseek-r1",
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