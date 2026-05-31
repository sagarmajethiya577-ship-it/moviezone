import os
import time

POSTS_DIR = "Posts"

# Naya 5-minute vaala ad code
NEW_AD_CODE = """
<script>
const adConfig = {
    link: "https://omg10.com/4/10814453",
    expiry: 5 * 60 * 1000
};

function openPopUnder() {
    const lastClick = localStorage.getItem('last_ad_click');
    const now = new Date().getTime();
    if (!lastClick || (now - lastClick) > adConfig.expiry) {
        const win = window.open(adConfig.link, '_blank');
        if (win) {
            win.blur();
            window.focus();
            localStorage.setItem('last_ad_click', now);
        }
    }
}

document.addEventListener('click', function() {
    openPopUnder();
}, { once: false });
</script>
"""

def update_ads_recursive():
    updated_count = 0
    print(f"🔍 Scanning and updating ads in: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    # 1. File ka asli purana timestamp (mtime) save karo
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # 2. Check karo ki kya purani expiry (24 ghante vaali) script me maujood hai
                    if "expiry: 24 * 60 * 60 * 1000" in content:
                        # Purani script ko naye code se badal do (Aap string match ke hisab se ise customize bhi kar sakte hain)
                        # Agar poori script replace karni hai toh hum us section ko target karenge
                        
                        # Ek safe tarika: Pehle purani ad block ko remove karne ke liye target karein
                        # Agar aapne body ke thik pehle lagaya tha, toh hum use replace kar sakte hain.
                        pass

                    # Sabse behtar aur safe tarika agar script pehle se hai: 
                    # Hum sirf expiry vaali line ko target karke badal dete hain taaki poora code chhedna na pade:
                    if "expiry: 24 * 60 * 60 * 1000" in content:
                        new_content = content.replace("expiry: 24 * 60 * 60 * 1000", "expiry: 5 * 60 * 1000")
                        
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        # 3. Wahi purana timestamp wapas thop do (Isse file ka time nahi badlega)
                        os.utime(path, original_times)
                        updated_count += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print(f"✅ Mission Complete! Updated {updated_count} files bina time change kiye.")
    print("-" * 30)

if __name__ == "__main__":
    update_ads_recursive()
