import asyncio, json, websockets

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3MmE5YTE0Yzk0NWQ0ZjExODYxYzJlYWZiNzRmZWE1YyIsImlhdCI6MTc3MzkxMDY4MiwiZXhwIjoyMDg5MjcwNjgyfQ.nf3wfc3l-xG94Peo2nMtDwnKLxIztBmxD47AbxXyCDk"

async def get_stats():
    uri = "ws://homeassistant:8123/api/websocket"
    async with websockets.connect(uri) as ws:
        msg = json.loads(await ws.recv())
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        msg = json.loads(await ws.recv())
        if msg["type"] != "auth_ok":
            print(f"Auth failed: {msg}")
            return
        await ws.send(json.dumps({
            "id": 1,
            "type": "recorder/statistics_during_period",
            "start_time": "2026-02-25T00:00:00+01:00",
            "end_time": "2026-04-02T00:00:00+01:00",
            "statistic_ids": ["sensor.heizenergie_energy"],
            "period": "day",
            "types": ["sum", "change"],
        }))
        msg = json.loads(await ws.recv())
        if msg.get("success"):
            data = msg["result"].get("sensor.heizenergie_energy", [])
            print("Datum;Tagesverbrauch_kWh;Gesamtstand_kWh")
            from datetime import datetime, timezone
            for row in data:
                ts = row["start"]
                if isinstance(ts, (int, float)):
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    start = dt.strftime("%Y-%m-%d")
                else:
                    start = str(ts)[:10]
                change = row.get("change", 0) or 0
                total = row.get("sum", 0) or 0
                print(f"{start};{change:.5f};{total:.5f}")
        else:
            print(f"Error: {json.dumps(msg, indent=2)}")

asyncio.run(get_stats())
