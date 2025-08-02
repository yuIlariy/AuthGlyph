import re
import subprocess
import requests
import json
import os
from config import GEO_API, AUTH_LOG_PATH

# 🧠 Supported login patterns
LOGIN_PATTERNS = [
    r"Accepted password for (\w+) from ([\d\.]+)",
    r"Accepted publickey for (\w+) from ([\d\.]+)",
    r"Accepted keyboard-interactive/pam for (\w+) from ([\d\.]+)"
]

# 🧱 In-memory login store
_login_records = []
_login_counter = 0
_last_login = ("N/A", "N/A", "N/A")

STATS_FILE = "logs/logins.json"
BASE_COUNTRY_CODE = "KE"  # ☄️ Kenya is home

# 🔍 Read system logs
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

# 🔎 Extract login line
def extract_login(line):
    for pattern in LOGIN_PATTERNS:
        match = re.search(pattern, line)
        if match:
            user = match.group(1)
            ip = match.group(2)
            time = " ".join(line.split()[0:3])
            return ip, user, time
    return None

# 🧠 Get latest login from logs
def get_last_login():
    lines = read_auth_log()
    for line in reversed(lines):
        result = extract_login(line)
        if result:
            return result
    return "N/A", "N/A", "N/A"

# 🌍 Geo IP lookup with country flag and WHOIS glyph
def geo_lookup(ip):
    try:
        r = requests.get(GEO_API + ip, timeout=5).json()

        city = r.get("city", "Unknown")
        country = r.get("country_name", "Unknown")
        code = r.get("country_code2", "").upper()

        if not code or len(code) != 2 or not code.isalpha():
            code = "ZZ"  # 🌫️ Unknown country

        flag = country_flag(code)

        is_proxy = r.get("is_proxy", False)
        is_anonymous = r.get("is_anonymous", False)
        is_hosting = r.get("is_hosting", False)

        if is_proxy or is_anonymous:
            whois_type = f"VPN {flag}"
        elif is_hosting:
            whois_type = f"Hosting {flag}"
        else:
            whois_type = f"Residential {flag}"

        geo_str = f"{city}, {country} {flag}"
        return geo_str, code, whois_type
    except Exception as e:
        print(f"[WARN] Geo lookup failed for {ip}: {e}")
        return "Unknown 🌫️", "ZZ", "Unknown 🌫️"

# 🏳️ Convert country code to emoji flag
def country_flag(code):
    if not code or len(code) != 2 or not code.isalpha():
        return "🌍"
    return chr(ord(code[0].upper()) + 127397) + chr(ord(code[1].upper()) + 127397)

# 💾 Save login records to disk
def save_login_stats():
    try:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, "w") as f:
            json.dump(_login_records, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save login stats: {e}")

# 🔁 Load login records from disk
def load_login_stats():
    global _login_records, _login_counter
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                _login_records = json.load(f)
                for entry in _login_records:
                    if "country" in entry and isinstance(entry["country"], str):
                        entry["country"] = entry["country"].upper()
                _login_counter = len(_login_records)
        except Exception as e:
            print(f"[ERROR] Failed to load login stats: {e}")

# 🧾 Record login for stats and grep
def record_login(ip, user, time, country="", whois="Unknown"):
    global _last_login, _login_counter
    _last_login = (ip, user, time)
    _login_counter += 1
    country = country.upper() if country else "ZZ"
    _login_records.append({
        "ip": ip,
        "user": user,
        "time": time,
        "country": country,
        "whois": whois
    })
    save_login_stats()

# 🧼 Retrofix broken country codes
def fix_login_records():
    fixed = 0
    for entry in _login_records:
        code = entry.get("country", "").upper()
        if not code or len(code) != 2 or not code.isalpha():
            geo_str, new_code, whois = geo_lookup(entry["ip"])
            entry["country"] = new_code
            entry["whois"] = whois
            fixed += 1
    if fixed:
        save_login_stats()
    return fixed

# 📊 Total login count
def get_login_count():
    return _login_counter

# 🔍 Search login records
def search_logins(query: str):
    query = query.lower()
    return [
        entry for entry in _login_records
        if query in entry["user"].lower()
        or query in entry["ip"].lower()
        or query in entry.get("country", "").lower()
        or query in entry.get("whois", "").lower()
    ]

# 🔥 Foreign login check
def is_foreign(entry: dict) -> bool:
    code = entry.get("country", "").upper()
    return code != BASE_COUNTRY_CODE


