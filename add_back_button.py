import os

# Dono folders jahan posts ho sakte hain
POSTS_DIRS = ["Posts", "Posts1"]

for POSTS_DIR in POSTS_DIRS:
    if not os.path.isdir(POSTS_DIR):
        continue

    print(f"📂 Processing folder: {POSTS_DIR}")

    for file in os.listdir(POSTS_DIR):
        if not file.endswith(".html"):
            continue

        path = os.path.join(POSTS_DIR, file)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Agar back button already hai to skip
        if 'class="back-btn"' in content:
            print(f"⏭️ Back button already exists: {POSTS_DIR}/{file}")
            continue

        # body tag ke baad back button inject karo
        if "<body" in content.lower():
            # exact <body> ya <body ...> dono case handle
            lower = content.lower()
            idx = lower.find("<body")
            end = lower.find(">", idx)

            if end != -1:
                new_content = (
                    content[:end + 1]
                    + '\n\n<a href="/" class="back-btn">← Back</a>\n'
                    + content[end + 1:]
                )

                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"✅ Back button added: {POSTS_DIR}/{file}")
            else:
                print(f"❌ <body> tag malformed: {POSTS_DIR}/{file}")
        else:
            print(f"❌ <body> tag not found: {POSTS_DIR}/{file}")

print("🎉 Done: Back button process complete (Posts + Posts1)")
