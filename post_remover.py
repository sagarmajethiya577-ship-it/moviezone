import os

def remove_loop():
    print("🗑️ --- Movies Zone Non-Stop File Remover ---")
    print("💡 Tip: Script se bahar aane ke liye 'exit' likhein.\n")
    
    while True:
        # Loop chalta rahega jab tak user exit nahi likhta
        url = input("🔗 Apni post ki URL link paste karo: ").strip()
        
        # Agar user exit likhe toh loop tod do
        if url.lower() == 'exit':
            print("\n👋 Bye bye! Loop band ho gaya.")
            break
            
        if not url:
            print("❌ Kuch toh paste karo bhai!\n")
            continue

        # Target links saaf karne ke liye
        targets = [
            "https://movieszone.shop/",
            "http://movieszone.shop/",
            "movieszone.shop/"
        ]
        
        relative_path = url
        for target in targets:
            relative_path = relative_path.replace(target, "")
        
        if relative_path.startswith("/"):
            relative_path = relative_path[1:]

        # File check aur deletion logic
        if os.path.exists(relative_path) and os.path.isfile(relative_path):
            try:
                os.remove(relative_path)
                print(f"✅ Mission Success! File delete ho gayi: {relative_path}\n")
            except Exception as e:
                print(f"❌ Error: Vajah -> {e}\n")
        else:
            print(f"❌ Error: File mili nahi! Path check karo: '{relative_path}'\n")

if __name__ == "__main__":
    remove_loop()
