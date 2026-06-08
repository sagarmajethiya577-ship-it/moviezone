import os

# =========================================================
# CONFIGURATION
# =========================================================
# Jahan aapki kharab files filter hoke aayi hain
ERROR_DIR = "/sdcard/error_posts"

# Python ko hum bata rahe hain ki p1...p20 folders Posts ke andar milenge
POSTS_BASE_DIR = os.path.expanduser("~/moviezone/Posts")

if not os.path.exists(ERROR_DIR):
    print(f"❌ Error: '{ERROR_DIR}' folder nahi mila jisme kharab posts hain.")
    exit()

if not os.path.exists(POSTS_BASE_DIR):
    print(f"❌ Error: '{POSTS_BASE_DIR}' folder nahi mila. Path sahi karo!")
    exit()

wrong_files = [f for f in os.listdir(ERROR_DIR) if f.endswith(".html")]

if not wrong_files:
    print("✨ 'error_posts' folder khali hai! Koi file delete karne ki zaroorat nahi hai.")
    exit()

print(f"🚀 Total {len(wrong_files)} kharab files ko p1 se p20 folders me dhoond kar delete kiya ja raha hai...\n")

deleted_count = 0

# p1 se p20 folders me check karega
for i in range(1, 21):
    folder_name = f"p{i}"
    target_folder_path = os.path.join(POSTS_BASE_DIR, folder_name)
    
    if os.path.exists(target_folder_path):
        for file_name in wrong_files:
            file_to_delete = os.path.join(target_folder_path, file_name)
            
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)
                print(f"🗑️ Deleted: Posts/{folder_name}/{file_name}")
                deleted_count += 1

print("-" * 50)
print(f"✅ Clean-up Done!")
print(f"📊 Total Files Deleted from Git folders: {deleted_count}")
print("\n👉 Ab aap isi folder (~/moviezone) me 'git status' karke dekh sakte hain ki files delete hui ya nahi.")
