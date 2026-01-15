import os
from bs4 import BeautifulSoup

POSTS_DIR = "Posts"
OUTPUT_FILE = "index.html"

cards_html = ""

# 🔥 Latest modified files first (new post = top)
files = sorted(
    os.listdir(POSTS_DIR),
    key=lambda x: os.path.getmtime(os.path.join(POSTS_DIR, x)),
    reverse=True
)

for file in files:
    if not file.endswith(".html"):
        continue

    path = os.path.join(POSTS_DIR, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    img = soup.find("img")
    img_src = img["src"] if img else ""

    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else file.replace(".html", "").replace("-", " ").title()

    cards_html += f"""
    <a class="post-card" href="Posts/{file}">
      <img src="{img_src}" alt="{title}">
      <h2>{title}</h2>
    </a>
    """

html = f"""<!DOCTYPE html>
<html lang="en">
<head>

<!-- ✅ Monetag verification -->
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
  © 2026 Movie Zone 🍿 | All Rights Reserved
</footer>

<!-- 🔥 FAST SEARCH (NO LAG even with 5000+ posts) -->
<script>
const input = document.getElementById("searchInput");
const cards = document.querySelectorAll(".post-card");

const cache = Array.from(cards).map(card => ({
  el: card,
  text: card.textContent.toLowerCase()
}));

let timer;
input.addEventListener("input", () => {{
  clearTimeout(timer);
  timer = setTimeout(() => {{
    const val = input.value.toLowerCase();
    cache.forEach(item => {{
      item.el.style.display = item.text.includes(val) ? "" : "none";
    }});
  }}, 200);
}});
</script>

<!-- ✅ Monetag Pop / Push Ad (body end = safe + fast) -->
<script>
(function(s){{
  s.dataset.zone='10453660';
  s.src='https://al5sm.com/tag.min.js';
}})(document.body.appendChild(document.createElement('script')));
</script>

</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html generated successfully (fast search + latest on top)")
