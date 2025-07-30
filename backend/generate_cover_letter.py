
# backend/generate_cover_letter.py
from openai import OpenAI
from .pdf_render_pandoc import render_pandoc_resume  # reuse the same renderer
import base64
import re

def extract_name_from_resume(resume_text: str) -> str:
    lines = resume_text.strip().splitlines()
    for line in lines:
        if line.strip() and len(line.strip().split()) >= 2:
            return line.strip().replace(" ", "_")
    return "Anonymous"

def generate_cover_letter_pdf(
    resume_text: str,
    job_description: str,
    api_key: str,
    full_name: str = "",
    job_title: str = "",
    company_name: str = "",
    prompt: str = "",
    model: str = "anthropic/claude-3.7-sonnet",
    font_size: str = "12pt"
) -> tuple[bytes, str]:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    default_instructions = (
        "Write a professional, concise, and personalized cover letter based on the resume and job description below.\n\n"
        "Use 3–5 paragraphs to highlight relevant qualifications, experience, and motivation.\n\n"
        "Keep it under one page. Avoid generic statements and include specific alignment with the role.\n\n"
        "Make sure there is space between each paragraph for readability. End with a friendly call to action."
    )

    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    RESUME TEXT:
    {resume_text}

    INSTRUCTIONS:
    {prompt or default_instructions}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    # Ensure there is a blank line between paragraphs
    raw_content = response.choices[0].message.content.strip()
    cover_letter_md = "\n\n".join([p.strip() for p in raw_content.split("\n") if p.strip()])


    # Render PDF
    pdf_bytes = render_pandoc_resume(cover_letter_md, template_file="cover_letter_template.tex")


    # # Fallback to parsed name if not provided
    # if not full_name:
    #     name_safe = extract_name_from_resume(resume_text)
    # else:
    #     name_safe = full_name.replace(" ", "_")

    # job_safe = job_title.replace(" ", "_") or "Job"
    # company_safe = company_name.replace(" ", "_") or "Company"

    # file_name = f"{name_safe}_{company_safe}_{job_safe}_CV.pdf"

    # Clean function to remove unwanted characters
    def clean_filename_part(text: str) -> str:
        text = text.replace("-", " ").replace(",", "") 
        return re.sub(r"[^\w\s]", "", text).replace(" ", "_")  # Remove special chars, keep words joined by _
    
    # Generate safe names
    safe_name = full_name.replace(" ", "_") if full_name else (
        f"{words[0]}_{words[1]}" if len(words) >= 2 else "Anonymous"
    )
    safe_job = clean_filename_part(job_title)
    safe_company = clean_filename_part(company_name)
    file_name = f"{name_safe}_{company_safe}_{job_safe}_CV.pdf"

    return pdf_bytes, file_name
