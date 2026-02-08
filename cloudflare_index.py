import os
from bs4 import BeautifulSoup
import json

# Folders jahan se posts read karni hain
POSTS_DIRS = ["Posts", "Posts1"]
OUTPUT_FILE = "index.html"

posts_data = []

# 🔹 Collect all html files from both folders with mtime
files = []

for d in POSTS_DIRS:
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if f.endswith(".html"):
            files.append((d, f))

# 🔹 Sort by modified time (latest first)
files.sort(
    key=lambda x: os.path.getmtime(os.path.join(x[0], x[1])),
    reverse=True
)

# 🔹 Parse each HTML file
for folder, file in files:
    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    img = soup.find("img")
    img_src = img["src"] if img else ""

    h1 = soup.find("h1")
    title = (
        h1.get_text(strip=True)
        if h1
        else file.replace(".html", "").replace("-", " ").title()
    )

    posts_data.append({
        "title": title,
        "img": img_src,
        "url": f"{folder}/{file}",   # 🔥 Posts ya Posts1 dono support
        "search": title.lower()
    })

# 🔹 Generate index.html
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
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

<main class="home-container" id="postList"></main>

<footer class="site-footer">
  © 2026 Movie Zone 🍿
</footer>

<script>
const posts = {json.dumps(posts_data)};
const container = document.getElementById("postList");
const input = document.getElementById("searchInput");

function render(list) {{
  container.innerHTML = list.map(p => `
    <a class="post-card" href="${{p.url}}">
      <img src="${{p.img}}" alt="${{p.title}}">
      <h2>${{p.title}}</h2>
    </a>
  `).join("");
}}

render(posts);

let timer;
input.addEventListener("input", () => {{
  clearTimeout(timer);
  timer = setTimeout(() => {{
    const val = input.value.toLowerCase();
    if (!val) {{
      render(posts);
      return;
    }}
    const filtered = posts.filter(p => p.search.includes(val));
    render(filtered);
  }}, 150);
}});
</script>

</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Ultra-fast index generated (Posts + Posts1, no DOM lag)")
