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

        # Agar already full HTML hai to skip
        if "<html" in content.lower():
            continue

        title = file.replace(".html", "").replace("-", " ").title()

        new_html = f"""<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/style.css">
</head>

<body>

<div class="post-container">

{content}

</div>

</body>
</html>
"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)

        print(f"✅ Wrapped: {POSTS_DIR}/{file}")

print("🎉 All posts wrapped successfully (Posts + Posts1)")
