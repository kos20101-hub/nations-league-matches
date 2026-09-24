import json
import os
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("API_FOOTBALL_KEY")
if not API_KEY:
    raise SystemExit("API_FOOTBALL_KEY is not set")

# Временно тестируем 2024 год
today = "2024-09-10"

url = f"https://v3.football.api-sports.io/fixtures?date={today}&league=5&season=2024"
req = urllib.request.Request(url, headers={
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io",
})

print(f"Fetching: {url}")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
except Exception as e:
    print(f"Error fetching data: {e}")
    data = {"response": []}

fixtures = data.get("response") or []

matches = []
for f in fixtures:
    fixture = f.get("fixture", {})
    teams = f.get("teams", {})
    league = f.get("league", {})
    matches.append({
        "time": (fixture.get("date") or "")[11:16] or "TBD",
        "home": teams.get("home", {}).get("name") or "?",
        "away": teams.get("away", {}).get("name") or "?",
        "league": league.get("name") or "",
        "status": (fixture.get("status") or {}).get("short") or "",
    })

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "date": today,
    "matches": matches,
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(matches)} matches to matches.json")
