# groq_client.py

import os
import re
from groq import Groq
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv("pass.env")  # Ensure pass.env contains GROQ_API_KEY

# === Set up the Groq client ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=GROQ_API_KEY)

# === Rewrite Function ===
def mistral_rewrite(text: str, style="modern and vivid"):
    prompt = f"""
You are a skilled creative writer. Your task is to rewrite the following book chapter in a {style} literary style.

Please:
- Enhance the storytelling with vivid, immersive language.
- Maintain the original meaning, plot, and character voices.
- Use modern sentence flow while keeping emotional and thematic depth.

Chapter to rewrite:
{text}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a masterful creative writer, skilled in vivid storytelling and narrative clarity."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.8,
        max_tokens=2048
    )

    return response.choices[0].message.content.strip()


# === Review Function with Preface Removal ===
def mistral_review(text: str):
    prompt = f"""
You are a professional literary editor. Please review and refine the following book chapter.

Your responsibilities:
- Improve clarity, sentence structure, and grammar.
- Maintain the author’s voice and emotional tone.
- Preserve the storyline and character integrity.
- Ensure smooth transitions and paragraph coherence.

Chapter to review:
{text}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a meticulous literary editor with a deep sense of tone, flow, and clarity."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.6,
        max_tokens=2048
    )

    raw = response.choices[0].message.content

    # === Strip prefaces like "Here's the revised version..." ===
    # Looks for common starting keywords or titles
    split_match = re.split(r"(CHAPTER\s+I.*|The Canoe Builder.*)", raw, flags=re.IGNORECASE | re.DOTALL)

    if len(split_match) >= 3:
        clean_text = split_match[1] + split_match[2]  # Include the chapter heading and content
    else:
        clean_text = raw  # Fallback if no clear match

    return clean_text.strip()
