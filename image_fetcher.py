"""
Ubuntu-Inspired Image Fetcher - Advanced Version
Author: [Your Name]
Date: [Date]

Description:
Downloads one or more images from provided URLs, saving them into a 'Fetched_Images' directory.
Implements Ubuntu principles:
- Community: Connects to the wider web to fetch shared resources.
- Respect: Handles errors gracefully without crashing.
- Sharing: Organizes fetched images for later sharing.
- Practicality: Creates a useful, reusable tool.

Challenge Features:
- Handles multiple URLs at once.
- Checks HTTP headers to ensure safe image downloads.
- Prevents duplicate downloads.
- Implements precautions for unknown sources.
"""

import os
import requests
from urllib.parse import urlparse
import uuid

def is_image_content(response):
    """Check if the Content-Type header indicates an image."""
    content_type = response.headers.get("Content-Type", "").lower()
    return content_type.startswith("image/")

def fetch_images(urls):
    folder_name = "Fetched_Images"
    os.makedirs(folder_name, exist_ok=True)

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Fetch with timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Check if content is an image
            if not is_image_content(response):
                print(f"✗ Skipped (Not an image): {url}")
                continue

            # Extract filename or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = f"image_{uuid.uuid4().hex}.jpg"

            filepath = os.path.join(folder_name, filename)

            # Prevent duplicate downloads
            if os.path.exists(filepath):
                print(f"⚠ Skipped (Duplicate): {filename}")
                continue

            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error for {url}: {e}")
        except Exception as e:
            print(f"✗ An error occurred for {url}: {e}")

    print("\nConnection strengthened. Community enriched.")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    urls_input = input("Please enter one or more image URLs (comma-separated): ")
    urls = urls_input.split(",")
    fetch_images(urls)

if __name__ == "__main__":
    main()
