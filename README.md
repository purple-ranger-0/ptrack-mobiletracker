# 📱 Ptrack-MobileTracker

      ██████╗ ████████╗██████╗  █████╗  ██████╗██╗  ██╗
      ██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
      ██████╔╝   ██║   ██████╔╝███████║██║     █████╔╝ 
      ██╔═══╝    ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ 
      ██║        ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
      ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
  
  

*A phone number intelligence and educational tracking tool by **Purple Ranger**.*

🔗 Visit our site: [https://purplehub.serveo.net](https://purplehub.serveo.net)  
💬 Contact on WhatsApp: [https://wa.link/nhd7st](https://wa.link/nhd7st)
📬 mail :purplehub@aol.com

---

## ⚠️ Disclaimer

> **This tool is strictly for educational and ethical use only.**

- ✅ Use only with **explicit consent** from the person being tracked.  
- ❌ Any misuse for illegal or malicious purposes is **strictly prohibited**.  
- ⚖️ The developer assumes **no responsibility** for misuse or legal consequences.  

---

## 🌟 Features

- 🔍 Extract **carrier**, **region**, and **timezone** from phone numbers using `phonenumbers`.
- 📡 Generate a **phishing page** (for demonstration purposes) to approximate target **location**.
- 🌐 Runs a lightweight **Flask**-based local web server.
- 📊 **Logs visitor data** including:
  - IP address  
  - Device information  
  - GPS coordinates (if permission granted)  
- 🌍 If GPS access is denied, it falls back to **IP-based geolocation**.
- 🧩 Compatible with **Ngrok**, **Cloudflare Tunnel**, or any custom domain setup for WAN access.

---

## 📥 Installation

### 🔧 Requirements

- Python 3.8+  
- `pip` (Python package manager)  
- `git`

---

### 📱 Installation on **Termux (Android)**

1. Install **Termux** from [F-Droid](https://f-droid.org/).  
2. Run the following commands:

```bash
pkg update && pkg upgrade -y
pkg install python git curl -y
pkg install cloudflared
git clone https://github.com/purple-ranger-0/ptrack-mobiletracker.git
cd ptrack-mobiletracker
pip install -r requirements.txt
```
### installation on linux

#### cloudflare installation
`sudo apt install cloudflared`
        (or)
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```
```bash
sudo apt update && sudo apt install python3 python3-pip git -y
git clone https://github.com/purple-ranger-0/ptrack-mobiletracker.git
cd ptrack-mobiletracker
pip3 install -r requirements.txt
```
### usage
```bash
python3 ptrack.py +9197*******8
```
To use this link wan level use tunel you prefered

Example 
```bash
ngrok http 5000
```

Thank you for visiting us
