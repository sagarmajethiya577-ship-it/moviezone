import os
from bs4 import BeautifulSoup

POSTS_DIR = "Posts"
OUTPUT_FILE = "index.html"

cards_html = ""

files = sorted(os.listdir(POSTS_DIR), reverse=True)

for file in files:
    if not file.endswith(".html"):
        continue

    path = os.path.join(POSTS_DIR, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    img = soup.find("img")
    img_src = img["src"] if img else ""

    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else file.replace(".html", "")

    cards_html += f"""
    <a class="post-card" href="Posts/{file}">
      <img src="{img_src}" alt="{title}">
      <h2>{title}</h2>
    </a>
    """

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta name="monetag" content="3022723db0ecc4b869eb8ce9984399b0">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Movie Zone 🍿</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<header class="site-header">
  <a href="/" class="site-title">Movie Zone 🍿</a>
  <p class="tagline">Latest Movies & Web Series</p>
</header>

<div class="search-box">
  <input type="text" id="searchInput" placeholder="Search movies...">
</div>

<main class="home-container" id="postList">
{cards_html}
</main>

<footer class="site-footer">
  © 2026 Movie Zone 🍿
</footer>

<script>
let timer;
const input = document.getElementById("searchInput");

input.addEventListener("keyup", function () {{
  clearTimeout(timer);
  timer = setTimeout(function () {{
    const value = input.value.toLowerCase();
    document.querySelectorAll(".post-card").forEach(function(card) {{
      card.style.display = card.innerText.toLowerCase().includes(value)
        ? "block"
        : "none";
    }});
  }}, 300);
});
</script>

</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html generated successfully")
