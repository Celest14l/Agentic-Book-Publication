# groq_client.py

import os
from groq import Groq

# === Configuration ===
GROQ_API_KEY = "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"  # Set your Groq API key here
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

    return response.choices[0].message.content


# === Review Function ===
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

    return response.choices[0].message.content
