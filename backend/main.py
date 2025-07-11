from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import io
import time
from backend.parser import extract_text_from_pdf
from backend.llm_interface import get_tailored_resume
from backend.pdf_render_pandoc import render_pandoc_resume


app = FastAPI()

# Allow frontend (like React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    cache_key: str = Form(None),
    use_cache: bool = Form(False),
):
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(io.BytesIO(resume_bytes))

    # Cache API key
    if use_cache and cache_key:
        session_cache[cache_key] = {
            "key": api_key,
            "expires": time.time() + 1800
        }


    # Retrieve from cache if exists and still valid
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


    pdf_bytes = render_pandoc_resume(tailored)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=optimized_resume.pdf"},
    )
