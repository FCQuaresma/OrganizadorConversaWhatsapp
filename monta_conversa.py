"""
Script para gerar um PDF em A4 reunindo:
– textos (.txt, .md)
– imagens (.jpg, .jpeg, .png)
– outros arquivos (audio, docx, pdf etc) como ANEXOS

Requer:
pip install reportlab pypdf pillow
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
from pypdf import PdfReader, PdfWriter

# ✅ IMAGEM SEM CORTES EM A4
def make_page_from_image(c: canvas.Canvas, img_path: str, page_size=A4, margin=30):
    try:
        img = Image.open(img_path)
        w, h = img.size

        max_w = page_size[0] - 2 * margin
        max_h = page_size[1] - 2 * margin

        scale = min(max_w / w, max_h / h)
        new_w = w * scale
        new_h = h * scale

        x = (page_size[0] - new_w) / 2
        y = (page_size[1] - new_h) / 2

        c.drawImage(img_path, x, y, width=new_w, height=new_h, preserveAspectRatio=True)
        c.showPage()

    except Exception as e:
        print("Erro imagem:", img_path, e)

# ✅ TEXTO SEM CORTES EM A4 (COM QUEBRA AUTOMÁTICA E PAGINAÇÃO)
def make_page_from_text(c: canvas.Canvas, text: str, page_size=A4, margin=50):
    max_width = page_size[0] - 2 * margin
    x = margin
    y = page_size[1] - margin

    textobject = c.beginText(x, y)
    textobject.setFont("Helvetica", 10)

    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        line = ""

        for word in words:
            test_line = line + word + " "
            if c.stringWidth(test_line, "Helvetica", 10) <= max_width:
                line = test_line
            else:
                textobject.textLine(line)
                line = word + " "

                if textobject.getY() <= margin:
                    c.drawText(textobject)
                    c.showPage()
                    textobject = c.beginText(x, page_size[1] - margin)
                    textobject.setFont("Helvetica", 10)

        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()

# ✅ CRIAÇÃO DO PDF
def create_pdf_from_folder(folder: str, output_pdf: str):
    files = []
    for root, dirs, fs in os.walk(folder):
        for f in fs:
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            files.append((mtime, path))

    files.sort(key=lambda x: x[0])

    temp_pdf = output_pdf + ".tmp.pdf"
    c = canvas.Canvas(temp_pdf, pagesize=A4)

    attachments = []

    for mtime, path in files:
        ext = Path(path).suffix.lower()

        if ext in [".jpg", ".jpeg", ".png"]:
            make_page_from_image(c, path)

        elif ext in [".txt", ".md"]:
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            make_page_from_text(c, text)

        else:
            attachments.append(path)

    c.save()

    reader = PdfReader(temp_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for attach in attachments:
        with open(attach, "rb") as f:
            data = f.read()
        writer.add_attachment(Path(attach).name, data)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print("✅ PDF criado em A4, sem cortes:", output_pdf)

# ✅ EXECUÇÃO PELO TERMINAL
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Uso correto:")
        print("python monta_conversa.py <pasta_de_entrada> <saida.pdf>")
    else:
        create_pdf_from_folder(sys.argv[1], sys.argv[2])
