# book.py

import os
import time
import json
import shutil
import urllib.request
from playwright.sync_api import sync_playwright
from groq_client import mistral_rewrite, mistral_review
from chromadb_utils import embed_version, search_version

# Global URL for the pipeline to process
URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

# === CHAPTER SCRAPING ===
def scrape_chapter(url, slug):
    TEXT_PATH = f"chapters/{slug}.txt"
    print("[\U0001f310] Scraping chapter from:", url)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("chapters", exist_ok=True)
    os.makedirs("versions", exist_ok=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url.strip())
            page.screenshot(path=f"screenshots/{slug}.png")
            content_divs = page.locator(".mw-parser-output")
            if content_divs.count() > 0:
                content = content_divs.nth(0).inner_text()
            else:
                raise ValueError("❌ Could not locate content block")

            with open(TEXT_PATH, "w", encoding="utf-8") as f:
                f.write(content)

            print("[✅] Chapter text saved to", TEXT_PATH)
            log_version(slug, "original", TEXT_PATH)
            browser.close()

    except Exception as e:
        print(f"[❌] Error scraping chapter: {e}")

# === AI-ASSISTED REWRITE (MISTRAL) ===
def rewrite_with_mistral(slug):
    try:
        with open(f"chapters/{slug}.txt", "r", encoding="utf-8") as f:
            chapter_text = f.read()
        print("[⚡] Sending text to Mistral for rewrite...")
        mistral_text = mistral_rewrite(chapter_text)
        # Remove leading helper lines (like "Here is the rewritten chapter")
        mistral_text = remove_llm_headers(mistral_text)
        path = f"chapters/{slug}_mistral.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(mistral_text)
        print("[✅] Mistral rewrite saved to", path)
        log_version(slug, "mistral_v1", path)
    except Exception as e:
        print(f"[❌] Error during Mistral rewrite: {e}")

# === AI REVIEW OF REWRITE ===
def review_with_llm(slug):
    try:
        with open(f"chapters/{slug}_mistral.txt", "r", encoding="utf-8") as f:
            mistral_text = f.read()
        print("[\U0001f9e0] Sending Mistral version for review...")
        reviewed_text = mistral_review(mistral_text)
        reviewed_text = remove_llm_headers(reviewed_text)
        path = f"chapters/{slug}_reviewed.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(reviewed_text)
        print("[✅] Review saved to", path)
        log_version(slug, "reviewed_v1", path)
    except Exception as e:
        print(f"[❌] Review failed: {e}")

# === CLEAN LLM HEADER ===
def remove_llm_headers(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("chapter"):
            return "\n".join(lines[i:]).strip()
    return text.strip()

# === HUMAN-IN-THE-LOOP EDITING ===
def human_in_the_loop(slug, skip=False):
    try:
        print("[✍️] Human-in-the-loop mode activated...")
        os.makedirs("human_edits", exist_ok=True)
        base_src = f"chapters/{slug}_reviewed.txt"
        version_count = 1
        version_log = f"versions/{slug}.json"
        if os.path.exists(version_log):
            with open(version_log, "r", encoding="utf-8") as f:
                data = json.load(f)
                version_count = sum(1 for v in data["versions"] if v["step"].startswith("human_v")) + 1
        version_tag = f"human_v{version_count}"
        dst = f"human_edits/{slug}_{version_tag}.txt"
        shutil.copyfile(base_src, dst)
        print(f"[\U0001f4c2] {version_tag} created → Edit manually: {dst}")

        if skip:
            print("[⏸️] Human edit skipped. You can continue later.")
            return

        decision = input("✅ Accept this edit as final? (y/n/pass): ").strip().lower()
        if decision == "y":
            log_version(slug, version_tag, dst)
            print(f"[📘] Accepted and logged version: {version_tag}")
        elif decision == "pass":
            print("[⏭️] Skipped. You can edit later.")
        else:
            print("[❌] Rejected. Version not logged.")

    except Exception as e:
        print(f"[❌] Human editing failed: {e}")

# === FINAL VERSION SELECTION ===
def select_final_version(slug):
    version_log = f"versions/{slug}.json"
    try:
        with open(version_log, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("\n📘 Available Versions:")
        for i, version in enumerate(data["versions"]):
            print(f"{i+1}. {version['step']} → {version['file']}")

        idx = int(input("✅ Select final version number: ")) - 1
        final = data["versions"][idx]
        data["final_version"] = {
            "step": final["step"],
            "file": final["file"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(version_log, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"[🎯] Final version set: {final['step']}")

    except Exception as e:
        print(f"[❌] Final selection failed: {e}")

# === VERSION LOGGER ===
def log_version(slug, step, file_path):
    version_log = f"versions/{slug}.json"
    data = {"versions": []}
    if os.path.exists(version_log):
        with open(version_log, "r", encoding="utf-8") as f:
            data = json.load(f)
    data["versions"].append({
        "step": step,
        "file": file_path,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(version_log, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[📘] Logged version: {step} → {file_path}")

# === PIPELINE EXECUTION ===
def run_full_pipeline():
    slug = URL.strip().split("/")[-1].lower().replace("_", "-")
    scrape_chapter(URL, slug)
    rewrite_with_mistral(slug)
    review_with_llm(slug)
    human_in_the_loop(slug)
    embed_version(slug)
    select_final_version(slug)
    search_version(slug, "canoe builder")
