import os
import json

CONFIG_FILE = "config.json"

def is_configured():
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE) as f:
        try:
            config = json.load(f)
            return "rtsp_url" in config and "uid" in config
        except:
            return False

def main():
    if is_configured():
        print("✅ Configuration found. Starting fire detection...")
        os.system("python3 fire_detection.py")
    else:
        print("🛠️ No config found. Starting setup server...")
        os.system("python3 config_server.py")

if __name__ == "__main__":
    main()
