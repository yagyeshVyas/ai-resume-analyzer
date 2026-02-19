# 🎯 AI Resume Analyzer & Job Match Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-1.32-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/OpenRouter-AI-purple?style=for-the-badge&logo=openai" />
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
| 📞 **Interview Probability** | Realistic chance of getting a callback |
| ✅ **Matched Skills** | Skills you already have that the job wants |
| ❌ **Missing Skills** | Critical keywords you need to add |
| 🚨 **Red Flags** | What recruiters notice negatively in 6 seconds |
| 💰 **Salary Insight** | Estimated salary range based on your profile |
| ⚡ **Quick Wins** | Things you can fix in under 10 minutes |
| 📈 **Progress Dashboard** | Track your scores across multiple job applications |
| 📋 **History Tracking** | SQLite database stores all your past analyses |
| ⬇️ **Download Report** | Export your full analysis as a text file |
| 🌙 **Dark Mode** | Fully supports light and dark mode |

---

## 🤖 Supported AI Models

### 🆓 Free Models (No credit card needed)
| Model | Best For |
|-------|----------|
| ⚡ Gemini 2.0 Flash | Speed + quality — Recommended |
| 🧠 DeepSeek R1 | Best reasoning and analysis |
| 🦙 Llama 3.3 70B | Very smart, open source |
| 🌟 Qwen 2.5 72B | Great overall quality |
| 🔥 Mistral 7B | Fastest responses |

### 💎 Paid Models (tiny cost ~$0.001 per analysis)
| Model | Best For |
|-------|----------|
| 👑 Claude 3.5 Sonnet | Best overall quality |
| 💎 GPT-4o | Top tier accuracy |
| 🚀 GPT-4o Mini | Fast and cheap |
| 🌙 Gemini 2.0 Flash | Latest Google model |
| 🧬 Claude 3 Haiku | Fastest paid model |

---

## 🚀 Quick Start

### Option 1: Run Locally (2 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/yagyeshVyas/ai-resume-analyzer.git
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

## 🔑 Get Your Free OpenRouter API Key

1. Visit [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up with Google (no credit card needed)
3. Click **"Create Key"**
4. Copy the key (starts with `sk-or-...`)
5. Paste it into the app sidebar

**Free tier:** Unlimited access to all free models — no credits needed!  
**Paid models:** Add credits at openrouter.ai for ~$0.001–$0.01 per analysis

---

## 🛠️ Tech Stack

```
Frontend    → Streamlit (Python web framework)
AI Engine   → OpenRouter API (10+ models: GPT-4, Claude, Gemini, DeepSeek, Llama)
Database    → SQLite (local, private, no setup needed)
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
├── analyzer.py         # AI analysis logic (OpenRouter API + PDF parsing)
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

---

## 💡 How to Use

1. **Get a free OpenRouter API key** at [openrouter.ai/keys](https://openrouter.ai/keys)
2. **Enter your API key** in the sidebar
3. **Choose your AI model** — start with Gemini 2.0 Flash (free & fast)
4. **Upload your resume** (PDF) or paste the text
5. **Paste the job description** from LinkedIn, Indeed, etc.
6. **Click Analyze** and wait ~15 seconds
7. **Review your scores** — ATS, Match, Interview Probability
8. **Fix the issues** and re-analyze until you're confident
9. **Track progress** in the Dashboard over time

---

## 🔒 Privacy

- Your resume is **never stored on any external server**
- Analysis data is saved **only on your local machine** in SQLite
- Your API key is **only held in your browser session** — never saved anywhere
- You can delete any analysis from the Dashboard at any time

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — free to use, modify, and share.

---

## 👨‍💻 Author

**Yagyesh Vyas** — Data & IT Developer | CS Graduate Student  
[LinkedIn](https://www.linkedin.com/in/yagyeshvyas) · [Portfolio](https://yagyesh-vyas-g11k379.gamma.site/) · [GitHub](https://github.com/yagyeshVyas)

---

⭐ **If this helped you land a job, please star the repo!**