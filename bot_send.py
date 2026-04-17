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
BASE_URL = "https://moviezone-22y.pages.dev/Posts/p20/"

TARGETS = [
     "https://t.me/moviesrequest044",
     "https://t.me/Moviezonechathouse",
]

DELAY = 30  # 10 minutes
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

        # Download image
        try:
            img_data = requests.get(img_url, timeout=10).content
        except:
            print(f"Image download failed: {file_name}")
            continue

        img_file = "temp.jpg"
        with open(img_file, "wb") as img:
            img.write(img_data)

        final_link = BASE_URL + file_name
        caption = f"{title}\n\n{final_link}"

        # Send to Saved Messages
        await client.send_file("me", img_file, caption=caption)

        # Send to all groups
        for target in TARGETS:
            await client.send_file(target, img_file, caption=caption)

        print(f"Posted: {title}")

        os.remove(img_file)

        # Save posted filename
        with open(POSTED_FILE, "a") as f:
            f.write(file_name + "\n")

        print("Waiting 10 minutes...\n")
        await asyncio.sleep(DELAY)

    print("✅ All new posts completed!")


with client:
    client.loop.run_until_complete(main())
