import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient

# ==============================
# 🔐 YOUR TELEGRAM DETAILS
# ==============================
api_id = 34330516
api_hash = "9693b684498bf93a949bf50ba0573fc3"
phone_number = "+919512339243"
# ==============================

SOURCE_DIR = "/sdcard/vegamovies_demo_post"
BASE_URL = "https://movieszone.shop/Posts/p20/"

TARGETS = [
     "https://t.me/moviesrequest044",
     "https://t.me/Moviezonechathouse",
]

DELAY = 30  # Wait time
POSTED_FILE = "posted_files.txt"

client = TelegramClient("session", api_id, api_hash)


async def main():
    await client.start(phone_number)

    files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith(".html")])

    # Load already posted files
    posted = set()
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            posted = set(line.strip() for line in f.readlines())

    print(f"Already posted: {len(posted)} files")

    for file_name in files:
        if file_name in posted:
            continue  # Skip already posted

        file_path = os.path.join(SOURCE_DIR, file_name)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        img_tag = soup.find("img")
        h1_tag = soup.find("h1")

        if not img_tag or not h1_tag:
            continue

        img_url = img_tag.get("src")
        title = h1_tag.text.strip()

        # Download image with verification and correct format
        try:
            response = requests.get(img_url, timeout=10)
            if response.status_code != 200:
                print(f"❌ Broken Image Link (Skipping): {file_name}")
                continue
            
            # Check actual image format (webp, png, or jpg)
            content_type = response.headers.get('content-type', '')
            if 'webp' in content_type:
                ext = '.webp'
            elif 'png' in content_type:
                ext = '.png'
            else:
                ext = '.jpg'
                
            img_data = response.content
            img_file = f"temp{ext}" # Save with correct extension

        except Exception as e:
            print(f"❌ Image download failed for {file_name}: {e}")
            continue

        with open(img_file, "wb") as img:
            img.write(img_data)

        final_link = BASE_URL + file_name
        caption = f"{title}\n\n{final_link}"

        print(f"⏳ Sending: {title}")

        try:
            # Send to Saved Messages as normal PHOTO
            await client.send_file("me", img_file, caption=caption)

            # Send to all groups as normal PHOTO
            for target in TARGETS:
                await client.send_file(target, img_file, caption=caption)

            print(f"✅ Posted Successfully: {title}")

            # Save posted filename ONLY if successful
            with open(POSTED_FILE, "a") as f:
                f.write(file_name + "\n")

        except Exception as e:
            # Agar image me sach me koi problem hai, to document nahi bhejega, bas skip kar dega
            print(f"⚠️ Ye image Telegram support nahi kar raha, skipping: {title} | Error: {e}")

        # Cleanup
        if os.path.exists(img_file):
            os.remove(img_file)

        print(f"Waiting {DELAY} seconds...\n")
        await asyncio.sleep(DELAY)

    print("✅ All new posts completed!")

with client:
    client.loop.run_until_complete(main())
