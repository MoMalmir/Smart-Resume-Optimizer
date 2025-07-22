# app/Home.py
import streamlit as st
from backend.parser import extract_text_from_pdf
from backend.llm_interface import get_tailored_resume
from backend.pdf_render_pandoc import render_pandoc_resume
import io
import base64
import time


# entry point and navigation menu
st.set_page_config(page_title="Smart Resume Optimizer", layout="wide")

st.title("👋 Welcome to Smart Resume Optimizer")
st.write("Tailor your resume to a specific job using LLMs.")

st.markdown("""
Use the sidebar to navigate between:
- ✨ **Run App**: Tailor and export your resume
- 📘 **Explanation**: Learn how the tool works
- 👤 **About Me**: Learn more about the developer
""")

# --- Upload PDF Resume ---
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("**Your resume (PDF only)**", type=["pdf"])

# --- API Key + Caching ---
st.subheader("🔐 API Key & Model")
api_key = st.text_input(
    "🔑 **OpenRouter API Key**",
    placeholder="Paste your OpenRouter API key here",
    type="password",
    help="Supports models from Claude, GPT-4, Mistral, etc."
)
st.markdown(
    "Don't have an API key? [Get one here](https://openrouter.ai/) _(free & paid models available)_"
)

use_cache = st.checkbox("🗃️ Remember this API key for this session?")
cache_duration = st.slider("⏱️ How long to cache (minutes)", min_value=5, max_value=60, value=30)
cache_key = "api_key"

if use_cache:
    now = time.time()
    expires = now + cache_duration * 60
    if api_key:
        st.session_state[cache_key] = {"key": api_key, "expires": expires}
    elif cache_key in st.session_state:
        if st.session_state[cache_key]["expires"] > now:
            api_key = st.session_state[cache_key]["key"]
        else:
            del st.session_state[cache_key]

# --- Prompt customization (optional) ---
st.subheader("✏️ Prompt & Personalization")

custom_prompt = st.text_area("📝 **Custom prompt** _(optional)_", height=250)

# --- Model selection ---
model_name = st.text_input(
    "🧠 **Model name** (from OpenRouter e.g. anthropic/claude-3.7-sonnet,anthropic/claude-sonnet-4, gpt-4-turbo, deepseek/deepseek-chat-v3-0324)",
    value="anthropic/claude-3.7-sonnet",  # default value
    help="Enter any model ID supported by OpenRouter (e.g. anthropic/claude-3.7-sonnet,anthropic/claude-sonnet-4, gpt-4-turbo, deepseek/deepseek-chat-v3-0324)"
)

# --- Optional full name input ---
full_name = st.text_input("👤 **Your full name** _(optional)_", placeholder="e.g. John_Doe")


# --- Job info ---
st.subheader("💼 Job Info")

job_title = st.text_input("📌 **Job Title**", placeholder="e.g. Data Scientist")
company_name = st.text_input("🏢 **Company Name**", placeholder="e.g. Hugging Face")
job_description = st.text_area("🧾 **Job Description**", height=250)

# --- Process Resume ---
st.subheader("🚀 Optimize")

if st.button("✨ Optimize Resume"):
    if not uploaded_file or not job_description or not api_key:
        st.error("Please fill out all required fields.")
    else:
        with st.spinner("Optimizing your resume... ⏳"):
            resume_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(io.BytesIO(resume_bytes))

            tailored_md = get_tailored_resume(
                resume_text=resume_text,
                job_description=job_description,
                api_key=api_key,
                prompt=custom_prompt,
                model=model_name
            )

            pdf_bytes = render_pandoc_resume(tailored_md)

            if full_name:
                safe_name = full_name.replace(" ", "_")
            else:
                words = resume_text.strip().split()
                safe_name = f"{words[0]}_{words[1]}" if len(words) >= 2 else "Anonymous"

            safe_job = job_title.replace(" ", "_")
            safe_company = company_name.replace(" ", "_")
            file_name = f"{safe_name}_{safe_job}_{safe_company}.pdf"

            # Show preview
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1200" height="700" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

            # Download button
            st.download_button(
                label="📥 Download Optimized Resume",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )
        
