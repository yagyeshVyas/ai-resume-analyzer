# 🎯 AI Resume Analyzer & Job Match Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-1.32-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Google_Gemini-AI-orange?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

> **Instantly know how well your resume matches any job — and exactly how to fix it.**

An AI-powered web app that analyzes your resume against job descriptions, gives you an ATS score, finds skill gaps, and suggests improvements — all for **free**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **ATS Score** | Simulate how ATS systems rate your resume (0-100) |
| 🎯 **Job Match Score** | Overall alignment with the job description |
| ✅ **Matched Skills** | Skills you already have that the job wants |
| ❌ **Missing Skills** | Critical keywords you need to add |
| 💡 **Improvements** | Specific, actionable suggestions to strengthen your resume |
| ⚡ **Quick Wins** | Things you can fix in under 10 minutes |
| 📈 **Progress Dashboard** | Track your scores across multiple job applications |
| 📋 **History Tracking** | SQLite database stores all your past analyses |
| ⬇️ **Download Report** | Export your analysis as a text file |

---

## 🚀 Quick Start

### Option 1: Run Locally (2 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

### Option 2: Deploy Free on Streamlit Cloud

1. Fork this repo on GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub → select this repo → click Deploy
4. Done! Your app is live at `https://YOUR_APP.streamlit.app`

---

## 🔑 Get Your Free Gemini API Key

1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy and paste it into the app sidebar

**Free tier limits:** 15 requests/minute · 1 million tokens/day — more than enough!

---

## 🛠️ Tech Stack

```
Frontend    → Streamlit (Python web framework)
AI Engine   → Google Gemini 1.5 Flash API
Database    → SQLite (local, private, no setup)
Charts      → Plotly
PDF Parser  → pdfplumber
Language    → Python 3.11
Hosting     → Streamlit Cloud (free)
```

---

## 📁 Project Structure

```
ai-resume-analyzer/
│
├── app.py              # Main Streamlit application (UI + routing)
├── analyzer.py         # AI analysis logic (Gemini API + PDF parsing)
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

---

## 🔒 Privacy

- Your resume is **never stored on any external server**
- Analysis data is saved **only to your local SQLite database**
- Your API key is **only held in your browser session** — never saved
- You can delete any analysis from the Dashboard at any time

---

## 💡 How to Use

1. **Get a free Gemini API key** (link above)
2. **Enter your API key** in the sidebar
3. **Upload your resume** (PDF) or paste the text
4. **Paste the job description** from LinkedIn, Indeed, etc.
5. **Click Analyze** and wait ~15 seconds
6. **Review your scores, fix issues, re-analyze** until you're confident
7. **Track progress** in the Dashboard over time

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 👨‍💻 Author

**Yagyesh Vyas** — Data & IT Developer | CS Graduate Student  
[LinkedIn](https://www.linkedin.com/in/yagyeshvyas) · [Portfolio](https://yagyesh-vyasg11k379.gamma.site/)

---

⭐ **If this helped you land a job, please star the repo!**