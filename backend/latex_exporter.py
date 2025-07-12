import subprocess
import tempfile
import os

TEMPLATE_PATH = "backend/resume_template.tex"

def render_latex_resume(content: str) -> bytes:
    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()

    # Insert content into the placeholders — you'll need to structure this yourself
    filled = template \
        .replace("%%SUMMARY%%", extract_section(content, "SUMMARY")) \
        .replace("%%EXPERIENCE%%", extract_section(content, "EXPERIENCE")) \
        .replace("%%SKILLS%%", extract_section(content, "TECHNICAL SKILLS")) \
        .replace("%%COURSES%%", extract_section(content, "RELATED COURSES AND CERTIFICATS")) \
        .replace("%%PUBLICATIONS%%", extract_section(content, "SELECTED PUBLICATIONS"))

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        with open(tex_path, "w") as f:
            f.write(filled)

        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path],
                       cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(result.stdout.decode())
        print(result.stderr.decode())

        pdf_path = os.path.join(tmpdir, "resume.pdf")
        if not os.path.exists(pdf_path):
            raise RuntimeError("PDF generation failed")

        with open(pdf_path, "rb") as f:
            return f.read()

def extract_section(text: str, heading: str) -> str:
    """
    Extract section from generated content based on markdown-style headings.
    Assumes: section titles are like ## SUMMARY, ## EXPERIENCE, etc.
    """
    lines = text.splitlines()
    section_lines = []
    capturing = False
    for line in lines:
        if line.strip().upper().startswith("## "):
            capturing = line.strip().upper()[3:] == heading.upper()
            continue
        if capturing:
            if line.strip().upper().startswith("## "):
                break
            section_lines.append(line)
    return "\n".join(section_lines).strip()
