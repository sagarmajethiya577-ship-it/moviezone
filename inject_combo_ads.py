import os
import time

POSTS_DIR = "Posts"

# Yaha humne AD_CODE ko full define kar diya hai
AD_CODE = """
<script>
const adConfig = {
    link: "https://omg10.com/4/10814453",
    expiry: 5 * 60 * 1000 // 5 Minute Expiry
};

function openPopUnder(keyName) {
    const lastClick = localStorage.getItem(keyName);
    const now = new Date().getTime();
    
    if (!lastClick || (now - lastClick) > adConfig.expiry) {
        const win = window.open(adConfig.link, '_blank');
        if (win) {
            win.blur();
            window.focus();
            localStorage.setItem(keyName, now);
            return true;
        }
    }
    return false;
}

// 1. Screen click ad
document.addEventListener('click', function(e) {
    if (e.target.closest('button')) return;
    openPopUnder('last_screen_ad_click');
}, { once: false });

// 2. Button click ad
document.addEventListener('DOMContentLoaded', function() {
    const allButtons = document.querySelectorAll('button');
    allButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const adOpened = openPopUnder('last_button_ad_click');
            if (adOpened) {
                e.preventDefault();
            }
        });
    });
});
</script>
"""

def inject_combo_ads():
    processed_count = 0
    print(f"🔍 Injecting Combo Ads in: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    # 1. Purana time (mtime) bachane ke liye save karo
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Agar naya setup pehle se hai, toh skip karo
                    if "last_button_ad_click" in content:
                        continue

                    # 2. SAFE CLEANUP: Agar koi purani script isme chal rahi hai, toh use pehle hatayenge
                    # Hum check karte hain ki kya purani script tag body ke pehle hai
                    # Agar aapki har file me script bilkul unique hai, toh sabse behtar hai ki hum naye code ko insert karein 
                    # Aur agar koi puraani script block hai jise aap target karna chahte ho, toh replace use kar sakte hain.
                    
                    # 3. Naya code hamesha </body> ke upar fresh thop do
                    if "</body>" in content:
                        new_content = content.replace("</body>", f"{AD_CODE}\n</body>")
                        
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        # 4. Wahi purana time wapas thop do
                        os.utime(path, original_times)
                        processed_count += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print(f"✅ Mission Complete! Combo ads deployed to {processed_count} files successfully!")
    print("-" * 30)

if __name__ == "__main__":
    inject_combo_ads()
