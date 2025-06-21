# 📚 AI-Driven Book Pipeline

**Automated Book Publication Workflow**  
Built using Playwright, LLMs (Groq Mistral + LLaMA 3), ChromaDB, and Python.  
This tool scrapes book chapters from web sources, rewrites and reviews them using AI, allows human editing, and manages versioning with intelligent search.  

> ⚙️ Built for automation, creativity, and iterative refinement in literary content creation.

---

## 🚀 Demo

🎬 **Watch the demo** → [Insert Demo Video Link Here]

---

## 📂 Features

- 🔍 **Web Scraping** – Extracts book chapter content from specified URLs using `playwright`.
- ✍️ **LLM Rewrite (Groq)** – Uses Mistral via Groq API to rewrite chapters in a modern literary style.
- 🧠 **AI Review** – Refines the rewritten version using LLaMA 3 for clarity, grammar, and tone.
- 🧑‍💻 **Human-in-the-Loop Editing** – Supports manual editing and version tagging.
- 🗂 **Version Logging** – Tracks all iterations (original, mistral, reviewed, human edits).
- 🧠 **ChromaDB Search** – Embeds each version and allows intelligent vector search (e.g., by topic or phrase).
- 🧪 **CLI Interface** – Streamlined terminal-based workflow for end-to-end processing.

---

## 🧱 Architecture

```plaintext
               ┌─────────────────────────────┐
               │     Chapter Scraper        │
               │  (Playwright via URL)       │
               └────────────┬────────────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ AI Rewrite (Groq)  │
                 │  → Mistral Style   │
                 └────────┬───────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ AI Review (Groq)    │
                │  → LLaMA 3 Editing  │
                └─────────┬───────────┘
                          │
          ┌───────────────▼───────────────┐
          │ Human-in-the-Loop Editing     │
          │  → Save as versioned files    │
          └───────────────┬───────────────┘
                          ▼
             ┌────────────────────────┐
             │   ChromaDB Embedding   │
             │   & Semantic Search    │
             └────────────────────────┘

