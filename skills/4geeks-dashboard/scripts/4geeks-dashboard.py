import json, urllib.request, os, datetime
from collections import Counter, defaultdict

# --- Leer token del entorno ---
token = ""
for e in open("/proc/self/environ","rb").read().split(b"\x00"):
    if e.startswith(b"FOURGEEKS_TOKEN="):
        # Token comes after the = sign
        parts = e.split(b"=", 1)
        if len(parts) > 1:
            token = parts[1].decode()
        break

if not token:
    print("ERROR: FOURGEEKS_TOKEN no encontrado en el entorno")
    exit(1)

headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
now = datetime.datetime.now(datetime.timezone.utc)

# --- Obtener perfil ---
req = urllib.request.Request("https://breathecode.herokuapp.com/v1/admissions/user/me", headers=headers)
user = json.loads(urllib.request.urlopen(req).read())

# --- Obtener tareas ---
req = urllib.request.Request("https://breathecode.herokuapp.com/v1/assignment/user/me/task", headers=headers)
tasks = json.loads(urllib.request.urlopen(req).read())

total = len(tasks)

# --- Conteos globales ---
status_counts = Counter(t.get("task_status","UNKNOWN") for t in tasks)
pending = status_counts.get("PENDING", 0)
done = status_counts.get("DONE", 0)
approved = status_counts.get("APPROVED", 0)
rejected = status_counts.get("REJECTED", 0)
completed = done + approved
pct = round(completed / total * 100) if total else 0

# --- Por cohorte ---
cohorts = defaultdict(lambda: {"t": 0, "PENDING": 0, "DONE": 0, "APPROVED": 0, "REJECTED": 0, "types": Counter()})
for t in tasks:
    c = t.get("cohort", {})
    cn = c.get("name", "?") if isinstance(c, dict) else "?"
    s = t.get("task_status", "?")
    tt = t.get("task_type", "?")
    cohorts[cn]["t"] += 1
    if s in cohorts[cn]:
        cohorts[cn][s] += 1
    cohorts[cn]["types"][tt] += 1

# --- Por tipo de tarea ---
type_info = defaultdict(lambda: {"total": 0, "done": 0, "approved": 0, "pending": 0})
for t in tasks:
    tt = t.get("task_type", "?")
    s = t.get("task_status", "?")
    type_info[tt]["total"] += 1
    if s == "DONE":
        type_info[tt]["done"] += 1
    elif s == "APPROVED":
        type_info[tt]["approved"] += 1
    elif s == "PENDING":
        type_info[tt]["pending"] += 1

# --- Últimas entregas ---
delivered = sorted([t for t in tasks if t.get("delivered_at")], key=lambda x: x["delivered_at"], reverse=True)

type_names = {"LESSON": "Lecciones", "PROJECT": "Proyectos", "EXERCISE": "Ejercicios", "QUIZ": "Cuestionarios"}

# ====== OUTPUT ======
print("📊 PANEL DE PROGRESO — 4GEEKS ACADEMY")
print(f"👤 {user.get('first_name','?')} {user.get('last_name','?')}")
print(f"📅 {now.strftime('%d/%m/%Y %H:%M')} UTC")
print()

# Barra de progreso general
bar_filled = round(20 * pct / 100)
bar_empty = 20 - bar_filled
bar = "█" * bar_filled + "░" * bar_empty
print(f"📊 PROGRESO GLOBAL")
print(f"   {bar}  {pct}%  ({completed}/{total})")
print()

# Métricas clave
print(f"📊 MÉTRICAS CLAVE")
print(f"   📋 Total tareas:      {total}")
print(f"   ✅ Entregadas:        {done}  ({round(done/total*100)}%)")
print(f"   ⭐ Aprobadas:         {approved}")
print(f"   ❌ Rechazadas:        {rejected}")
print(f"   🔴 Pendientes:        {pending}")
print(f"   🎯 Eficiencia:        {pct}% completado · {round(approved/total*100)}% aprobado oficialmente")
print()

# Por cohorte
print(f"📊 PROGRESO POR COHORTE")
print("━" * 45)
for cn in sorted(cohorts.keys()):
    cd = cohorts[cn]
    ct = cd["t"]
    ccomp = cd["DONE"] + cd["APPROVED"]
    cpct = round(ccomp / ct * 100) if ct else 0
    bar_f = round(10 * ccomp / ct) if ct else 0
    bar_e = 10 - bar_f
    bar_s = "█" * bar_f + "░" * bar_e

    parts = []
    if cd["PENDING"]: parts.append(f"🔴{cd['PENDING']}")
    if cd["DONE"]: parts.append(f"📤{cd['DONE']}")
    if cd["APPROVED"]: parts.append(f"⭐{cd['APPROVED']}")
    if cd["REJECTED"]: parts.append(f"❌{cd['REJECTED']}")
    status_s = " · ".join(parts)

    types_s = ", ".join(f"{type_names.get(t,t)} {n}" for t, n in cd["types"].most_common())

    print(f"\n🎓 {cn}")
    print(f"   {bar_s}  {cpct}%  ({ccomp}/{ct})")
    print(f"   {status_s}")
    print(f"   {types_s}")
print()

# Por tipo de tarea
print(f"📊 POR TIPO DE TAREA")
print("━" * 45)
type_order = sorted(type_info.keys(), key=lambda k: -type_info[k]["total"])
for tt in type_order:
    ti = type_info[tt]
    tc = ti["done"] + ti["approved"]
    tpct = round(tc / ti["total"] * 100) if ti["total"] else 0
    bar_f = round(10 * tc / ti["total"]) if ti["total"] else 0
    bar_e = 10 - bar_f
    bar_s = "█" * bar_f + "░" * bar_e
    name = type_names.get(tt, tt)
    extra = f" · 🔴{ti['pending']} pend" if ti["pending"] else ""
    print(f"   {name:15s} {bar_s}  {tpct}%  ({tc}/{ti['total']}){extra}")
print()

# Últimas entregas
if delivered:
    print(f"📊 ÚLTIMAS 5 ENTREGAS")
    print("━" * 45)
    for t in delivered[:5]:
        title = t.get("title","?")
        cn = t.get("cohort",{}).get("name","?") if isinstance(t.get("cohort"), dict) else "?"
        dd = t.get("delivered_at","")[:10]
        diff = now - datetime.datetime.fromisoformat(t["delivered_at"].replace("Z","+00:00"))
        ds = diff.days
        print(f"   📌 {title[:55]}")
        print(f"      {cn} · {dd} (hace {ds} días)")
print()

# Síntesis
print(f"📊 SÍNTESIS")
print("━" * 45)
print(f"   📋 {total} tareas asignadas en {len(cohorts)} cohortes")
print(f"   ✅ {completed} completadas ({pct}%) · ⭐ {approved} oficialmente aprobadas")
if pending:
    print(f"   🔴 {pending} pendientes por hacer")
if rejected:
    print(f"   ❌ {rejected} rechazadas por corregir")
if done:
    print(f"   📤 {done} esperando revisión de mentores")
print()
if pct < 30:
    print(f"💡 Apenas empezando. {pending} pendientes por resolver.")
elif pct < 70:
    print(f"💡 Buen ritmo. Vas por el {pct}% — sigue así.")
else:
    print(f"💡 Casi listo. {pct}% completado. Quedan detalles.")