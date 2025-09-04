# backend/pdf_render_latex.py

import subprocess
import tempfile
import os

def render_latex_resume(tex_content: str) -> bytes:
    """
    Render LaTeX resume content into a PDF using xelatex.

    Args:
        tex_content (str): LaTeX string content for the resume.

    Returns:
        bytes: Binary content of the generated PDF.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        # 🔍 Save raw LLM output for debugging if anything goes wrong
        with open("llm_output_debug.tex", "w", encoding="utf-8") as debug_file:
            debug_file.write(tex_content)

        # Save LaTeX content to temp .tex file
        with open(tex_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(tex_content)

        # Compile to PDF with xelatex
        try:
            subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-output-directory", tmpdir,
                    tex_path
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            print("\n❌ Xelatex failed with error:")
            print(e.stdout.decode(errors="ignore"))
            print(e.stderr.decode(errors="ignore"))
            raise RuntimeError("Xelatex failed. Check the above log and `llm_output_debug.tex`.")

        # Read and return compiled PDF
        with open(pdf_path, "rb") as pdf_file:
            return pdf_file.read()
