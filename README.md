<div align="center">

# 📄 MarkDrop

### Drop any file. Get clean Markdown.

**Optimized for LLMs like ChatGPT, Claude, Gemini, Grok & NotebookLM.**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-markdrop--production.up.railway.app-blue?style=for-the-badge)](https://markdrop-production.up.railway.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=for-the-badge&logo=railway)](https://railway.app)

</div>

---

## 🤔 Why MarkDrop?

AI models work best with **clean, structured text** — not messy PDFs or bloated Word files.

MarkDrop strips formatting noise and converts any document into high-fidelity Markdown, so you can paste it straight into ChatGPT, Claude, or Gemini without any preprocessing.

**No sign-up. No file storage. No nonsense.**

---

## ✨ Features

- 🗂️ **7 supported formats** — PDF, DOCX, PPTX, XLSX, CSV, HTML, TXT, and Images
- ⚡ **Instant conversion** — powered by Microsoft's MarkItDown engine
- 👁️ **Live preview** — see rendered Markdown before copying or downloading
- 📋 **One-click copy** — paste directly into any AI tool
- 💾 **Download as .md** — save for local use or pipelines
- 🔒 **Privacy-first** — files are never stored on the server
- 🎯 **Drag & drop UI** — zero friction, works from any browser

---

## 🎬 Demo

> Upload a PDF → get clean Markdown in seconds

<!-- Record a quick GIF and add it here -->
<!-- ![MarkDrop Demo](./assets/demo.gif) -->

🔗 **Try it live:** [markdrop-production.up.railway.app](https://markdrop-production.up.railway.app/)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI |
| Conversion Engine | Microsoft MarkItDown |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Railway |

---

## 📦 Run Locally

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/sydystic/Markdrop.git
cd Markdrop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload

# 4. Open in browser
# http://localhost:8000
```

---

## 📁 Project Structure

```
Markdrop/
├── main.py              # FastAPI app + conversion logic
├── static/              # Frontend (HTML, CSS, JS)
├── requirements.txt     # Python dependencies
├── Procfile             # Railway deployment config
└── README.md
```

---

## 🧠 How It Works

```
User uploads file (PDF / DOCX / PPTX / XLSX / CSV / HTML / Image)
        ↓
FastAPI receives file via multipart upload
        ↓
Microsoft MarkItDown processes and extracts structured content
        ↓
Clean Markdown returned to frontend
        ↓
User previews, copies, or downloads the .md file ✅
```

---

## 🗺️ Roadmap

- [ ] Batch file conversion (multiple files at once)
- [ ] API endpoint for programmatic access
- [ ] Markdown customization options (heading levels, table style)
- [ ] Browser extension for converting web pages
- [ ] Integration with Notion, Obsidian

---

## 👤 Author

**Siddhi** — [@sydystic](https://github.com/sydystic) · [LinkedIn](https://www.linkedin.com/in/siddhikurne/)

<div align="center">
  <sub>Built for developers and AI power users who hate copy-paste hell.</sub>
</div>
