import json
import urllib.request
from datetime import datetime, timezone

API_KEY = "123"
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsday.php?d={today}&s=Soccer"
print(f"Fetching: {url}")

try:
    with urllib.request.urlopen(url) as response:
        raw_text = response.read().decode("utf-8")
        data = json.loads(raw_text)
except Exception as e:
    print(f"Error fetching data: {e}")
    raw_text = ""
    data = {"events": []}

# Сохраняем сырой ответ, чтобы посмотреть, что прислал сервис
with open("raw_debug.json", "w", encoding="utf-8") as f:
    f.write(raw_text)

events = data.get("events") or []
print(f"Total soccer events received: {len(events)}")

# Покажем первые 5 названий турниров, чтобы понять, что вообще есть
for e in events[:5]:
    print(f"  League: {e.get('strLeague')}")

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "date": today,
    "matches": [],
}

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Debug run finished")
