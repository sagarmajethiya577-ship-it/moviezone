import os

POSTS_DIR = "Posts"

for file in os.listdir(POSTS_DIR):
    if not file.endswith(".html"):
        continue

    path = os.path.join(POSTS_DIR, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Agar back button already hai to skip
    if 'class="back-btn"' in content:
        print("⏭️ Back button already exists:", file)
        continue

    # body ke andar back button inject karo
    if "<body" in content.lower():
        new_content = content.replace(
            "<body>",
            '<body>\n\n<a href="/" class="back-btn">← Back</a>\n',
            1
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("✅ Back button added:", file)
    else:
        print("❌ <body> tag not found:", file)

print("🎉 Done: Back button process complete")
