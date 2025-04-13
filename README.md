# 🩺 MedBot – Local Medical Assistant (WIP)

MedBot is a fully local, privacy-respecting medical assistant. It answers user questions using only trusted medical documents (PDFs) provided by the user.

## Features

- 🔍 Embeds and retrieves from chunked medical documents
- 🧠 Exact and semantic hybrid search
- 🧾 100% source-grounded answers
- 🤖 LLM answer generation coming soon

## Folder Structure

- `data/raw_documents/` → medical PDFs
- `data/chunks/` → preprocessed text chunks
- `embeddings/` → ChromaDB vector DB
- `scripts/` → processing & search scripts

## Next Steps

- [ ] Integrate LLM (Mistral / Gemma)
- [ ] Add a Streamlit UI
