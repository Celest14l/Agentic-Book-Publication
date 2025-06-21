import chromadb
from sentence_transformers import SentenceTransformer
import os
import json

CHROMA_DIR = "chroma_index"
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="chapters")

def embed_version(slug):
    print("[📥] Indexing chapter versions into ChromaDB...")

    version_file = f"versions/{slug}.json"
    if not os.path.exists(version_file):
        print(f"[⚠️] No version log found for {slug}")
        return

    with open(version_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for version in data["versions"]:
        try:
            with open(version["file"], "r", encoding="utf-8") as f:
                content = f.read()
            embedding = model.encode(content).tolist()

            collection.add(
                documents=[content],
                embeddings=[embedding],
                ids=[f"{slug}_{version['step']}"]
            )
        except Exception as e:
            print(f"[❌] Failed indexing {version['step']}: {e}")

    print("[✅] Embedding completed.")

def search_version(slug, query_text):
    print(f"[🔍] Searching chapter '{slug}' for: {query_text}")
    embedding = model.encode(query_text).tolist()

    results = collection.query(query_embeddings=[embedding], n_results=3)
    for i, doc in enumerate(results["documents"][0]):
        print(f"\n[Match {i+1}]")
        print(doc[:500] + "...")
