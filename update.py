import os
import re

POSTS_DIR = "Posts"

OLD_LINK = "https://moviezone-22y.pages.dev/"
NEW_LINK = "https://omg10.com/4/10814453"

def replace_ad_link():
    updated = 0
    skipped = 0

    print(f"🔍 Scanning: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)

                try:
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # ✅ Only replace inside adConfig link
                    pattern = r'(link:\s*")https://moviezone-22y\.pages\.dev/(")'
                    new_content = re.sub(pattern, rf'\1{NEW_LINK}\2', content)

                    if content != new_content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        os.utime(path, original_times)  # 🛡️ keep old time
                        updated += 1
                    else:
                        skipped += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print("✅ Done!")
    print(f"🔄 Updated files: {updated}")
    print(f"⏭️ Skipped: {skipped}")
    print("-" * 30)

if __name__ == "__main__":
    replace_ad_link()
