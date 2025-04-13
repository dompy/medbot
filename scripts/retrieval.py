import os
import chromadb
from sentence_transformers import SentenceTransformer

CHUNK_DIR = "../data/chunks/"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.PersistentClient(path="../embeddings/")
collection = client.get_collection(name="medical_chunks")

def find_exact_match(query):
    for folder in os.listdir(CHUNK_DIR):
        folder_path = os.path.join(CHUNK_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if not file.endswith(".txt"):
                continue

            file_path = os.path.join(folder_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if query.strip() in content:
                    return (folder, file, content)
    return None

def build_context(query, n_results=10, max_chars=3000):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    seen_ids = set()
    context_blocks = []
    total_chars = 0

    # First: Check for exact match
    exact = find_exact_match(query)
    if exact:
        folder, file, content = exact
        block = f"📘 (Exact match) From {folder} — {file}:\n{content}\n"
        context_blocks.append(block)
        seen_ids.add(f"{folder}_{file}")
        total_chars += len(block)

    # Then: Add semantic results (excluding duplicates)
    for chunk, meta in zip(chunks, metadatas):
        chunk_id = f"{meta['source']}_{meta['chunk']}"
        if chunk_id in seen_ids:
            continue
        block = f"📘 From {meta['source']} (Chunk {meta['chunk']}):\n{chunk}\n"
        if total_chars + len(block) > max_chars:
            break
        context_blocks.append(block)
        total_chars += len(block)

    return "\n\n".join(context_blocks)

if __name__ == "__main__":
    query = input("Enter your medical question or quote:\n> ")
    context = build_context(query)

    print("\n🧠 Context block for LLM:\n")
    print(context)
