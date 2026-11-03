import pdfplumber

pdf_path = "/Users/madhavathavale/Downloads/Capgain.pdf"
txt_path = "output.txt"

with pdfplumber.open(pdf_path) as pdf:
    with open(txt_path, "w") as f:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                f.write(text + "\n")