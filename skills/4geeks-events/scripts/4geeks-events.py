#!/usr/bin/env python3
import json, urllib.request, os, datetime

def get_token():
    for e in open("/proc/self/environ","rb").read().split(b"\x00"):
        if e.startswith(b"FOURGEEKS_TOKEN="):
            parts = e.split(b"=", 1)
            if len(parts) > 1:
                return parts[1].decode()
    return ""

token = get_token()
if not token:
    print("❌ FOURGEEKS_TOKEN no encontrado en el entorno")
    exit(1)

headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
now = datetime.datetime.now(datetime.timezone.utc)

# Obtener eventos próximos
req = urllib.request.Request("https://breathecode.herokuapp.com/v1/events/all?upcoming=true", headers=headers)
resp = urllib.request.urlopen(req)
events = json.loads(resp.read())

if not events:
    print("📭 No hay eventos próximos programados.")
    exit(0)

print("📅 PRÓXIMOS EVENTOS — 4GEEKS ACADEMY")
print(f"   {len(events)} evento(s) encontrado(s)")
print()

# Ordenar por fecha
events.sort(key=lambda e: e.get("starting_at", ""))

for ev in events:
    title = ev.get("title", "?")
    start = ev.get("starting_at", "")
    end = ev.get("ending_at", "")
    excerpt = (ev.get("excerpt") or "").strip()
    etype = ev.get("event_type", {})
    etype_name = etype.get("name", "") if isinstance(etype, dict) else ""
    lang = ev.get("lang", "?")
    status = ev.get("status", "?")
    online = ev.get("online_event", False)
    venue = ev.get("venue", None)
    capacity = ev.get("capacity", 0)
    url = ev.get("url", "")
    banner = ev.get("banner", "")
    tags = (ev.get("tags") or "").split(",")
    host_user = ev.get("host_user", {})
    host_name = host_user.get("first_name", "") if isinstance(host_user, dict) else ""
    if isinstance(host_user, dict) and host_user.get("last_name"):
        host_name += " " + host_user["last_name"]

    # Parsear fechas
    try:
        start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
        start_pretty = start_dt.strftime("%d/%m/%Y %H:%M")
        end_dt = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
        end_pretty = end_dt.strftime("%H:%M")
        days_until = (start_dt - now).days
        if days_until == 0:
            when = "🟢 Hoy"
        elif days_until == 1:
            when = "🟡 Mañana"
        elif days_until <= 7:
            when = f"🟠 En {days_until} días"
        else:
            when = f"📅 En {days_until} días"
    except:
        start_pretty = start[:16] if start else "?"
        end_pretty = end[:16] if end else "?"
        when = "📅"

    print(f"{when} {title}")
    print(f"   📆 {start_pretty} → {end_pretty}")
    if excerpt:
        print(f"   📝 {excerpt}")
    if etype_name:
        print(f"   🏷️ {etype_name}")
    if lang:
        print(f"   🌐 {lang.upper()}")
    if host_name:
        print(f"   🎙️ {host_name}")
    if online:
        print(f"   💻 Online")
    elif venue:
        print(f"   📍 {venue}")
    if capacity:
        print(f"   👥 {capacity} plazas")
    if url:
        print(f"   🔗 {url}")
    if banner:
        print(f"   🖼️ {banner}")
    print()

# Resumen por tipo
from collections import Counter
type_counts = Counter()
for ev in events:
    et = ev.get("event_type", {})
    tn = et.get("name", "Sin tipo") if isinstance(et, dict) else "Sin tipo"
    type_counts[tn] += 1

print("📊 RESUMEN")
print("━" * 30)
for tname, count in type_counts.most_common():
    print(f"   {tname}: {count}")
print(f"\n   Total: {len(events)} evento(s) próximos")