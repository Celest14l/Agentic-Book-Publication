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
📦 Installation
🔧 Requirements
Python 3.9+

playwright installed with Chromium browser

Groq API key in .env

1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/yourusername/book-pipeline.git
cd book-pipeline
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
playwright install
3. Setup Environment Variables
Create a file named pass.env and add:

ini
Copy
Edit
GROQ_API_KEY=your-groq-api-key
4. Run the Pipeline
bash
Copy
Edit
python main.py
🗂 Project Structure
bash
Copy
Edit
book-pipeline/
├── book.py               # Main pipeline logic
├── groq_client.py        # Groq-based LLM rewrite & review
├── chromadb_utils.py     # Vector DB logic (embed/search)
├── main.py               # Entrypoint to run full pipeline
├── versions/             # Stores version logs
├── chapters/             # All generated chapter files
├── human_edits/          # Manually edited versions
├── screenshots/          # Screenshot of original webpage
├── pass.env              # Environment variables
├── requirements.txt      # Python dependencies
└── README.md             # You're here

💡 Customization
🌐 Change URL in book.py to process different chapters.

📝 Tweak the rewrite/review prompts in groq_client.py for style control.

🔍 Modify search queries (search_version()) for different retrieval strategies.

📁 Set skip=True in human_in_the_loop(slug, skip=True) to bypass manual steps.

🔐 API Usage
Make sure your Groq API key is active and has access to llama3-8b-8192.

If needed, rate-limit or chunk large texts before sending to LLM.

📈 Future Improvements
 Optional PDF Export (currently removed)

 Frontend UI (Gradio or Streamlit)

 Automatic style classification

 Agentic orchestration using LangGraph or CrewAI

🧑 Author
Priyanshu Singh
AI/ML Enthusiast | Builder of intelligent pipelines
📧 priyaanshu128912@gmail.com
🔗 https://www.linkedin.com/in/priyanshubeingcelestial/

📄 License
MIT License – use, fork, improve, share freely.
Attribution appreciated. 🙏
