import os
import re

POSTS_DIR = "Posts"

# Ekdam simple aur 100% working JavaScript combo ad code
AD_CODE = """
<script>
const myAdConfig = {
    link: "https://omg10.com/4/10814453",
    expiry: 5 * 60 * 1000 // 5 Minute Expiry
};

function launchPopUnder(keyName) {
    const lastClick = localStorage.getItem(keyName);
    const now = new Date().getTime();
    
    if (!lastClick || (now - lastClick) > myAdConfig.expiry) {
        const win = window.open(myAdConfig.link, '_blank');
        if (win) {
            win.blur();
            window.focus();
            localStorage.setItem(keyName, now);
            return true;
        }
    }
    return false;
}

// Pure page par kahi bhi click ho (Button ko chhodkar)
document.addEventListener('click', function(e) {
    if (e.target.closest('button')) return;
    launchPopUnder('last_screen_ad_click');
}, { once: false });

// Page ke saare buttons par dynamic listener (Bina kisi DOMContentLoaded ke jhamele ke)
setInterval(function() {
    const allButtons = document.querySelectorAll('button:not([ad-tracked])');
    allButtons.forEach(function(button) {
        button.setAttribute('ad-tracked', 'true');
        button.addEventListener('click', function(e) {
            launchPopUnder('last_button_ad_click');
        });
    });
}, 1000); // Har ek second me check karega agar koi naya button aaya ho toh
</script>
"""

def clean_and_inject_ads():
    processed_count = 0
    print(f"🧹 Clearing old scripts and injecting Fresh Combo Ads in: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    # 1. Purana modification time save karo tracking bachane ke liye
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # 2. JADD SE SAAF KARO: Jitne bhi <script>...</script> tags hain pehle unhe poora uda do
                    # Yeh regex pattern saare script tags ko dhoondh kar delete maar dega
                    cleaned_content = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', '', content)

                    # 3. Fresh inject karo </body> ke upar
                    if "</body>" in cleaned_content:
                        new_content = cleaned_content.replace("</body>", f"{AD_CODE}\n</body>")
                        
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        # 4. Wahi purana time wapas thop do
                        os.utime(path, original_times)
                        processed_count += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print(f"✨ Mission Accomplished! Total {processed_count} files cleaned & updated.")
    print("-" * 30)

if __name__ == "__main__":
    clean_and_inject_ads()
