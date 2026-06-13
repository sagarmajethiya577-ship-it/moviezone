import os
import re
import time
import requests

# =========================================================
# CONFIGURATION
# =========================================================
POSTS_BASE_DIR = os.path.expanduser("~/moviezone/Posts")
IMGBB_API_KEY = "f32e74f0652698d7db9b3e4c06f8b87e"
TEMP_IMG_PATH = "/sdcard/temp_migration_img.jpg"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# =========================================================
# IMGBB UPLOAD FUNCTION
# =========================================================
def upload_to_imgbb(image_url):
    try:
        # 1. Cloudinary se image download karo
        img_data = requests.get(image_url, headers=HEADERS, timeout=20).content
        with open(TEMP_IMG_PATH, 'wb') as handler:
            handler.write(img_data)

        # 2. ImgBB par upload karo
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY}
        
        with open(TEMP_IMG_PATH, "rb") as file:
            files = {"image": file}
            response = requests.post(url, data=payload, files=files, timeout=30)
            json_data = response.json()

        if os.path.exists(TEMP_IMG_PATH):
            os.remove(TEMP_IMG_PATH)

        if json_data.get("success"):
            return json_data["data"]["url"]
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        if os.path.exists(TEMP_IMG_PATH):
            os.remove(TEMP_IMG_PATH)
    return None

# =========================================================
# MAIN MIGRATOR OPERATOR
# =========================================================
def start_migration():
    if not os.path.exists(POSTS_BASE_DIR):
        print(f"❌ Error: Path nahi mila -> {POSTS_BASE_DIR}")
        return

    try:
        upload_limit = int(input("Kitni images update karni hain? (Enter number, e.g. 10): ").strip())
    except ValueError:
        print("❌ Sahi number daalo bhai!")
        return

    uploaded_count = 0
    file_modified_count = 0

    print("\n🔍 Scanning folders p1 se p20...")
    print("-" * 60)

    # RegEx to find Cloudinary links in <img src="..."> tags
    cloudinary_regex = r'https://res\.cloudinary\.com/[^\s"\'>]+'

    for i in range(1, 21):
        if uploaded_count >= upload_limit:
            break

        folder_name = f"p{i}"
        folder_path = os.path.join(POSTS_BASE_DIR, folder_name)

        if not os.path.exists(folder_path):
            continue

        for file_name in os.listdir(folder_path):
            if not file_name.endswith(".html"):
                continue
            if uploaded_count >= upload_limit:
                break

            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find all unique Cloudinary links in this file
            cloudinary_links = list(set(re.findall(cloudinary_regex, content)))

            if cloudinary_links:
                # CRITICAL: Puraana time note karo (Access time & Modification time)
                file_stat = os.stat(file_path)
                old_atime = file_stat.st_atime
                old_mtime = file_stat.st_mtime

                file_updated = False
                new_content = content

                for c_link in cloudinary_links:
                    if uploaded_count >= upload_limit:
                        break

                    print(f"🔄 Found Cloudinary link in {folder_name}/{file_name}")
                    print(f"📥 Downloading: {c_link[:60]}...")
                    
                    # Upload to ImgBB
                    imgbb_link = upload_to_imgbb(c_link)
                    
                    if imgbb_link:
                        print(f"📤 Uploaded to ImgBB: {imgbb_link}")
                        # Replace content
                        new_content = new_content.replace(c_link, imgbb_link)
                        uploaded_count += 1
                        file_updated = True
                        # API safety ke liye loop me thoda break
                        time.sleep(1.5)
                    else:
                        print("❌ Upload fail hua, skipping this link.")

                if file_updated:
                    # Naya content file me save karo
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    # MAGIC LINE: File ka purana timestamp wapas apply kar do!
                    os.utime(file_path, (old_atime, old_mtime))
                    
                    print(f"✅ Successfully Updated (Time Saved): {folder_name}/{file_name}\n")
                    file_modified_count += 1

    print("-" * 60)
    print("✨ Migration Process Finished!")
    print(f"📊 Total Images Migrated to ImgBB: {uploaded_count}/{upload_limit}")
    print(f"📁 Total HTML Files Safely Patched: {file_modified_count}")

if __name__ == "__main__":
    start_migration()
