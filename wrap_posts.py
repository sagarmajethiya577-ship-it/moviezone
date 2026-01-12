import os

POSTS_DIR = "Posts"

for file in os.listdir(POSTS_DIR):
    if not file.endswith(".html"):
        continue

    path = os.path.join(POSTS_DIR, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

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

<script src="/ads.js"></script>

</body>
</html>
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print("✅ Fixed:", file)

print("🎉 All posts wrapped successfully")

