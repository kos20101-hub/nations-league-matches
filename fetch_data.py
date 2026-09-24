import json
import urllib.request
from datetime import datetime, timezone

# Бесплатный ключ TheSportsDB для всех пользователей
API_KEY = "123"

# Берём сегодняшнюю дату
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsday.php?d={today}&s=Soccer"
print(f"Fetching: {url}")

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
except Exception as e:
    print(f"Error fetching data: {e}")
    data = {"events": []}

events = data.get("events") or []

# Фильтруем только Лигу наций
nations = [
    e for e in events
    if e.get("strLeague") and "Nations League" in e["strLeague"]
]

matches = []
for e in nations:
    matches.append({
        "time": e.get("strTime") or "TBD",
        "home": e.get("strHomeTeam") or "?",
        "away": e.get("strAwayTeam") or "?",
        "league": e.get("strLeague") or "",
        "status": e.get("strStatus") or "",
    })

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "date": today,
    "matches": matches,
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(matches)} matches to matches.json")
