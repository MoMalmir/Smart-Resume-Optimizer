# backend/pdf_render_latex.py

import subprocess
import tempfile
import os

def render_latex_resume(tex_content: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        # Save .tex content
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

        # Compile to PDF using xelatex (ensure xelatex is installed)
        subprocess.run([
            "xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path
        ], check=True)

        # Read the generated PDF
        with open(pdf_path, "rb") as f:
            return f.read()
