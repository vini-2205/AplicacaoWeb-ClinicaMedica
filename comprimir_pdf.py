from pypdf import PdfReader, PdfWriter

def comprimir_pdf(nome : str):
    reader = PdfReader(nome)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.write(page)

    novo_nome = nome.removesuffix(".pdf")

    with open(novo_nome, "wb") as f:
        writer.write(f)