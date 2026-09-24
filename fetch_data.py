import json
import urllib.request
from datetime import datetime, timezone

API_KEY = "123"

# ID Лиги наций УЕФА в базе TheSportsDB
NATIONS_LEAGUE_ID = "4491"

endpoints = {
    "eventsnextleague": f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsnextleague.php?id={NATIONS_LEAGUE_ID}",
    "eventspastleague": f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventspastleague.php?id={NATIONS_LEAGUE_ID}",
}

all_matches = []

for name, url in endpoints.items():
    print(f"--- Trying {name} ---")
    print(f"URL: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except Exception as e:
        print(f"Error: {e}")
        continue

    events = data.get("events") or []
    print(f"Events received: {len(events)}")
    for e in events[:3]:
        print(f"  {e.get('strHomeTeam')} vs {e.get('strAwayTeam')} | {e.get('strLeague')} | {e.get('dateEvent')}")

    for e in events:
        all_matches.append({
            "time": e.get("strTime") or "TBD",
            "home": e.get("strHomeTeam") or "?",
            "away": e.get("strAwayTeam") or "?",
            "league": e.get("strLeague") or "",
            "date": e.get("dateEvent") or "",
        })

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "matches": all_matches,
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Total saved: {len(all_matches)}")
