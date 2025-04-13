import os
from pypdf import PdfReader

RAW_PATH = "../data/raw_documents/"
OUTPUT_PATH = "../data/chunks/"
CHUNK_SIZE = 200        # smaller chunk size
CHUNK_OVERLAP = 100     # large overlap to increase match coverage

os.makedirs(OUTPUT_PATH, exist_ok=True)

def chunk_text(text, size, overlap):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunk = ' '.join(words[i:i + size])
        chunks.append(chunk)
    return chunks

def pdf_to_chunks(pdf_path, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return chunk_text(full_text, chunk_size, overlap)

for filename in os.listdir(RAW_PATH):
    if filename.endswith(".pdf"):
        base_name = os.path.splitext(filename)[0]
        chunk_path = os.path.join(OUTPUT_PATH, base_name)
        os.makedirs(chunk_path, exist_ok=True)

        if len(os.listdir(chunk_path)) > 0:
            print(f"⏩ Skipped (already chunked): {filename}")
            continue

        chunks = pdf_to_chunks(os.path.join(RAW_PATH, filename))
        for i, chunk in enumerate(chunks):
            with open(os.path.join(chunk_path, f"{i:03}.txt"), "w", encoding="utf-8") as f:
                f.write(chunk)

        print(f"✅ Chunked: {filename} into {len(chunks)} chunks")
