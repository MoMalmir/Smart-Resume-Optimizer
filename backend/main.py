from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import io
import time
from backend.parser import extract_text_from_pdf
from backend.llm_interface import get_tailored_resume
from fastapi.responses import StreamingResponse
#from backend.latex_exporter import render_latex_resume
from backend.pdf_render_pandoc import render_pandoc_resume

app = FastAPI()
session_cache = {}


@app.get("/")
def home():
    return {"message": "Resume Optimizer is live!"}


@app.post("/optimize-and-export")
async def optimize_and_export_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    api_key: str = Form(...),
    custom_prompt: str = Form(...),
    cache_key: str = Form(""),
    use_cache: bool = Form(False),
):
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(io.BytesIO(resume_bytes))

    if use_cache and cache_key:
        session_cache[cache_key] = {"key": api_key, "expires": time.time() + 1800}

    key_to_use = api_key
    if use_cache and cache_key in session_cache:
        if session_cache[cache_key]["expires"] > time.time():
            key_to_use = session_cache[cache_key]["key"]
        else:
            del session_cache[cache_key]

    tailored = get_tailored_resume(
        resume_text=resume_text,
        job_description=job_description,
        api_key=key_to_use,
        prompt=custom_prompt,
    )

    # Generate PDF from Markdown
    pdf_bytes = render_pandoc_resume(tailored)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=optimized_resume.pdf"},
    )
