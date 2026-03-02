"""
app.py - AI Career Suite | Dark Luxury UI
Author: Yagyesh Vyas | github.com/yagyeshVyas
"""

import streamlit as st
import pandas as pd
import requests
from analyzer import (
    extract_text_from_pdf, analyze_resume,
    get_score_color, get_score_label,
    FREE_MODELS, PAID_MODELS, get_model_id
)
from database import (
    init_db, save_analysis, get_all_analyses,
    get_top_missing_skills, get_score_trend, delete_analysis
)

st.set_page_config(
    page_title="AI Career Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg:#07070f; --bg2:#0e0e1a; --bg3:#13131f;
    --border:rgba(139,92,246,0.18); --border2:rgba(139,92,246,0.35);
    --purple:#8b5cf6; --purple2:#a78bfa; --violet:#7c3aed;
    --green:#10b981; --amber:#f59e0b; --red:#ef4444;
    --text:#e2e8f0; --text2:#94a3b8; --text3:#64748b;
    --font-h:'Syne',sans-serif; --font-b:'DM Sans',sans-serif;
}
.stApp { background:var(--bg) !important; font-family:var(--font-b) !important; }
[data-testid="stSidebar"] { background:var(--bg2) !important; border-right:1px solid var(--border) !important; }
[data-testid="stAppViewContainer"] > .main .block-container { padding:2rem 3rem !important; max-width:1400px !important; }
h1,h2,h3 { font-family:var(--font-h) !important; color:var(--text) !important; }

.hero {
    position:relative; background:linear-gradient(135deg,#13131f 0%,#1a0a2e 50%,#0a1628 100%);
    border:1px solid var(--border2); border-radius:20px; padding:3rem;
    margin-bottom:2.5rem; overflow:hidden; text-align:center;
}
.hero::before {
    content:''; position:absolute; top:-60%; left:50%; transform:translateX(-50%);
    width:600px; height:400px;
    background:radial-gradient(ellipse,rgba(139,92,246,0.25) 0%,transparent 70%);
}
.hero-badge {
    display:inline-block; background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.4);
    color:var(--purple2); font-size:0.72rem; font-weight:600; letter-spacing:0.12em;
    text-transform:uppercase; padding:5px 14px; border-radius:100px; margin-bottom:1.2rem;
}
.hero h1 {
    font-family:var(--font-h) !important; font-size:2.8rem !important; font-weight:800 !important;
    background:linear-gradient(135deg,#e2e8f0 0%,#a78bfa 50%,#60a5fa 100%);
    -webkit-background-clip:text !important; -webkit-text-fill-color:transparent !important;
    background-clip:text !important; line-height:1.2 !important; margin-bottom:0.8rem !important;
}
.hero p { color:var(--text2) !important; font-size:1.05rem !important; font-weight:300 !important; max-width:600px; margin:0 auto !important; }

.score-wrap {
    background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:16px;
    padding:1.5rem; text-align:center; position:relative; overflow:hidden; margin-bottom:1rem;
}
.score-wrap::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0; }
.score-wrap.green::before { background:linear-gradient(90deg,#10b981,#34d399); }
.score-wrap.amber::before { background:linear-gradient(90deg,#f59e0b,#fbbf24); }
.score-wrap.red::before   { background:linear-gradient(90deg,#ef4444,#f87171); }
.score-number { font-family:var(--font-h); font-size:3.5rem; font-weight:800; line-height:1; margin:0.3rem 0; }
.score-number.green { color:#10b981; } .score-number.amber { color:#f59e0b; } .score-number.red { color:#ef4444; }
.score-label  { font-size:0.72rem; color:var(--text3); text-transform:uppercase; letter-spacing:0.1em; font-weight:600; }
.score-title  { font-size:0.82rem; color:var(--text2); font-weight:500; margin-bottom:0.5rem; }
.score-badge  { display:inline-block; padding:3px 10px; border-radius:100px; font-size:0.72rem; font-weight:600; margin-top:0.5rem; }
.score-badge.green { background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3); }
.score-badge.amber { background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3); }
.score-badge.red   { background:rgba(239,68,68,0.15);  color:#ef4444; border:1px solid rgba(239,68,68,0.3); }

.chips { display:flex; flex-wrap:wrap; gap:7px; margin:0.6rem 0; }
.chip  { padding:4px 12px; border-radius:100px; font-size:0.78rem; font-weight:500; border:1px solid; }
.chip-green  { background:rgba(16,185,129,0.1);  color:#34d399; border-color:rgba(16,185,129,0.25); }
.chip-red    { background:rgba(239,68,68,0.1);   color:#f87171; border-color:rgba(239,68,68,0.25); }
.chip-blue   { background:rgba(96,165,250,0.1);  color:#93c5fd; border-color:rgba(96,165,250,0.25); }
.chip-purple { background:rgba(139,92,246,0.1);  color:#a78bfa; border-color:rgba(139,92,246,0.25); }

.info-box    { background:rgba(139,92,246,0.06); border:1px solid rgba(139,92,246,0.2); border-left:3px solid var(--purple); border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; color:var(--text); line-height:1.6; }
.win-box     { background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.2); border-left:3px solid var(--amber); border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; color:var(--text); line-height:1.6; }
.danger-box  { background:rgba(239,68,68,0.06);  border:1px solid rgba(239,68,68,0.2);  border-left:3px solid var(--red);   border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; color:var(--text); line-height:1.6; }
.success-box { background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.2); border-left:3px solid var(--green); border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin:0.5rem 0; font-size:0.9rem; color:var(--text); line-height:1.6; }

.section-title {
    font-family:var(--font-h); font-size:0.78rem; font-weight:700; letter-spacing:0.14em;
    text-transform:uppercase; color:var(--purple2); margin:1.5rem 0 0.8rem;
    display:flex; align-items:center; gap:10px;
}
.section-title::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(139,92,246,0.4),transparent); }

.summary-box {
    background:linear-gradient(135deg,rgba(139,92,246,0.08) 0%,rgba(16,185,129,0.05) 100%);
    border:1px solid rgba(139,92,246,0.25); border-radius:14px;
    padding:1.4rem 1.6rem; font-size:0.95rem; color:var(--text); line-height:1.7; margin:1rem 0;
}
.resume-output {
    background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:14px;
    padding:2rem; font-family:'DM Sans',sans-serif; font-size:0.88rem;
    color:var(--text); line-height:1.8; white-space:pre-wrap;
}
.api-box { background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.2); border-radius:10px; padding:0.8rem; font-size:0.78rem; color:var(--purple2); margin-top:0.4rem; line-height:1.6; }
.api-box a { color:var(--purple2); text-decoration:none; font-weight:600; }
.free-badge { display:inline-block; background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3); font-size:0.65rem; padding:2px 8px; border-radius:100px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; }
.paid-badge { display:inline-block; background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3); font-size:0.65rem; padding:2px 8px; border-radius:100px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:0.4rem; }

.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
    background:rgba(255,255,255,0.04) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; color:var(--text) !important; font-family:var(--font-b) !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color:var(--purple) !important; box-shadow:0 0 0 3px rgba(139,92,246,0.1) !important;
}
.stButton>button {
    background:linear-gradient(135deg,#7c3aed,#6d28d9) !important; color:white !important;
    border:none !important; border-radius:10px !important; font-family:var(--font-h) !important;
    font-weight:700 !important; font-size:0.92rem !important; letter-spacing:0.03em !important;
    padding:0.65rem 2rem !important; transition:all 0.2s !important;
    box-shadow:0 4px 20px rgba(124,58,237,0.3) !important;
}
.stButton>button:hover { background:linear-gradient(135deg,#8b5cf6,#7c3aed) !important; box-shadow:0 4px 30px rgba(139,92,246,0.5) !important; transform:translateY(-1px) !important; }
.stButton>button[disabled] { background:rgba(255,255,255,0.06) !important; color:var(--text3) !important; box-shadow:none !important; transform:none !important; }
.stDownloadButton>button { background:rgba(16,185,129,0.12) !important; color:#10b981 !important; border:1px solid rgba(16,185,129,0.3) !important; border-radius:10px !important; font-weight:600 !important; box-shadow:none !important; }
.stDownloadButton>button:hover { background:rgba(16,185,129,0.2) !important; }
.stProgress>div>div>div>div { background:linear-gradient(90deg,#7c3aed,#a78bfa) !important; border-radius:100px !important; }
.stProgress>div>div>div { background:rgba(255,255,255,0.06) !important; border-radius:100px !important; }
.stRadio>div { gap:0.5rem !important; }
.stRadio>div>label { background:rgba(255,255,255,0.03) !important; border:1px solid var(--border) !important; border-radius:8px !important; padding:0.4rem 0.8rem !important; color:var(--text2) !important; transition:all 0.2s !important; }
.stRadio>div>label:has(input:checked) { background:rgba(139,92,246,0.12) !important; border-color:var(--purple) !important; color:var(--purple2) !important; }
.stSelectbox>label, .stTextInput>label, .stTextArea>label, .stRadio>label, .stFileUploader>label, .stSlider>label, .stCheckbox>label span { color:var(--text2) !important; font-size:0.85rem !important; }
[data-testid="stFileUploadDropzone"] { background:rgba(255,255,255,0.02) !important; border:1px dashed var(--border2) !important; border-radius:12px !important; }
div[data-testid="stExpander"] { background:rgba(255,255,255,0.02) !important; border:1px solid var(--border) !important; border-radius:12px !important; }
div[data-testid="stExpander"]:hover { border-color:var(--border2) !important; }
[data-testid="stMetric"] { background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:12px; padding:1rem; }
[data-testid="stMetricLabel"] { color:var(--text2) !important; font-size:0.8rem !important; }
[data-testid="stMetricValue"] { color:var(--text) !important; font-family:var(--font-h) !important; }
hr { border-color:var(--border) !important; }
#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

init_db()

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>🚀 AI Career Suite</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1.5rem'>Powered by OpenRouter</div>", unsafe_allow_html=True)

    st.markdown("**🔑 API Key**")
    api_key = st.text_input("", type="password", placeholder="sk-or-v1-...", label_visibility="collapsed")
    st.markdown("""<div class="api-box">🆓 Free — no credit card needed<br>Get key: <a href="https://openrouter.ai/keys" target="_blank">openrouter.ai/keys</a></div>""", unsafe_allow_html=True)
    st.markdown("---")

    tier = st.radio("**🤖 Model Tier**", ["🆓 Free", "💎 Paid"], horizontal=True)
    if tier == "🆓 Free":
        st.markdown('<span class="free-badge">✓ No credits needed</span>', unsafe_allow_html=True)
        opts = list(FREE_MODELS.keys())
    else:
        st.markdown('<span class="paid-badge">💳 Credits required</span>', unsafe_allow_html=True)
        opts = list(PAID_MODELS.keys())

    sel_name = st.selectbox("", opts, label_visibility="collapsed")
    sel_id   = get_model_id(sel_name)
    st.markdown("---")

    page = st.radio("**📌 Navigate**", [
        "🎯 Analyzer", "✉️ Cover Letter",
        "🎤 Interview Prep", "📝 Resume Builder",
        "📊 Dashboard", "ℹ️ About"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#475569;text-align:center;line-height:1.8'>Built by <b style='color:#7c3aed'>Yagyesh Vyas</b><br>Python · OpenRouter · SQLite · Streamlit</div>", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────
def chips(items, cls="chip-green"):
    if not items: return "<span style='color:#475569;font-style:italic;font-size:0.82rem'>None found</span>"
    return '<div class="chips">'+"".join(f'<span class="chip {cls}">{i}</span>' for i in items)+'</div>'

def score_card(score, title):
    cls = "green" if score >= 75 else ("amber" if score >= 50 else "red")
    st.markdown(f"""<div class="score-wrap {cls}">
        <div class="score-title">{title}</div>
        <div class="score-number {cls}">{score}</div>
        <div class="score-label">out of 100</div>
        <span class="score-badge {cls}">{get_score_label(score)}</span>
    </div>""", unsafe_allow_html=True)
    st.progress(score / 100)

def ai_call(prompt, temperature=0.7, max_tokens=2500):
    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
                 "HTTP-Referer": "https://ai-career-suite.streamlit.app", "X-Title": "AI Career Suite"},
        json={"model": sel_id, "messages": [{"role": "user", "content": prompt}],
              "max_tokens": max_tokens, "temperature": temperature}, timeout=90)
    if r.status_code == 401: raise ValueError("Invalid API key — get a free one at openrouter.ai/keys")
    if r.status_code == 402: raise ValueError("No credits — use a free model or add credits at openrouter.ai")
    if r.status_code == 429: raise ValueError("Rate limit hit! (Free: 20/min, 200/day)\n→ Switch to '🎲 Auto Free Router' in sidebar — picks any available model automatically!")
    if r.status_code != 200: raise ValueError(f"API error {r.status_code}: {r.text[:150]}")
    return r.json()["choices"][0]["message"]["content"].strip()


# ════════════════════════════════════════════════════════
# 🎯 RESUME ANALYZER
# ════════════════════════════════════════════════════════
if page == "🎯 Analyzer":
    st.markdown("""<div class="hero"><div class="hero-badge">ATS · Match Score · Interview Probability</div>
    <h1>AI Resume Analyzer</h1>
    <p>Upload your resume, paste any job description — get a senior recruiter's verdict in 15 seconds</p></div>""", unsafe_allow_html=True)

    if not api_key: st.warning("⚠️ Enter your free OpenRouter API key in the sidebar → openrouter.ai/keys")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">📄 Your Resume</div>', unsafe_allow_html=True)
        rtype = st.radio("", ["📎 Upload PDF", "📋 Paste Text"], horizontal=True, label_visibility="collapsed", key="an_rt")
        resume_text = ""; resume_file = ""
        if rtype == "📎 Upload PDF":
            up = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="an_pdf")
            if up:
                try:
                    resume_text = extract_text_from_pdf(up); resume_file = up.name
                    st.success(f"✅ Extracted {len(resume_text.split())} words from **{up.name}**")
                    with st.expander("👁 Preview"): st.text(resume_text[:600]+"..." if len(resume_text)>600 else resume_text)
                except ValueError as e: st.error(str(e))
        else:
            resume_text = st.text_area("", height=220, placeholder="Paste your full resume text here...", label_visibility="collapsed", key="an_paste")
            resume_file = "pasted.txt"
    with c2:
        st.markdown('<div class="section-title">💼 Job Details</div>', unsafe_allow_html=True)
        jt = st.text_input("Job Title", placeholder="e.g. Data Engineer, AI Engineer")
        co = st.text_input("Company",   placeholder="e.g. Google, Amazon, TCS")
        jd = st.text_area("Job Description", height=180, placeholder="Paste the full job posting here — requirements, responsibilities, qualifications...")

    st.markdown("")
    if st.button("🚀 Analyze My Resume", type="primary", use_container_width=True, disabled=not api_key):
        if not resume_text.strip(): st.error("❌ Please provide your resume.")
        elif not jd.strip():        st.error("❌ Please paste the job description.")
        elif len(jd) < 50:          st.error("❌ Job description too short — paste the full posting.")
        else:
            with st.spinner("🤖 Analyzing with senior recruiter-level AI..."):
                try:
                    result = analyze_resume(api_key, sel_id, resume_text, jd, jt, co)
                    result.update({"resume_filename": resume_file, "job_title": jt, "company_name": co, "word_count": len(resume_text.split())})
                    save_analysis(result)
                    st.session_state["last_result"] = result
                    st.success("✅ Analysis complete!")
                except ValueError as e: st.error(f"❌ {e}")

    if "last_result" in st.session_state:
        r = st.session_state["last_result"]
        st.markdown("---")
        if r.get("job_title"): st.markdown(f"<h3 style='color:#e2e8f0;font-family:Syne'>Results — {r['job_title']}{' @ '+r['company_name'] if r.get('company_name') else ''}</h3>", unsafe_allow_html=True)
        s1,s2,s3 = st.columns(3)
        with s1: score_card(r["ats_score"],  "🎯 ATS Score")
        with s2: score_card(r["match_score"],"💼 Job Match")
        with s3: score_card(r.get("hire_probability",0),"📞 Interview Chance")
        st.markdown(f'<div class="summary-box">🤖 <strong>AI Verdict:</strong> {r["overall_summary"]}</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2, gap="large")
        with col1:
            st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(chips(r["matched_skills"],"chip-green"), unsafe_allow_html=True)
            st.markdown('<div class="section-title">💪 Strengths</div>', unsafe_allow_html=True)
            for s in r.get("strengths",[]): st.markdown(f'<div class="info-box">✅ {s}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            st.markdown(chips(r["missing_skills"],"chip-red"), unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔧 Improvements</div>', unsafe_allow_html=True)
            for tip in r.get("improvements",[]): st.markdown(f'<div class="info-box">💡 {tip}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔑 ATS Keywords to Add</div>', unsafe_allow_html=True)
        st.markdown(chips(r.get("keyword_suggestions",[]),"chip-blue"), unsafe_allow_html=True)
        if r.get("quick_wins"):
            st.markdown('<div class="section-title">⚡ Quick Wins — Fix in 10 Minutes</div>', unsafe_allow_html=True)
            for w in r["quick_wins"]: st.markdown(f'<div class="win-box">⚡ {w}</div>', unsafe_allow_html=True)
        if r.get("red_flags"):
            st.markdown('<div class="section-title">🚨 Recruiter Red Flags</div>', unsafe_allow_html=True)
            for f in r["red_flags"]: st.markdown(f'<div class="danger-box">🚨 {f}</div>', unsafe_allow_html=True)
        if r.get("salary_insight"): st.markdown(f'<div class="success-box">💰 <strong>Salary Insight:</strong> {r["salary_insight"]}</div>', unsafe_allow_html=True)
        with st.expander("📋 Experience & Education Details"):
            e1,e2 = st.columns(2)
            with e1: st.markdown("**Experience Gap**"); st.info(r.get("experience_gap","N/A"))
            with e2: st.markdown("**Education Match**"); st.info(r.get("education_match","N/A"))
        st.markdown("---")
        report = f"""AI RESUME ANALYSIS REPORT\n{'='*50}
Job: {r.get('job_title','N/A')} @ {r.get('company_name','N/A')}
ATS: {r['ats_score']}/100 | Match: {r['match_score']}/100 | Interview: {r.get('hire_probability',0)}/100
\nSUMMARY\n{r['overall_summary']}
\nMATCHED: {', '.join(r['matched_skills'])}
MISSING:  {', '.join(r['missing_skills'])}
KEYWORDS: {', '.join(r.get('keyword_suggestions',[]))}
\nSTRENGTHS\n{chr(10).join('• '+s for s in r['strengths'])}
\nIMPROVEMENTS\n{chr(10).join('• '+s for s in r['improvements'])}
\nQUICK WINS\n{chr(10).join('• '+s for s in r.get('quick_wins',[]))}
\nRED FLAGS\n{chr(10).join('• '+s for s in r.get('red_flags',[]))}
\nSALARY: {r.get('salary_insight','N/A')}
EXPERIENCE: {r.get('experience_gap','N/A')}
EDUCATION: {r.get('education_match','N/A')}"""
        st.download_button("⬇️ Download Full Report", data=report, file_name=f"analysis_{(r.get('job_title','role')).replace(' ','_')}.txt", mime="text/plain", use_container_width=True)


# ════════════════════════════════════════════════════════
# ✉️ COVER LETTER
# ════════════════════════════════════════════════════════
elif page == "✉️ Cover Letter":
    st.markdown("""<div class="hero"><div class="hero-badge">AI-Written · ATS-Friendly · Personalized</div>
    <h1>Cover Letter Generator</h1>
    <p>Paste resume + job description → Get a compelling, custom cover letter in seconds</p></div>""", unsafe_allow_html=True)
    if not api_key: st.warning("⚠️ Enter your free OpenRouter API key in the sidebar → openrouter.ai/keys")
    c1,c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">📄 Your Resume</div>', unsafe_allow_html=True)
        ct = st.radio("", ["📎 Upload PDF","📋 Paste Text"], horizontal=True, label_visibility="collapsed", key="cl_rt")
        cl_r = ""
        if ct == "📎 Upload PDF":
            up = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="cl_pdf")
            if up:
                try: cl_r = extract_text_from_pdf(up); st.success(f"✅ {len(cl_r.split())} words extracted")
                except ValueError as e: st.error(str(e))
        else: cl_r = st.text_area("", height=200, placeholder="Paste resume...", label_visibility="collapsed", key="cl_paste")
    with c2:
        st.markdown('<div class="section-title">💼 Job Details</div>', unsafe_allow_html=True)
        cl_jt = st.text_input("Job Title",   placeholder="e.g. Data Engineer", key="cl_jt")
        cl_co = st.text_input("Company",     placeholder="e.g. Google", key="cl_co")
        cl_hm = st.text_input("Hiring Manager (optional)", placeholder="e.g. Sarah Johnson", key="cl_hm")
        cl_jd = st.text_area("Job Description", height=140, key="cl_jd", placeholder="Paste job posting here...")
    st.markdown('<div class="section-title">🎨 Tone</div>', unsafe_allow_html=True)
    tone = st.select_slider("", ["Very Formal","Professional","Friendly & Professional","Enthusiastic"], value="Professional", label_visibility="collapsed")
    if st.button("✉️ Generate Cover Letter", type="primary", use_container_width=True, disabled=not api_key):
        if not cl_r.strip(): st.error("❌ Please provide your resume.")
        elif not cl_jd.strip(): st.error("❌ Please paste the job description.")
        else:
            with st.spinner("✉️ Writing your personalized cover letter..."):
                try:
                    letter = ai_call(f"""You are an elite career coach writing cover letters that get callbacks at top MNCs. Tone: {tone}.
RESUME: {cl_r}
JOB: {cl_jt or 'the position'} at {cl_co or 'the company'}
HIRING MANAGER: {cl_hm or 'Hiring Manager'}
JD: {cl_jd}
Rules: powerful hook (NOT "I am writing to apply"), 3-4 paragraphs max 380 words, 2-3 specific quantified achievements from resume, 5 ATS keywords naturally, confident call to action. Sound human not generic AI.
Write ONLY the letter starting from "Dear {cl_hm or 'Hiring Manager'}," """, temperature=0.75)
                    st.markdown('<div class="section-title">✅ Your Cover Letter</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="resume-output">{letter}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Download Cover Letter", data=letter, file_name=f"cover_letter_{(cl_co or 'company').replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
                    st.info("💡 Copy into Google Docs and add your name/address header before sending.")
                except Exception as e: st.error(f"❌ {e}")


# ════════════════════════════════════════════════════════
# 🎤 INTERVIEW PREP
# ════════════════════════════════════════════════════════
elif page == "🎤 Interview Prep":
    st.markdown("""<div class="hero"><div class="hero-badge">Role-Specific · Resume-Based · STAR Format</div>
    <h1>Interview Prep Guide</h1>
    <p>Get tailored interview questions with ideal answers — based on YOUR resume and the exact role</p></div>""", unsafe_allow_html=True)
    if not api_key: st.warning("⚠️ Enter your free OpenRouter API key in the sidebar → openrouter.ai/keys")
    c1,c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">📄 Your Resume</div>', unsafe_allow_html=True)
        ipt = st.radio("", ["📎 Upload PDF","📋 Paste Text"], horizontal=True, label_visibility="collapsed", key="ip_rt")
        ip_r = ""
        if ipt == "📎 Upload PDF":
            up = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="ip_pdf")
            if up:
                try: ip_r = extract_text_from_pdf(up); st.success(f"✅ {len(ip_r.split())} words extracted")
                except ValueError as e: st.error(str(e))
        else: ip_r = st.text_area("", height=200, placeholder="Paste resume...", label_visibility="collapsed", key="ip_paste")
    with c2:
        st.markdown('<div class="section-title">💼 Job Details</div>', unsafe_allow_html=True)
        ip_jt = st.text_input("Job Title", placeholder="e.g. Data Engineer", key="ip_jt")
        ip_co = st.text_input("Company",   placeholder="e.g. TCS, Google",   key="ip_co")
        ip_jd = st.text_area("Job Description", height=140, key="ip_jd", placeholder="Paste job posting here...")
    st.markdown('<div class="section-title">⚙️ Question Categories</div>', unsafe_allow_html=True)
    q1,q2,q3,q4 = st.columns(4)
    with q1: qt = st.checkbox("🔧 Technical",  value=True)
    with q2: qb = st.checkbox("🧠 Behavioral", value=True)
    with q3: qs = st.checkbox("💡 Situational",value=True)
    with q4: qf = st.checkbox("🏢 Company Fit",value=True)
    nq = st.slider("Questions per category", 2, 5, 3)
    if st.button("🎤 Generate Interview Questions", type="primary", use_container_width=True, disabled=not api_key):
        if not ip_r.strip(): st.error("❌ Please provide your resume.")
        elif not ip_jd.strip(): st.error("❌ Please paste the job description.")
        else:
            types = [t for t, c in [("Technical (role-specific skills, tools, concepts)",qt), ("Behavioral (STAR format, past experiences)",qb), ("Situational (hypothetical scenarios)",qs), ("Company Fit (culture, motivation, goals)",qf)] if c]
            with st.spinner("🎤 Generating your personalized interview guide..."):
                try:
                    guide = ai_call(f"""You are a senior interviewer at a top MNC with 15 years hiring for {ip_jt or 'tech'} roles.
RESUME: {ip_r}
ROLE: {ip_jt or 'the role'} at {ip_co or 'top MNC'}
JD: {ip_jd}
Generate {nq} questions for EACH: {', '.join(types)}
For EVERY question: ❓ Question (specific to their resume), 🎯 Why asked (1 sentence), ✅ Ideal answer (3-4 bullets using their actual experience), ❌ Common mistake to avoid.
Reference actual projects/skills from THEIR resume. Format with clear headers.""", temperature=0.6)
                    st.markdown('<div class="section-title">✅ Your Interview Prep Guide</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="resume-output">{guide}</div>', unsafe_allow_html=True)
                    st.download_button("⬇️ Download Interview Guide", data=guide, file_name=f"interview_{(ip_jt or 'prep').replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
                    st.info("💡 Practice each answer out loud 3 times. Record yourself — it works!")
                except Exception as e: st.error(f"❌ {e}")


# ════════════════════════════════════════════════════════
# 📝 RESUME BUILDER
# ════════════════════════════════════════════════════════
elif page == "📝 Resume Builder":
    st.markdown("""<div class="hero"><div class="hero-badge">Build Fresh · Rewrite for New Job · 100% ATS Optimized</div>
    <h1>AI Resume Builder</h1>
    <p>Build a perfect resume from scratch — or paste your existing one and let AI rewrite it for any specific job</p></div>""", unsafe_allow_html=True)
    if not api_key: st.warning("⚠️ Enter your free OpenRouter API key in the sidebar → openrouter.ai/keys")

    mode = st.radio("", ["✨ Build Fresh Resume", "🔄 Rewrite Existing Resume for New Job"], horizontal=True, label_visibility="collapsed", key="rb_mode")
    st.markdown("---")

    # ── MODE: REWRITE ──
    if mode == "🔄 Rewrite Existing Resume for New Job":
        st.markdown("""<div class="info-box">🔄 <strong>How this works:</strong> Paste your current resume → paste the target job description
        → AI completely rewrites your resume to be 100% ATS-optimized for that specific job.
        Your facts stay accurate, but language, keywords, and structure are rebuilt for maximum impact.</div>""", unsafe_allow_html=True)

        rw1, rw2 = st.columns(2, gap="large")
        with rw1:
            st.markdown('<div class="section-title">📄 Your Current Resume</div>', unsafe_allow_html=True)
            rwt = st.radio("", ["📎 Upload PDF","📋 Paste Text"], horizontal=True, label_visibility="collapsed", key="rw_rt")
            rw_cur = ""
            if rwt == "📎 Upload PDF":
                up = st.file_uploader("", type=["pdf"], label_visibility="collapsed", key="rw_pdf")
                if up:
                    try:
                        rw_cur = extract_text_from_pdf(up)
                        st.success(f"✅ Extracted {len(rw_cur.split())} words from **{up.name}**")
                        with st.expander("👁 Preview extracted text"): st.text(rw_cur[:600]+"..." if len(rw_cur)>600 else rw_cur)
                    except ValueError as e: st.error(str(e))
            else: rw_cur = st.text_area("", height=300, placeholder="Paste your complete current resume here...", label_visibility="collapsed", key="rw_paste")
        with rw2:
            st.markdown('<div class="section-title">🎯 Target Job</div>', unsafe_allow_html=True)
            rw_jt = st.text_input("Job Title *",            placeholder="e.g. Data Engineer, AI Engineer", key="rw_jt")
            rw_co = st.text_input("Company (optional)",     placeholder="e.g. Google, Amazon, TCS",         key="rw_co")
            rw_jd = st.text_area("Job Description *", height=220, placeholder="Paste the full job posting here — the more detail, the better the rewrite...", key="rw_jd")

        st.markdown('<div class="section-title">⚙️ Rewrite Options</div>', unsafe_allow_html=True)
        op1,op2,op3 = st.columns(3)
        with op1: rw_ats  = st.checkbox("🔥 Aggressive ATS keywords", value=True, help="Heavily injects job keywords throughout")
        with op2: rw_num  = st.checkbox("📊 Add estimated metrics",   value=True, help="AI adds realistic numbers/% where missing")
        with op3: rw_lang = st.checkbox("✨ Modernize language",       value=True, help="Replace weak verbs with power action words")

        if st.button("🔄 Rewrite My Resume", type="primary", use_container_width=True, disabled=not api_key):
            if not rw_cur.strip():   st.error("❌ Please provide your current resume.")
            elif not rw_jd.strip():  st.error("❌ Please paste the target job description.")
            elif len(rw_jd) < 50:   st.error("❌ Job description too short — paste the full posting.")
            else:
                ats_rule  = "Inject EXACT keywords from JD throughout every section. Mirror job description language precisely. Front-load each bullet with the most important keyword." if rw_ats else "Naturally weave in relevant keywords."
                num_rule  = "Add realistic quantified achievements where missing (e.g. 'reduced processing time by 40%', 'managed 3+ projects simultaneously'). Every bullet needs at least one number or % or scale." if rw_num else "Keep existing metrics."
                lang_rule = "Replace ALL weak verbs (helped, worked, assisted) with power verbs (Engineered, Architected, Spearheaded, Automated, Optimized). Remove all filler phrases like 'responsible for'." if rw_lang else "Improve language where clearly weak."
                prompt = f"""You are the world's best resume writer specializing in ATS optimization for top MNC companies.
TASK: Completely rewrite this resume to achieve 95%+ ATS score for this specific job.

CURRENT RESUME:
{rw_cur}

TARGET JOB: {rw_jt or 'the role'} at {rw_co or 'the company'}
JOB DESCRIPTION:
{rw_jd}

REWRITE RULES:
- {ats_rule}
- {num_rule}
- {lang_rule}
- Keep ALL facts 100% accurate (companies, dates, education, certifications — never fabricate)
- Structure: Contact → Professional Summary → Key Achievements → Experience → Skills → Projects → Education → Certifications
- Professional Summary: 3 powerful sentences — target job title + top 3 matching skills + unique value
- Skills: organized by category, job-critical skills listed FIRST
- Each bullet: [Power Verb] + [What you did] + [Tool/Tech] + [Measurable result]
- Add a "Key Achievements" callout with 3 most impressive accomplishments
- Keep to 1-2 pages of content (700-900 words)

Output the COMPLETE rewritten resume, ready to copy-paste. Start with the person's name as header."""
                with st.spinner(f"🔄 Rewriting your resume for **{rw_jt or 'the role'}**... (~20 seconds)"):
                    try:
                        rewritten = ai_call(prompt, temperature=0.35, max_tokens=3000)
                        st.markdown("---")
                        st.markdown("""<div class="success-box">✅ <strong>Resume rewritten!</strong>
                        Your resume is now ATS-optimized for this specific job.
                        Go to <strong>🎯 Analyzer</strong> tab to verify your ATS score — aim for 80%+!</div>""", unsafe_allow_html=True)
                        st.markdown('<div class="section-title">📄 Your Rewritten Resume</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{rewritten}</div>', unsafe_allow_html=True)
                        d1,d2 = st.columns(2)
                        with d1: st.download_button("⬇️ Download Rewritten Resume", data=rewritten, file_name=f"resume_{(rw_jt or 'rewritten').replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
                        with d2: st.download_button("⬇️ Download Both Versions", data=f"ORIGINAL:\n{'='*50}\n{rw_cur}\n\nREWRITTEN:\n{'='*50}\n{rewritten}", file_name="resume_comparison.txt", mime="text/plain", use_container_width=True)
                        st.markdown("""<div class="win-box">⚡ <strong>Next Steps:</strong><br>
                        1. Copy the resume above → paste into Google Docs → format cleanly<br>
                        2. Go to <strong>🎯 Analyzer</strong> → paste this resume + job description → check ATS score<br>
                        3. Aim for 80%+ before applying. Rewrite again if needed!</div>""", unsafe_allow_html=True)
                    except Exception as e: st.error(f"❌ {e}")

    # ── MODE: BUILD FRESH ──
    else:
        st.markdown("""<div class="info-box">✨ <strong>How this works:</strong> Fill in your details → AI builds a complete,
        professional, ATS-optimized resume tailored to your target job. Takes about 20 seconds.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="section-title">👤 Personal Info</div>', unsafe_allow_html=True)
        p1,p2 = st.columns(2, gap="large")
        with p1:
            rb_name = st.text_input("Full Name *",   placeholder="Yagyesh Vyas",    key="rb_name")
            rb_mail = st.text_input("Email *",       placeholder="you@gmail.com",   key="rb_mail")
            rb_ph   = st.text_input("Phone",         placeholder="+1 (123) 456-7890",key="rb_ph")
            rb_loc  = st.text_input("Location",      placeholder="Richmond, VA, USA",key="rb_loc")
        with p2:
            rb_tgt  = st.text_input("Target Job Title *", placeholder="e.g. Data Engineer, AI Engineer", key="rb_tgt")
            rb_li   = st.text_input("LinkedIn URL",       placeholder="linkedin.com/in/yourname",        key="rb_li")
            rb_gh   = st.text_input("GitHub URL",         placeholder="github.com/yourname",             key="rb_gh")
            rb_port = st.text_input("Portfolio URL",      placeholder="yoursite.com",                    key="rb_port")
        st.markdown('<div class="section-title">🎓 Education</div>', unsafe_allow_html=True)
        rb_edu = st.text_area("", height=85, label_visibility="collapsed", key="rb_edu",
            placeholder="Master's in CS, University of the Potomac, 2024–2026, GPA 3.88\nBachelor's in CS, GTU, 2019–2022, GPA 8.08")
        st.markdown('<div class="section-title">💼 Work Experience</div>', unsafe_allow_html=True)
        rb_exp = st.text_area("", height=120, label_visibility="collapsed", key="rb_exp",
            placeholder="Data & IT Developer Intern, MKL Management LLC, Feb 2025–Oct 2025\n- Built Python automation scripts\n- Designed Power BI dashboards\n- Managed SQL databases")
        st.markdown('<div class="section-title">🛠 Skills & Projects</div>', unsafe_allow_html=True)
        sk1,sk2 = st.columns(2, gap="large")
        with sk1: rb_sk = st.text_area("Technical Skills (comma-separated)", height=85, key="rb_sk", placeholder="Python, SQL, Power BI, Docker, AWS, Streamlit, REST APIs, Git...")
        with sk2: rb_pr = st.text_area("Projects", height=85, key="rb_pr", placeholder="AI Resume Analyzer — Python, OpenRouter API, Streamlit. Live at streamlit.app")
        st.markdown('<div class="section-title">🏆 Certifications & Target JD</div>', unsafe_allow_html=True)
        ce1,ce2 = st.columns(2, gap="large")
        with ce1: rb_cert = st.text_area("Certifications", height=75, key="rb_cert", placeholder="AWS ML Fundamentals, Jan 2026\nKubernetes Cloud Native, Jan 2026")
        with ce2: rb_jd   = st.text_area("Target Job Description (recommended)", height=75, key="rb_jd2", placeholder="Paste the job you're targeting for a tailored resume...")

        if st.button("📝 Build My Resume", type="primary", use_container_width=True, disabled=not api_key):
            if not rb_name.strip() or not rb_mail.strip() or not rb_tgt.strip(): st.error("❌ Please fill in Name, Email, and Target Job Title.")
            else:
                with st.spinner("📝 Building your ATS-optimized resume..."):
                    try:
                        output = ai_call(f"""You are the world's best resume writer. Build a complete ATS-optimized resume.
Name:{rb_name} | Email:{rb_mail} | Phone:{rb_ph} | Location:{rb_loc}
LinkedIn:{rb_li} | GitHub:{rb_gh} | Portfolio:{rb_port} | Target:{rb_tgt}
EDUCATION: {rb_edu}
EXPERIENCE: {rb_exp}
SKILLS: {rb_sk}
PROJECTS: {rb_pr}
CERTIFICATIONS: {rb_cert}
TARGET JD: {rb_jd or f'General {rb_tgt} role'}

Rules: Professional Summary (3 sentences, target title+top skills+value), power verbs+quantified results, skills by category, ATS keywords from JD throughout, clear section headers with === markers, 600-800 words. Output COMPLETE copy-paste-ready resume.""", temperature=0.35, max_tokens=3000)
                        st.markdown("---")
                        st.markdown('<div class="success-box">✅ <strong>Resume built!</strong> Now go to <strong>🎯 Analyzer</strong> tab to check your ATS score!</div>', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">📄 Your AI-Built Resume</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{output}</div>', unsafe_allow_html=True)
                        st.download_button("⬇️ Download Resume", data=output, file_name=f"resume_{rb_name.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
                        st.info("💡 Copy into Google Docs → format cleanly → go to 🎯 Analyzer to verify ATS score!")
                    except Exception as e: st.error(f"❌ {e}")


# ════════════════════════════════════════════════════════
# 📊 DASHBOARD
# ════════════════════════════════════════════════════════
elif page == "📊 Dashboard":
    st.markdown("""<div class="hero"><div class="hero-badge">Progress · Trends · Insights</div>
    <h1>My Progress Dashboard</h1>
    <p>Track your resume improvements and application history over time</p></div>""", unsafe_allow_html=True)
    analyses = get_all_analyses(); ms = get_top_missing_skills(); st_data = get_score_trend()
    if not analyses: st.info("📭 No analyses yet. Go to **🎯 Analyzer** to get started!")
    else:
        avg_ats = sum(a["ats_score"] for a in analyses)/len(analyses)
        avg_m   = sum(a["match_score"] for a in analyses)/len(analyses)
        best    = max(a["ats_score"] for a in analyses)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("📋 Total Analyses", len(analyses))
        m2.metric("🎯 Avg ATS",  f"{avg_ats:.0f}/100")
        m3.metric("💼 Avg Match",f"{avg_m:.0f}/100")
        m4.metric("🏆 Best ATS", f"{best}/100")
        if len(st_data) >= 2:
            st.markdown('<div class="section-title">📈 Score Improvement Over Time</div>', unsafe_allow_html=True)
            df = pd.DataFrame(st_data).set_index("date")[["ats","match"]]
            df.columns = ["ATS Score","Match Score"]; st.line_chart(df)
        if ms:
            st.markdown('<div class="section-title">🎯 Skills You Keep Missing — Learn These First</div>', unsafe_allow_html=True)
            df2 = pd.DataFrame(ms).head(10).set_index("skill"); df2.columns = ["Times Required"]; st.bar_chart(df2)
        st.markdown('<div class="section-title">📋 Analysis History</div>', unsafe_allow_html=True)
        for a in analyses:
            icon = "🟢" if a["ats_score"]>=70 else ("🟡" if a["ats_score"]>=50 else "🔴")
            with st.expander(f"{icon} {a['job_title'] or 'Unknown'}{' @ '+a['company_name'] if a['company_name'] else ''} — ATS {a['ats_score']} · Match {a['match_score']} · {a['created_at'][:10]}"):
                h1,h2 = st.columns(2)
                with h1: st.markdown("**Matched:**"); st.markdown(chips(a["matched_skills"][:8],"chip-green"), unsafe_allow_html=True)
                with h2: st.markdown("**Missing:**");  st.markdown(chips(a["missing_skills"][:8],"chip-red"),   unsafe_allow_html=True)
                st.markdown(f"**Summary:** {a['overall_summary']}")
                if st.button("🗑️ Delete", key=f"del_{a['id']}"): delete_analysis(a["id"]); st.rerun()


# ════════════════════════════════════════════════════════
# ℹ️ ABOUT
# ════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    st.markdown("""<div class="hero"><div class="hero-badge">Free · Open Source · For Every Job Seeker</div>
    <h1>About AI Career Suite</h1>
    <p>Built by a job seeker, for job seekers — because ATS systems reject 75% of resumes before a human ever sees them</p></div>""", unsafe_allow_html=True)
    st.markdown("""
### 🛠️ Tools
| Tool | What it does |
|------|-------------|
| 🎯 **Resume Analyzer** | ATS score, job match, interview probability, red flags, salary insight |
| ✉️ **Cover Letter** | Custom ATS-friendly cover letter in 15 seconds |
| 🎤 **Interview Prep** | Role-specific Q&A based on YOUR resume |
| 📝 **Resume Builder** | Build from scratch OR rewrite existing resume for any job |
| 📊 **Dashboard** | Track progress and skill gaps across all applications |

---

### 🤖 AI Models (30+ total)
**Free:** Auto Router · Llama 3.3 · DeepSeek R1 · Gemma 3 27B · Qwen3 Coder · OpenAI GPT-OSS 120B · Mistral · NVIDIA Nemotron · and 20+ more

**Paid:** Claude Sonnet/Opus · GPT-4o · Gemini 2.5 Pro · Grok 4 · DeepSeek R1

Get free key: [openrouter.ai/keys](https://openrouter.ai/keys)

---

### 🛠️ Tech Stack
Python 3.11 · OpenRouter API · SQLite · Streamlit · pdfplumber · Streamlit Cloud

---

### 🔒 Privacy
Resume never stored on any server · Data only on your local machine · API key only in browser session

---

### 👨‍💻 Author
**Yagyesh Vyas** — Data & IT Developer | CS Graduate Student | F1 Visa

[LinkedIn](https://www.linkedin.com/in/yagyeshvyas) · [Portfolio](https://yagyesh-vyas-g11k379.gamma.site/) · [GitHub](https://github.com/yagyeshVyas)

⭐ If this helped you land a job, please star the repo!
    """)