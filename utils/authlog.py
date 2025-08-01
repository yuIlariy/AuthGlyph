import re
import subprocess
import requests
from config import GEO_API, AUTH_LOG_PATH

# Supported login patterns
LOGIN_PATTERNS = [
    r"Accepted password for (\w+) from ([\d\.]+)",
    r"Accepted publickey for (\w+) from ([\d\.]+)",
    r"Accepted keyboard-interactive/pam for (\w+) from ([\d\.]+)"
]

def read_auth_log():
    try:
        with open(AUTH_LOG_PATH, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        try:
            output = subprocess.check_output(
                ["journalctl", "-u", "sshd", "--no-pager", "--no-hostname"],
                text=True
            )
            return output.splitlines()
        except Exception as e:
            print(f"[ERROR] Failed to read logs: {e}")
            return []

def extract_login(line):
    for pattern in LOGIN_PATTERNS:
        match = re.search(pattern, line)
        if match:
            user = match.group(1)
            ip = match.group(2)
            time = " ".join(line.split()[0:3])
            return ip, user, time
    return None

def get_last_login():
    lines = read_auth_log()
    for line in reversed(lines):
        result = extract_login(line)
        if result:
            return result
    return "N/A", "N/A", "N/A"

def geo_lookup(ip):
    try:
        r = requests.get(GEO_API + ip, timeout=5).json()
        city = r.get("city", "Unknown")
        country = r.get("country", "Unknown")
        code = r.get("countryCode", "")
        flag = country_flag(code)
        return f"{city}, {country} {flag}"
    except Exception as e:
        print(f"[WARN] Geo lookup failed for {ip}: {e}")
        return "Unknown 🌫️"

def country_flag(code):
    if not code or len(code) != 2:
        return ""
    return chr(ord(code[0].upper()) + 127397) + chr(ord(code[1].upper()) + 127397)


_login_counter = 0
_last_login = ("N/A", "N/A", "N/A")

def record_login(ip, user, time):
    global _last_login, _login_counter
    _last_login = (ip, user, time)
    _login_counter += 1

def get_login_count():
    return _login_counter


