import os
from sentence_transformers import SentenceTransformer
import chromadb

CHUNK_DIR = "../data/chunks/"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

client = chromadb.PersistentClient(path="../embeddings/")
collection = client.get_or_create_collection(name="medical_chunks")

existing_ids = set(collection.get()["ids"])

for doc_folder in os.listdir(CHUNK_DIR):
    folder_path = os.path.join(CHUNK_DIR, doc_folder)
    if not os.path.isdir(folder_path):
        continue

    for chunk_file in os.listdir(folder_path):
        if not chunk_file.endswith(".txt"):
            continue

        chunk_path = os.path.join(folder_path, chunk_file)
        chunk_id = f"{doc_folder}_{chunk_file}"  # e.g. NEJM_003.txt

        if chunk_id in existing_ids:
            print(f"⏩ Skipped: {chunk_id}")
            continue

        with open(chunk_path, "r", encoding="utf-8") as f:
            content = f.read()

        embedding = model.encode(content)

        collection.add(
            documents=[content],
            embeddings=[embedding.tolist()],
            ids=[chunk_id],
            metadatas=[{"source": doc_folder, "chunk": chunk_file}]
        )

        print(f"✅ Embedded: {chunk_id}")
