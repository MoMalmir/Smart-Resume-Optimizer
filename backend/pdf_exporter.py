
import markdown
from weasyprint import HTML

def markdown_to_pdf(markdown_text: str) -> bytes:
    html_content = markdown.markdown(markdown_text)
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes