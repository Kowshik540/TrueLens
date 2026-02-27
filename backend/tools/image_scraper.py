import requests
from bs4 import BeautifulSoup
import os

def scrape_image(url: str) -> str:
    """
    Takes an article URL.
    Finds the first meaningful image on the page.
    Downloads it to a temp file.
    Returns the local file path of the downloaded image.
    Returns empty string if no image found.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Get the webpage HTML
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all image tags
        images = soup.find_all("img")

        image_url = ""

        # Look for first image that is large enough to be meaningful
        for img in images:
            src = img.get("src", "")

            # Skip tiny icons, logos, tracking pixels
            if not src:
                continue
            if any(skip in src.lower() for skip in ["logo", "icon", "pixel", "tracking", "avatar", "badge"]):
                continue
            if src.startswith("data:"):
                continue

            # Make relative URLs absolute
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                base = "/".join(url.split("/")[:3])
                src = base + src

            image_url = src
            break

        if not image_url:
            print("No image found on page")
            return ""

        # Download the image
        img_response = requests.get(image_url, headers=headers, timeout=10)

        # Save to temp file
        temp_path = "temp_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(img_response.content)

        print(f"Image downloaded from: {image_url}")
        return temp_path

    except Exception as e:
        print(f"Image scraping error: {e}")
        return ""