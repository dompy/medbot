import os

CHUNK_PATH = "../data/chunks/"

def find_exact_match(query):
    results = []

    for folder in os.listdir(CHUNK_PATH):
        folder_path = os.path.join(CHUNK_PATH, folder)
        if not os.path.isdir(folder_path):
            continue

        for file in os.listdir(folder_path):
            if not file.endswith(".txt"):
                continue

            file_path = os.path.join(folder_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if query.strip() in content:
                    results.append((folder, file, content))

    return results

if __name__ == "__main__":
    print("Paste an exact phrase to search for in your document chunks:")
    query = input("> ")

    matches = find_exact_match(query)

    if matches:
        print(f"\n✅ Found {len(matches)} exact match(es):\n")
        for folder, file, content in matches:
            print(f"📘 From {folder} — {file}:\n{content[:500]}...\n")
    else:
        print("\n❌ No exact matches found.")
