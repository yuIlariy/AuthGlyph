import re
import requests
from config import AUTH_LOG_PATH, GEO_API

def get_last_login():
    with open(AUTH_LOG_PATH, "r") as f:
        lines = f.readlines()
    for line in reversed(lines):
        if "Accepted password" in line:
            match = re.search(r"Accepted password for (\w+) from ([\d\.]+)", line)
            if match:
                user = match.group(1)
                ip = match.group(2)
                time = " ".join(line.split()[0:3])
                return ip, user, time
    return "N/A", "N/A", "N/A"

def geo_lookup(ip):
    try:
        r = requests.get(GEO_API + ip).json()
        return f"{r.get('city')}, {r.get('country')} 🌐"
    except:
        return "Unknown 🌫️"
