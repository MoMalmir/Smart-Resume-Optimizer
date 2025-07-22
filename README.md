---
title: Smart Resume Optimizer
emoji: 🎯
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

<!-- HF README START -->

# 🧠 Smart Resume Optimizer

Smart Resume Optimizer helps job seekers generate **tailored, optimized resumes** based on job descriptions using LLMs via [OpenRouter](https://openrouter.ai/). It supports models like Claude 3, GPT-4, Mistral, DeepSeek, and more.

[![🤗 Spaces](https://img.shields.io/badge/🤗%20Spaces-Deployed-blue)](https://huggingface.co/spaces/msmalmir/smart-resume-optimizer)

---

## 📚 Table of Contents

- [🧠 Smart Resume Optimizer](#-smart-resume-optimizer)
- [✨ How It Works](#-how-it-works)
- [🔐 Privacy Notice](#-privacy-notice)
- [🧾 Requirements](#-requirements)
- [⚙️ Developer Setup](#️-developer-setup)
  - [🔁 Run Locally with Docker](#-run-locally-with-docker)
  - [🧪 Manual Setup (No Docker)](#-manual-setup-no-docker)
  - [🌍 Environment Variables](#-environment-variables)
  - [🧪 Testing (Optional)](#-testing-optional)
  - [🚀 Deployment](#-deployment)
- [🙋‍♂️ Author](#️-author)

---

## ✨ How It Works

1. Upload your **PDF resume**
2. Paste the **job description** you're targeting
3. Enter a **custom prompt** with instructions for tailoring 
4. (Optional) Choose a **model**
5. Click "Optimize" ✨
6. View and download your tailored resume as a **PDF**


The system supports any model on OpenRouter, including:

- `anthropic/claude-3.7-sonnet`
- `gpt-4-turbo`
- `deepseek/deepseek-chat`
- ...and more

---

## 🔐 Privacy Notice

This application runs entirely in your browser and **does not store or send your resume or job description to any third party** except to the selected LLM model via the OpenRouter API (under your API key). We do not log or collect:

- Your OpenRouter API key
- Your uploaded resume
- The job description or tailored output

---

## 🧾 Requirements

To use the hosted app, you’ll need:

- 📄 A resume in **PDF format**
- 📋 A job description you're applying to
- ✍️ A **custom prompt** describing how to tailor the resume
- 🔑 An **OpenRouter API key** (sign up at [openrouter.ai](https://openrouter.ai/))

---

<!-- HF README END -->

<!-- GITHUB DEV DOCS START -->

## ⚙️ Developer Setup

You can clone and run the app locally or build your own Docker container.

### 🔁 Run Locally with Docker

We’ve built a lightweight Docker container for deploying on Hugging Face. It **may work locally**, but for full interactive UI use (with Streamlit), local dev mode is recommended instead.

To try running the container locally:

```bash
docker build -t smart-resume .
docker run -p 7860:7860 smart-resume
```

Visit [http://localhost:7860](http://localhost:7860) after the container starts.

### 🧪 Manual Setup (No Docker)

```bash
git clone https://github.com/msmalmir/Smart-Resume-Optimizer.git
cd Smart-Resume-Optimizer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Home.py
```

### 🌍 Environment Variables

Create a `.env` file in the root or export directly in your terminal:

```env
OPENROUTER_API_KEY=your-api-key-here
```

### 🧪 Testing (Optional)

If you want to contribute or build CI pipelines, you can run basic tests:

```bash
pytest
```

### 🚀 Deployment

This app is deployed automatically to Hugging Face Spaces via GitHub Actions.

To deploy:
- Push to `main`, or
- Trigger the `Deploy` action manually from the GitHub Actions tab

---

## 🙋‍♂️ Author

Built with ❤️ by [@msmalmir](https://github.com/msmalmir)

<!-- GITHUB DEV DOCS END -->
