# app.py
import streamlit as st
from backend.parser import extract_text_from_pdf
from backend.generate_optimized_resume import get_tailored_resume
from backend.pdf_render_pandoc import render_pandoc_resume
from backend.pdf_render_latex import render_latex_resume
from backend.get_resume_skills import extract_skills_from_resume
from backend.generate_cover_letter import generate_cover_letter_pdf
import io
import re
import base64
import time

default_pdf_prompt = """
Your objective is to generate a compelling, professional, one-page resume in Markdown format, tailored to the provided job description. This resume will be converted directly to PDF, so it must be clean, structured, and formatted strictly in Markdown.
If the resume contains tools, frameworks, or skills not mentioned in the job description, replace them with similar or more relevant ones only if they are logically equivalent. For example, replace “Tableau” with “PowerBI” if PowerBI is mentioned in the job description. Do not replace if the substitution is not ethically or professionally accurate.
Goal:
Generate a resume that:
Highlights measurable achievements (use the XYZ format: Accomplished X, measured by Y, by doing Z),
Prioritize listing projects from most relevant to least relevant based on the job description.
Briefly mention the tools used and skills developed in each project if relevant, 
Identify and prioritize keywords and skills (hard and soft) in the job description,
Do not invent or add any projects, skills, tools, courses, or experiences that do not exist in the original resume. Only use content from the provided resume. Be strictly truthful and ethical
If possible, while staying honest, incorporate as many relevant keywords from the job description as you can to optimize the resume for Applicant Tracking Systems (ATS).
Includes all specified sections with bullet points where appropriate,
Follows consistent and professional formatting,
Uses Markdown section headers and bullet points,
Avoid generic or vague claims.
Include only the most relevant projects and publications based on the job description.
Remove any projects that are not closely aligned with the target role or do not showcase relevant skills.
Select and list only the top 1–2 publications that best support the role, focusing on research areas, tools, or methods that match the job description.
Instructions:
Do not include triple backticks, YAML blocks, or any explanations. Only output the Markdown-formatted resume.
Use markdown-style section headers like ## SUMMARY, ## EXPERIENCE, etc.
Separate each section with a line (—-).
Use bullet points for EXPERIENCE, TECHNICAL SKILLS, PUBLICATIONS, RELATED COURSES, and LEADERSHIP & MENTORSHIP.
Keep total content to about 400–500 words (1 page).
Write in third-person, professional tone. No first-person pronouns or buzzwords.
Use strong action verbs (e.g., Led, Built, Reduced, Optimized).
Include at least five quantified achievements.
Ensure content flows logically and supports job relevance.
Additional Instructions:
Do not include SUMMARY
Format the ## EDUCATION section to minimize space, following this layout:

- University of Texas at San Antonio, PhD Electrical and Computer Engineering | 2022–Present
- Tarbiat Modares University, MS Electrical and Computer Engineering | 2013–2016
- Enghelab Eslami Technical University, BS Electrical Engineering | 2009–2013 

​
Sections to Include (mandatory, even if one or two are empty — include placeholder content if necessary),
Header section (mandetory): 
Extract the name, email, phone number, location, and links (LinkedIn, GitHub, Google Scholar) from the original resume.
At the very top middle of the Markdown output, include them in this exact format:
”
# **Mostafa Malmir** (bring the name to the middle of the page)
malmir.edumail@gmail.com | (210) 350–9263 | San Antonio, TX | [LinkedIn.com](https://linkedin.com/in/mostafa-malmir) | [GitHub.com](https://github.com/momalmir) | [Google Scholar](https://scholar.google.com/citations?user=GZ4wP8YAAAAJ&hl=en)”
*Do not separate continue on the SUMMARY section*
SUMMARY
seperate with a line 
EXPERIENCE
seperate with a line 
TECHNICAL SKILLS
seperate with a line 
EDUCATION
seperate with a line 
RELATED COURSES AND CERTIFICATES
(**separate the items in this section with | or a small black circles in inline do not make bullet points**)
seperate with a line 
SELECTED PUBLICATIONS
seperate with a line 
LEADERSHIP AND MENTORSHIP
Formatting Reminders:
Do not use LaTeX formatting, tables, or HTML.
Ensure all bullet lists are clean -Item.
Minimize vertical space between sections and bullet points to maximize content on a single page.
Do not add extra blank lines between bullets or section headers unless necessary for clarity.
Make sure no section is skipped, even if it's empty — use "N/A" or a single bullet like Available upon request.
Output Format:
Just the formatted resume in Markdown with clean headers and bullet points — no extra text or formatting artifacts.
"""


default_latex_prompt = """
- Please modify the latex original resume to emphasize the most relevant skills, projects, and experience for the job.
- Do not change the latex structure, syntax, or formatting commands.
- Do not include triple backticks, YAML blocks, or any explanations. Only output the revised LaTeX file content directly.
- Your task is to modify the **content** if needed (not structure) of the LaTeX resume to emphasize the most relevant skills, projects, and experience for the job.
- Try to keep the resume to one and half page if possible.
- Try to do not change the project that much if it is not necessary.
- Keep relevant skills and experience for the job and remove the less relevant ones if needed to save space.
- Keep the Selected Publications section but only keep at most 2 of the most relevant ones to the job.
- Keep the Leadership and Mentorship section

- If the resume contains tools, frameworks, or skills not mentioned in the job description, replace them with similar or more relevant ones only if they are logically equivalent. For example, replace “Tableau” with “PowerBI” if PowerBI is mentioned in the job description. Do not replace if the substitution is not ethically or professionally accurate.
- Highlights measurable achievements (use the XYZ format: Accomplished X, measured by Y, by doing Z),
- Prioritize listing projects from most relevant to least relevant based on the job description.
- Briefly mention the tools used and skills developed in each project if relevant,
- Identify and prioritize keywords and skills (hard and soft) in the job description,
- **Do not invent or add any projects, skills, tools, courses, or experiences that do not exist in the original resume. Only use content from the provided resume. Be strictly truthful and ethical**
- If possible, while staying honest, incorporate as many relevant keywords from the job description as you can to optimize the resume for Applicant Tracking Systems (ATS).
- Follows consistent and professional formatting,
- Avoid generic or vague claims.
- Include only the most relevant projects and publications based on the job description.
- Remove any projects that are not closely aligned with the target role or do not showcase relevant skills.
- Select and list only the top 1–2 publications that best support the role, focusing on research areas, tools, or methods that match the job description.

- Ensure all environments (e.g., `\begin{itemize}`) are properly closed with their corresponding `\end{...}`

- Escape all LaTeX special characters in text content. For example:
  - Use `\&` instead of `&`
  - Use `\%` instead of `%`
  - Use `\_` instead of `_`
  - Use `\#` instead of `#`
  - Use `\textasciitilde{}` instead of `~`
  - Use `\textasciicircum{}` instead of `^`
  - Use `\textbackslash{}` instead of `\`

❌ Do NOT:
- Add a new `\section` not in the original
- Convert content to Markdown or plain text
- Break the LaTeX syntax
- Output code fences (no ```latex)
- Do not include triple backticks, YAML blocks, or any explanations.

🛠️ Output:
Return valid LaTeX starting with `\documentclass` and ending with `\end{document}`

"""

# default_latex_prompt = """
# You are a resume editing assistant.

# Your task is to revise the following LaTeX-formatted resume **without altering the LaTeX structure, syntax, or formatting commands**. 
# Your task is to modify the **content** (not structure) of the LaTeX resume to emphasize the most relevant skills, projects, and experience for the job.


# ---

# **Instructions:**

# - Do NOT delete or change any LaTeX commands (`\section`, `\begin{itemize}`, `\item`, etc.)
# - Keep the formatting of fonts, spacing, and layout exactly as in the original
# - Only modify the **text inside sections and bullet points** (e.g., reword descriptions, reorder items, replace skills with more relevant ones if appropriate)
# - Do NOT introduce new sections or add entirely new content
# - DO NOT fabricate, exaggerate, or invent any achievements or skills
# - Optimize language to highlight achievements, use active verbs, and include metrics when available
# - Focus especially on modifying the most relevant sections (e.g., `\section{Experience}`, `\section{Projects}`, `\section{Skills}`) to match keywords and qualifications in the job description
# - Keep content concise — do not add lengthy paragraphs
# - Ensure all environments (e.g., `\begin{itemize}`) are properly closed with their corresponding `\end{...}`
# - Do NOT output code blocks, explanations, or backticks — only return the revised LaTeX file content directly
# - Your final output must stay within the original layout constraints and should not cause the resume to exceed one page when rendered as PDF.
# - You may **remove or shorten** items or skills that are clearly unrelated to the job posting, if needed to save space
# - Do not output explanations, Markdown, or backticks — return only the raw LaTeX resume code

# ---
# 📝 Page Length Constraint:
# Ensure that the revised LaTeX resume fits **on a single page** when compiled to PDF. 
# To do this:
# - Trim overly detailed bullet points
# - Condense redundant or less relevant content
# - Prioritize clarity and brevity
# - Avoid adding new content unless necessary
# - Avoid wordiness or long sentences


# ---

# **Example of allowed edits:**

# ✅ Change:
# - Reorder, reword, or replace bullet points to match job keywords
# - Modify only the **inside** of existing sections or items
# - Add achievements, active verbs, or clarifications if supported by original resume
# ❌ Do NOT:
# - Add a new `\section` not in the original
# - Convert content to Markdown or plain text
# - Break the LaTeX syntax
# - Output code fences (no ```latex)

# ---

# 🛠️ Output:
# Return valid LaTeX starting with `\documentclass` and ending with `\end{document}`

# """


#- `\item Developed X tool` → `\item Built X tool to streamline workflow, reducing manual effort by 40%`



# default_latex_prompt = """
# You are given the full LaTeX source of a resume and a job description.

# Your task is to modify the **content** (not structure) of the LaTeX resume to emphasize the most relevant skills, projects, and experience for the job.

# 🟢 Do:
# - Reorder, reword, or replace bullet points to match job keywords
# - Modify only the **inside** of existing sections or items
# - Add achievements, active verbs, or clarifications if supported by original resume

# 🔴 Do not:
# - Delete any sections (like Publications, Leadership, etc.)
# - Add or remove \section or \begin{itemize} blocks
# - Break LaTeX syntax or convert to Markdown
# - Output code fences (no ```latex)

# 🛠️ Output:
# Return valid LaTeX starting with `\documentclass` and ending with `\end{document}`

# """



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

# --- Choose Resume Format ---
resume_format = st.radio(
    "🗂️ Select your resume format",
    options=["PDF", "LaTeX (.tex)"],
    index=0,
    horizontal=True,
    help="Choose whether to upload a PDF resume or a LaTeX (.tex) resume."
)

# --- Upload PDF Resume ---
st.subheader("📄 Upload Resume")
if resume_format == "PDF":
    uploaded_file = st.file_uploader("**Your resume (PDF only)**", type=["pdf"])
else:
    uploaded_file = st.file_uploader("**Your resume (LaTeX .tex only)**", type=["tex"])


# --- Resume Ingestion ---
if uploaded_file:
    resume_bytes = uploaded_file.read()
    if resume_format == "LaTeX (.tex)":
        resume_text = resume_bytes.decode("utf-8")
    else:
        resume_text = extract_text_from_pdf(io.BytesIO(resume_bytes))
    st.session_state["resume_text"] = resume_text
    st.success("Resume loaded successfully.")
    st.info("Note: Skills and cover letter will use the latest uploaded or optimized resume.")


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


# --- Optimize Resume ---
st.subheader("🚀 Optimize Resume")

if st.button("✨ Optimize Resume"):
    if not uploaded_file or not job_description or not api_key:
        st.error("Please fill out all required fields.")
    else:
        with st.spinner("Optimizing your resume... ⏳"):
            resume_text = st.session_state.get("resume_text", "")
            tailored_md = get_tailored_resume(
                resume_text=resume_text,
                job_description=job_description,
                api_key=api_key,
                prompt=custom_prompt.strip() if custom_prompt else (
                    default_latex_prompt if resume_format == "LaTeX (.tex)" else default_pdf_prompt
                ),
                model=model_name
            )
            st.session_state["tailored_md"] = tailored_md
            st.session_state["resume_text"] = tailored_md # <- use for downstream


            pdf_bytes = (
                render_latex_resume(tailored_md)
                if resume_format == "LaTeX (.tex)"
                else render_pandoc_resume(tailored_md)
            )


            def clean_filename_part(text: str) -> str:
                text = text.replace("-", " ").replace(",", "")
                return re.sub(r"[^\w\s]", "", text).replace(" ", "_")


            words = resume_text.strip().split()
            safe_name = full_name.replace(" ", "_") if full_name else (
                f"{words[0]}_{words[1]}" if len(words) >= 2 else "Anonymous"
            )
            safe_job = clean_filename_part(job_title)
            safe_company = clean_filename_part(company_name)
            file_name = f"{safe_name}_{safe_company}_{safe_job}_resume.pdf"


            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1200" height="700" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)


            st.download_button(
                label="📥 Download Optimized Resume",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )
        
# --- Extract Skills Section ---
st.subheader("🧠 Extract Skills from Resume")
skill_model = st.text_input(
    "🔍 Model for Skill Extraction (use a lightweight model for faster performance and lower cost)",
    value="moonshotai/kimi-k2",
    help="Use a lightweight model to extract skills from the generated resume."
)

if st.button("📋 Extract Skills"):
    if not st.session_state.get("resume_text") or not api_key:
        st.error("Please upload or optimize your resume and enter API key.")
    else:
        with st.spinner("Extracting skills..."):
            skills = extract_skills_from_resume(
            st.session_state["resume_text"], api_key, skill_model
            )
            st.success("Here are the extracted skills:")
            st.code(skills, language='text')


# --- Cover Letter Section ---
st.subheader("✉️ Generate Cover Letter")


custom_cover_prompt = st.text_area(
    "📝 Custom Prompt for Cover Letter (optional)",
    placeholder="Leave blank to use the default professional tone.",
    height=200
)


if st.button("✏️ Create Cover Letter"):
    if not st.session_state.get("resume_text") or not job_description or not api_key:
        st.error("Please fill out all required fields.")
    else:
        with st.spinner("Generating cover letter... ⏳"):
            if full_name:
                safe_name = full_name.replace(" ", "_")
            else:
                words = st.session_state.get("resume_text", "").strip().split()
                safe_name = f"{words[0]}_{words[1]}" if len(words) >= 2 else "Anonymous"


            pdf_bytes, file_name = generate_cover_letter_pdf(
                resume_text=st.session_state.get("resume_text", ""),
                job_description=job_description,
                api_key=api_key,
                full_name=full_name,
                job_title=job_title,
                company_name=company_name,
                prompt=custom_cover_prompt,
                model=model_name,
                font_size="12pt"
            )


            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1200" height="700" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)


            st.download_button(
                label="📥 Download Cover Letter PDF",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )