import json
import urllib.request
from datetime import datetime, timezone

API_KEY = "123"
PREMIER_LEAGUE_ID = "4328"

url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsnextleague.php?id={PREMIER_LEAGUE_ID}"
print(f"Fetching: {url}")

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
    data = {"events": []}

events = data.get("events") or []
print(f"Events received: {len(events)}")

matches = []
for e in events:
    matches.append({
        "time": e.get("strTime") or "TBD",
        "home": e.get("strHomeTeam") or "?",
        "away": e.get("strAwayTeam") or "?",
        "league": e.get("strLeague") or "",
        "date": e.get("dateEvent") or "",
    })

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "matches": matches,
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Total saved: {len(matches)}")
