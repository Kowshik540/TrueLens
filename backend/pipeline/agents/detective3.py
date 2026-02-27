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
    """
    Detective 3 — Image Forensics
    Scrapes images from article URL, reads hidden metadata,
    and flags any signs of manipulation or misuse.
    """
    print("\nDetective 3 — Investigating images...")

    content    = state["content"]
    input_type = state["input_type"]

    # Only works if user gave a URL
    if input_type != "url":
        print("Detective 3 — No URL provided, skipping image forensics")
        return {
            **state,
            "image_url":   "",
            "exif_data":   {},
            "image_flags": ["No URL provided — image forensics skipped"],
            "image_score": 15
        }

    # Step 1 — Scrape image from article URL
    image_path = scrape_image(content)

    if not image_path:
        print("Detective 3 — No image found on page")
        return {
            **state,
            "image_url":   "",
            "exif_data":   {},
            "image_flags": ["No image found in article"],
            "image_score": 15
        }

    # Step 2 — Read EXIF metadata from image
    exif_data = read_exif(image_path)

    # Step 3 — Ask Groq to interpret the metadata
    exif_text = json.dumps(exif_data) if exif_data else "No EXIF metadata found in this image"

    prompt = f"""
You are an image forensics expert analyzing a news article image.

The article URL is: {content}
The image metadata (EXIF data) extracted from the image is:
{exif_text}

Based on this information, identify any suspicious findings such as:
- Image date does not match the article date
- Image was edited with software like Photoshop
- GPS location does not match the claimed location in article
- No metadata at all (scrubbed — common in manipulated images)
- Any other red flags

Reply with ONLY a valid JSON object in this exact format:
{{
  "flags": ["flag one", "flag two"],
  "image_score": 0
}}

For image_score out of 30:
- 25-30 if image looks completely legitimate
- 15-24 if minor concerns or no metadata
- 5-14 if suspicious signs found
- 0-4 if clear manipulation detected
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result      = json.loads(raw)
        flags       = result.get("flags", [])
        image_score = int(result.get("image_score", 15))

        print(f"Detective 3 — Image flags: {flags}")
        print(f"Detective 3 — Image score: {image_score}/30")

        return {
            **state,
            "image_url":   content,
            "exif_data":   exif_data,
            "image_flags": flags,
            "image_score": image_score
        }

    except Exception as e:
        print(f"Detective 3 error: {e}")
        return {
            **state,
            "image_url":   "",
            "exif_data":   exif_data,
            "image_flags": ["Could not analyze image"],
            "image_score": 15
        }