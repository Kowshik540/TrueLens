import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState
from tools.image_scraper import scrape_image
from tools.exif_reader import read_exif

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective3(state: InvestigationState) -> InvestigationState:
    print("\nDetective 3 — Investigating images...")

    content    = state["content"]
    input_type = state["input_type"]

    if input_type != "url":
        return {**state, "image_url": "", "exif_data": {}, "image_flags": ["No URL provided"], "image_score": 10}

    image_path = scrape_image(content)

    if not image_path:
        return {**state, "image_url": "", "exif_data": {}, "image_flags": ["No image found on article"], "image_score": 8}

    exif_data = read_exif(image_path)
    flags = []
    score = 30

    # Deterministic penalties
    if not exif_data:
        score -= 8
        flags.append("No EXIF metadata found")

    software = exif_data.get("Software") if exif_data else None
    if software:
        score -= 10
        flags.append(f"Image edited with {software}")

    # Let LLM add extra flags (not score)
    prompt = f"""
You are an image forensics expert.
Look at the metadata below and list any suspicious flags only.

Metadata:
{json.dumps(exif_data)}

Reply ONLY JSON:
{{ "flags": ["flag one", "flag two"] }}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        result = json.loads(raw)
        flags.extend(result.get("flags", []))

    except:
        pass

    score = max(0, min(score, 30))

    return {
        **state,
        "image_url": content,
        "exif_data": exif_data,
        "image_flags": list(set(flags)),
        "image_score": score
    }
