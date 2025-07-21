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

A tool that helps job seekers generate tailored resumes for specific job descriptions using LLMs. Built with Streamlit, OpenAI, and Pandoc.

[![🤗 Spaces](https://img.shields.io/badge/🤗%20Spaces-Deployed-blue)](https://huggingface.co/spaces/msmalmir/smart-resume-optimizer)
---

<!-- HF README END -->

<!-- GITHUB DEV DOCS START -->

## 🚀 Features

- Upload your resume and job description
- Get a clean, optimized Markdown resume
- Instant PDF download
- No data is stored

## 🛠️ For Developers

Clone the repo and run locally with Docker, or use Codespaces for instant cloud dev.

```bash
docker build -t smart-resume .
docker run -p 7860:7860 smart-resume
