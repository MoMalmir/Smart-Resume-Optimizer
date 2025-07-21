# app/Explanation.py
import streamlit as st

st.markdown("""
# 🧠 Smart Resume Optimizer

Welcome to the **Smart Resume Optimizer** – an AI-powered tool designed to tailor your resume to specific job postings using advanced natural language processing.

---

### 🚀 What This Tool Does
- 📝 **Parses your uploaded resume**
- 💼 **Analyzes a job description** you provide
- 🤖 **Uses AI to rewrite your resume** to better match the job
- 📄 **Exports a polished PDF resume** based on a clean LaTeX template
- 👀 **Lets you preview before download**

---

### 📌 How to Use
1. **Upload your current resume** (PDF only)
2. **Paste the job description** for the position you're targeting
3. *(Optional)* Add a **custom instruction** (e.g., “Emphasize research skills”)
4. Provide your **OpenAI API key**
5. Click **Optimize Resume**
6. **Preview your tailored resume**, then **download the final PDF**

---

### 🛠️ Notes
- Your data never leaves your browser session.
- API key is used only temporarily to generate output.
- You can reuse the same key during a session by enabling cache.
""", unsafe_allow_html=True)
