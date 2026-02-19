"""
app.py - AI Resume Analyzer & Job Match Tool
Built with Streamlit + Google Gemini AI + SQLite

Author: Yagyesh Vyas
GitHub: https://github.com/yagyeshvyas
"""

import streamlit as st
import pandas as pd
from analyzer import (
    extract_text_from_pdf, analyze_resume,
    get_score_color, get_score_label,
    FREE_MODELS, PAID_MODELS, get_model_id
)
from database import (
    init_db, save_analysis, get_all_analyses,
    get_top_missing_skills, get_score_trend, delete_analysis
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main theme */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; font-weight: 800; }
    .main-header p  { font-size: 1.1rem; margin: 0.5rem 0 0; opacity: 0.9; }

    /* Score cards */
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 4px solid;
        margin-bottom: 1rem;
    }
    .score-number { font-size: 3rem; font-weight: 900; line-height: 1; }
    .score-label  { font-size: 0.85rem; color: #666; margin-top: 0.3rem; }
    .score-title  { font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }

    /* Skill chips */
    .chip-container { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0; }
    .chip-green {
        background: #e8f5e9; color: #2e7d32; padding: 4px 12px;
        border-radius: 20px; font-size: 0.82rem; font-weight: 500;
        border: 1px solid #a5d6a7;
    }
    .chip-red {
        background: #ffebee; color: #c62828; padding: 4px 12px;
        border-radius: 20px; font-size: 0.82rem; font-weight: 500;
        border: 1px solid #ef9a9a;
    }
    .chip-blue {
        background: #e3f2fd; color: #1565c0; padding: 4px 12px;
        border-radius: 20px; font-size: 0.82rem; font-weight: 500;
        border: 1px solid #90caf9;
    }

    /* Info boxes */
    .info-box {
        background: #f8f9ff;
        border-left: 4px solid #667eea;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.92rem;
    }
    .win-box {
        background: #fffde7;
        border-left: 4px solid #f9a825;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.92rem;
    }

    /* Section headers */
    .section-header {
        font-size: 1.15rem; font-weight: 700;
        color: #333; margin: 1.2rem 0 0.6rem;
        display: flex; align-items: center; gap: 8px;
    }

    /* Sidebar */
    .api-info {
        background: #e8f4fd;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 0.82rem;
        color: #1565c0;
        margin-top: 0.5rem;
    }
    
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INIT DATABASE
# ─────────────────────────────────────────────
init_db()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
    st.title("⚙️ Settings")
    st.markdown("---")

    # API Key input
    st.markdown("### 🔑 OpenRouter API Key")
    api_key = st.text_input(
        "Enter your API key",
        type="password",
        placeholder="sk-or-...",
        help="Get a free key at openrouter.ai/keys"
    )
    st.markdown("""
    <div class="api-info">
    🆓 <b>Free to start!</b><br>
    Get your key at:<br>
    <a href="https://openrouter.ai/keys" target="_blank">openrouter.ai/keys</a><br><br>
    ✅ No credit card for free models<br>
    💳 Add credits for paid models
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Model selector
    st.markdown("### 🤖 Choose AI Model")

    model_tier = st.radio(
        "Model tier",
        ["🆓 Free Models", "💎 Paid Models"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if model_tier == "🆓 Free Models":
        model_options = list(FREE_MODELS.keys())
        st.markdown("""
        <div class="api-info">
        ✅ These models are <b>completely free</b><br>
        No credits needed!
        </div>
        """, unsafe_allow_html=True)
    else:
        model_options = list(PAID_MODELS.keys())
        st.markdown("""
        <div class="api-info" style="background:#fff3e0; border-color:#e65100; color:#e65100">
        💳 These models cost a tiny amount<br>
        (~$0.001–$0.01 per analysis)<br>
        Add credits at openrouter.ai
        </div>
        """, unsafe_allow_html=True)

    selected_model_name = st.selectbox(
        "Select model",
        model_options,
        label_visibility="collapsed"
    )
    selected_model_id = get_model_id(selected_model_name)

    st.markdown("---")
    st.markdown("### 📌 Navigation")
    page = st.radio(
        "Go to",
        ["🎯 Analyze Resume", "📊 My Dashboard", "ℹ️ How It Works"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#999; text-align:center;">
    Built with ❤️ by Yagyesh Vyas<br>
    Python · OpenRouter AI · SQLite · Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: RENDER CHIPS
# ─────────────────────────────────────────────
def render_chips(items: list, chip_class: str) -> str:
    if not items:
        return "<i style='color:#999'>None found</i>"
    chips = "".join(f'<span class="{chip_class}">{item}</span>' for item in items)
    return f'<div class="chip-container">{chips}</div>'


def score_display(score: int, title: str, color: str):
    """Display score as a styled metric with progress bar."""
    st.markdown(f"""
    <div class="score-card" style="border-top-color:{color}">
        <div class="score-title">{title}</div>
        <div class="score-number" style="color:{color}">{score}</div>
        <div class="score-label">out of 100</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(score / 100)


# ═══════════════════════════════════════════════════════════
# PAGE 1: ANALYZE RESUME
# ═══════════════════════════════════════════════════════════
if page == "🎯 Analyze Resume":

    st.markdown("""
    <div class="main-header">
        <h1>🎯 AI Resume Analyzer</h1>
        <p>Upload your resume · Paste a job description · Get instant AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Section ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Your Resume")
        resume_input_type = st.radio(
            "Input method",
            ["Upload PDF", "Paste Text"],
            horizontal=True,
            label_visibility="collapsed"
        )

        resume_text = ""
        resume_filename = ""

        if resume_input_type == "Upload PDF":
            uploaded = st.file_uploader("Drop your PDF here", type=["pdf"])
            if uploaded:
                resume_filename = uploaded.name
                try:
                    resume_text = extract_text_from_pdf(uploaded)
                    st.success(f"✅ Parsed {len(resume_text.split())} words from '{uploaded.name}'")
                    with st.expander("👁️ Preview extracted text"):
                        st.text(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
                except ValueError as e:
                    st.error(str(e))
        else:
            resume_text = st.text_area(
                "Paste resume text here",
                height=250,
                placeholder="Copy and paste your resume content here..."
            )
            resume_filename = "pasted_resume.txt"

    with col2:
        st.markdown("### 💼 Job Description")
        job_title   = st.text_input("Job Title", placeholder="e.g. Data Engineer, AI Engineer")
        company_name = st.text_input("Company Name", placeholder="e.g. Google, Amazon, TCS")
        job_description = st.text_area(
            "Paste the full job description",
            height=200,
            placeholder="Paste the complete job posting here including requirements, responsibilities, and qualifications..."
        )

    st.markdown("---")

    # ── Analyze Button ──
    analyze_btn = st.button(
        "🚀 Analyze My Resume",
        type="primary",
        use_container_width=True,
        disabled=not api_key
    )

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to get started. It's free!")

    if analyze_btn:
        if not resume_text.strip():
            st.error("❌ Please provide your resume (upload PDF or paste text).")
        elif not job_description.strip():
            st.error("❌ Please paste a job description.")
        elif len(job_description.strip()) < 50:
            st.error("❌ Job description is too short. Please paste the full job posting.")
        else:
            with st.spinner("🤖 AI is analyzing your resume... This takes about 10-15 seconds..."):
                try:
                    result = analyze_resume(
                        api_key=api_key,
                        model_id=selected_model_id,
                        resume_text=resume_text,
                        job_description=job_description,
                        job_title=job_title,
                        company_name=company_name
                    )

                    # Save to database
                    result["resume_filename"] = resume_filename
                    result["job_title"] = job_title
                    result["company_name"] = company_name
                    result["word_count"] = len(resume_text.split())
                    save_analysis(result)

                    st.success("✅ Analysis complete! Scroll down to see your results.")
                    st.session_state["last_result"] = result

                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

    # ── Display Results ──
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        if result.get("job_title"):
            st.markdown(f"**Role:** {result['job_title']}" + 
                       (f" @ **{result['company_name']}**" if result.get('company_name') else ""))

        # ── Score Gauges ──
        g1, g2 = st.columns(2)
        with g1:
            ats_color = get_score_color(result["ats_score"])
            score_display(result["ats_score"], "🎯 ATS Score", ats_color)
            st.markdown(
                f"<div style='text-align:center; font-weight:600; color:{ats_color}'>"
                f"{get_score_label(result['ats_score'])}</div>",
                unsafe_allow_html=True
            )
        with g2:
            match_color = get_score_color(result["match_score"])
            score_display(result["match_score"], "💼 Job Match Score", match_color)
            st.markdown(
                f"<div style='text-align:center; font-weight:600; color:{match_color}'>"
                f"{get_score_label(result['match_score'])}</div>",
                unsafe_allow_html=True
            )

        # ── Overall Summary ──
        st.markdown(f"""
        <div class="info-box" style="background:#f0f4ff; border-color:#4c6ef5; margin-top:1rem">
        <b>🤖 AI Assessment:</b><br>{result['overall_summary']}
        </div>
        """, unsafe_allow_html=True)

        # ── Skills Analysis ──
        st.markdown("---")
        sc1, sc2 = st.columns(2)

        with sc1:
            st.markdown('<div class="section-header">✅ Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(render_chips(result["matched_skills"], "chip-green"), unsafe_allow_html=True)

        with sc2:
            st.markdown('<div class="section-header">❌ Missing Skills (Add These!)</div>', unsafe_allow_html=True)
            st.markdown(render_chips(result["missing_skills"], "chip-red"), unsafe_allow_html=True)

        # ── Keyword Suggestions ──
        st.markdown('<div class="section-header">🔑 Keywords to Add for Better ATS</div>', unsafe_allow_html=True)
        st.markdown(render_chips(result.get("keyword_suggestions", []), "chip-blue"), unsafe_allow_html=True)

        # ── Strengths & Improvements ──
        st.markdown("---")
        imp1, imp2 = st.columns(2)

        with imp1:
            st.markdown('<div class="section-header">💪 Your Strengths</div>', unsafe_allow_html=True)
            for i, strength in enumerate(result.get("strengths", []), 1):
                st.markdown(f'<div class="info-box">✅ {strength}</div>', unsafe_allow_html=True)

        with imp2:
            st.markdown('<div class="section-header">🔧 Improvements Needed</div>', unsafe_allow_html=True)
            for i, tip in enumerate(result.get("improvements", []), 1):
                st.markdown(f'<div class="info-box">💡 {tip}</div>', unsafe_allow_html=True)

        # ── Quick Wins ──
        if result.get("quick_wins"):
            st.markdown("---")
            st.markdown('<div class="section-header">⚡ Quick Wins (Fix in 10 Minutes!)</div>', unsafe_allow_html=True)
            for win in result["quick_wins"]:
                st.markdown(f'<div class="win-box">⚡ {win}</div>', unsafe_allow_html=True)

        # ── Additional Details ──
        with st.expander("📋 Experience & Education Analysis"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.markdown("**Experience Gap Analysis**")
                st.info(result.get("experience_gap", "N/A"))
            with col_e2:
                st.markdown("**Education Match**")
                st.info(result.get("education_match", "N/A"))

        # ── Download Report ──
        st.markdown("---")
        report_text = f"""
AI RESUME ANALYSIS REPORT
{'='*50}
Job Title:    {result.get('job_title', 'N/A')}
Company:      {result.get('company_name', 'N/A')}
ATS Score:    {result['ats_score']}/100
Match Score:  {result['match_score']}/100

OVERALL SUMMARY
{'-'*40}
{result['overall_summary']}

MATCHED SKILLS
{'-'*40}
{', '.join(result['matched_skills'])}

MISSING SKILLS
{'-'*40}
{', '.join(result['missing_skills'])}

KEYWORDS TO ADD
{'-'*40}
{', '.join(result.get('keyword_suggestions', []))}

STRENGTHS
{'-'*40}
{chr(10).join(f'• {s}' for s in result['strengths'])}

IMPROVEMENTS NEEDED
{'-'*40}
{chr(10).join(f'• {s}' for s in result['improvements'])}

QUICK WINS
{'-'*40}
{chr(10).join(f'• {s}' for s in result.get('quick_wins', []))}

EXPERIENCE GAP
{'-'*40}
{result.get('experience_gap', 'N/A')}

EDUCATION MATCH
{'-'*40}
{result.get('education_match', 'N/A')}
"""
        st.download_button(
            "⬇️ Download Full Report (.txt)",
            data=report_text,
            file_name=f"resume_analysis_{result.get('job_title','role').replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# ═══════════════════════════════════════════════════════════
# PAGE 2: DASHBOARD
# ═══════════════════════════════════════════════════════════
elif page == "📊 My Dashboard":

    st.markdown("""
    <div class="main-header">
        <h1>📊 My Progress Dashboard</h1>
        <p>Track your resume improvements and application history over time</p>
    </div>
    """, unsafe_allow_html=True)

    analyses = get_all_analyses()
    missing_skills_data = get_top_missing_skills()
    score_trend = get_score_trend()

    if not analyses:
        st.info("📭 No analyses yet. Go to 'Analyze Resume' to get started!")
    else:
        # ── Summary Stats ──
        avg_ats   = sum(a["ats_score"] for a in analyses) / len(analyses)
        avg_match = sum(a["match_score"] for a in analyses) / len(analyses)
        best_ats  = max(a["ats_score"] for a in analyses)

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Analyses", len(analyses))
        s2.metric("Avg ATS Score", f"{avg_ats:.0f}/100")
        s3.metric("Avg Match Score", f"{avg_match:.0f}/100")
        s4.metric("Best ATS Score", f"{best_ats}/100")

        st.markdown("---")

        # ── Score Trend Chart ──
        if len(score_trend) >= 2:
            st.markdown("### 📈 Score Improvement Over Time")
            df_trend = pd.DataFrame(score_trend)
            df_trend = df_trend.set_index("date")[["ats", "match"]]
            df_trend.columns = ["ATS Score", "Match Score"]
            st.line_chart(df_trend)

        # ── Top Missing Skills ──
        if missing_skills_data:
            st.markdown("### 🎯 Skills You Keep Missing (Focus on These!)")
            df_skills = pd.DataFrame(missing_skills_data).head(10)
            df_skills = df_skills.set_index("skill")
            df_skills.columns = ["Times Required"]
            st.bar_chart(df_skills)

        # ── History Table ──
        st.markdown("### 📋 Analysis History")
        for a in analyses:
            with st.expander(
                f"{'🟢' if a['ats_score'] >= 70 else '🟡' if a['ats_score'] >= 50 else '🔴'} "
                f"{a['job_title'] or 'Unknown Role'}"
                f"{' @ ' + a['company_name'] if a['company_name'] else ''} — "
                f"ATS: {a['ats_score']}/100 · Match: {a['match_score']}/100 · {a['created_at'][:10]}"
            ):
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.markdown("**Matched Skills:**")
                    st.markdown(render_chips(a["matched_skills"][:8], "chip-green"), unsafe_allow_html=True)
                with col_h2:
                    st.markdown("**Missing Skills:**")
                    st.markdown(render_chips(a["missing_skills"][:8], "chip-red"), unsafe_allow_html=True)

                st.markdown(f"**Summary:** {a['overall_summary']}")

                if st.button(f"🗑️ Delete", key=f"del_{a['id']}"):
                    delete_analysis(a["id"])
                    st.rerun()


# ═══════════════════════════════════════════════════════════
# PAGE 3: HOW IT WORKS
# ═══════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ How It Works</h1>
        <p>Everything you need to know about the AI Resume Analyzer</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🔍 What is an ATS Score?
    An **Applicant Tracking System (ATS)** is software used by 99% of Fortune 500 companies 
    to filter resumes before a human ever sees them. If your resume doesn't match the right 
    keywords, it gets rejected automatically — even if you're qualified.

    Our AI simulates how an ATS reads your resume and gives you a score from 0-100.

    ---

    ### 🤖 How the AI Analysis Works

    1. **You upload your resume** (PDF or text)
    2. **You paste the job description** from any job site
    3. **Google Gemini AI** reads both and compares them deeply:
       - Finds matching and missing keywords
       - Analyzes experience and education alignment  
       - Suggests specific improvements
       - Generates actionable quick wins
    4. **Results are saved** to your personal SQLite database
    5. **Dashboard tracks progress** over multiple applications

    ---

    ### 💡 Tips for Best Results

    - Paste the **complete** job description, not just the title
    - Use your **most recent, updated** resume
    - Analyze **each job separately** — tailor your resume for each role
    - Focus on the **Quick Wins** first, then tackle bigger improvements
    - Track your scores over time in the **Dashboard**

    ---

    ### 🛠️ Tech Stack
    | Component | Technology |
    |-----------|-----------|
    | AI Engine | OpenRouter API (100+ models) |
    | Free Models | Gemini 2.0, DeepSeek R1, Llama 3.3, Qwen 2.5 |
    | Paid Models | Claude 3.5, GPT-4o, and more |
    | Backend | Python 3.11 |
    | Database | SQLite (local, private) |
    | Web UI | Streamlit |
    | Charts | Plotly |
    | PDF Parser | pdfplumber |

    ---

    ### 🔒 Privacy
    - Your resume data is stored **only on your local machine**
    - Nothing is sent to any server except the Gemini AI API for analysis
    - Your API key is never stored — it stays in your browser session only
    
    ---
    
    ### 🆓 100% Free Forever
    - **Streamlit Cloud**: Free hosting at streamlit.io/cloud
    - **Google Gemini API**: Free tier = 15 requests/minute, 1M tokens/day
    - **SQLite**: Built into Python, no setup needed
    - **No credit card required**
    """)
