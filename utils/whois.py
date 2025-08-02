import requests

def whois_info(ip):
    try:
        r = requests.get(f"http://ipwho.is/{ip}", timeout=5).json()
        conn = r.get("connection", {})
        isp = conn.get("isp", "Unknown ISP")
        asn = conn.get("asn", "Unknown ASN")
        org = conn.get("org", "")
        domain = conn.get("domain", "")
        return f"{isp} (ASN {asn}) — {org} — {domain}"
    except Exception as e:
        print(f"[WARN] WHOIS lookup failed for {ip}: {e}")
        return "Unknown WHOIS 🌫️"

  
