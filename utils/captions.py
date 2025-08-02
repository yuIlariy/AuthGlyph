import random

# 🌋 Themes for normal logins
themes = [
    "🦔 <b>Sentinel Mode</b>",
    "🌋 <b>Breach Watch</b>",
    "🧊 <b>Frost Login</b>",
    "🌪️ <b>Storm Access</b>",
    "🛡️ <b>Guardian Alert</b>",
    "🕵️ <b>Shadow Trace</b>",
    "⚡ <b>Pulse Entry</b>",
    "🧠 <b>Neural Breach</b>",
    "🛰️ <b>Orbital Ping</b>",
    "🧨 <b>Exploit Triggered</b>",
    "🪓 <b>Root Chop</b>",
    "🧬 <b>Genome Access</b>",
    "🧱 <b>Firewall Breach</b>",
    "🧿 <b>Watcher Glyph</b>",
    "🪐 <b>Cosmic Login</b>",
    "🧛 <b>Vampire Session</b>",
    "🧟 <b>Zombie Shell</b>",
    "🧳 <b>Traveler Login</b>",
    "🧭 <b>Compass Trace</b>",
    "🧰 <b>Toolchain Entry</b>",
    "🧗 <b>Climber Access</b>",
    "🧼 <b>Clean Shell</b>",
    "🧱 <b>Bricklayer Mode</b>",
    "🧞 <b>Wishful Login</b>",
    "🧙 <b>Wizard Shell</b>",
    "🧚 <b>Fairy Ping</b>",
    "🧜 <b>Deep Sea Login</b>",
    "🧀 <b>Cheesy Breach</b>",
    "🧊 <b>Glacier Trace</b>",
    "🧨 <b>Detonator Ping</b>",
    "🧵 <b>Threaded Entry</b>",
    "🧹 <b>Sweeper Login</b>",
    "🧺 <b>Basket Shell</b>",
    "🧼 <b>Sanitized Access</b>",
    "🧯 <b>Extinguisher Mode</b>",
    "🧪 <b>Lab Session</b>",
    "🧫 <b>Petri Login</b>",
    "🧬 <b>DNA Trace</b>",
]

# 🔥 Suspicious themes for foreign logins
suspicious_themes = [
    "🚨 <b>Suspicious Login</b>",
    "🧨 <b>Foreign Breach</b>",
    "🕷️ <b>Unusual Access</b>",
    "🛑 <b>Alert: External Shell</b>",
    "🧟 <b>Zombie Ping</b>",
    "🧛 <b>Vampire Trace</b>",
    "🧬 <b>Unknown Genome</b>",
    "🧠 <b>Alien Session</b>",
    "🧿 <b>Glyph Intrusion</b>",
    "🧱 <b>Firewall Breach</b>",
]

def themed_caption(ip, user, time, geo, whois=None):
    country_flag = geo.split()[-1] if geo else ""
    is_foreign = country_flag != "🇰🇪"
    theme = random.choice(suspicious_themes if is_foreign else themes)

    caption = (
        f"{theme}\n"
        f"👤 <b>User:</b> <code>{user}</code>\n"
        f"🕒 <b>Time:</b> <code>{time}</code>\n"
        f"🌐 <b>IP:</b> <code>{ip}</code>\n"
        f"🌍 <b>Location:</b> {geo}"
    )

    if whois:
        caption += f"\n🛰️ <b>WHOIS:</b> <code>{whois}</code>"

    return caption


