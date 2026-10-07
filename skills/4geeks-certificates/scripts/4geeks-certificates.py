#!/usr/bin/env python3
import json, urllib.request, os

token = ""
for e in open("/proc/self/environ","rb").read().split(b"\x00"):
    if e.startswith(b"FOURGEEKS_TOKEN="):
        parts = e.split(b"=", 1)
        if len(parts) > 1:
            token = parts[1].decode()
        break
if not token:
    print("ERROR: FOURGEEKS_TOKEN no encontrado")
    exit(1)

headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

try:
    req = urllib.request.Request("https://breathecode.herokuapp.com/v1/certificate/me", headers=headers)
    certs = json.loads(urllib.request.urlopen(req).read())
except urllib.error.HTTPError as e:
    if e.code == 401:
        print("❌ Token expirado. Renueva FOURGEEKS_TOKEN.")
    else:
        print(f"❌ Error {e.code}: {e.read().decode()[:200]}")
    exit(1)

if not certs:
    print("📭 No tienes certificados emitidos aún.")
    exit(0)

print(f"📜 CERTIFICADOS — 4GEEKS ACADEMY")
print(f"   Total: {len(certs)} certificado(s)")
print()

for c in certs:
    cid = c.get("id", "?")
    status = c.get("status", "?")
    status_text = c.get("status_text", "")
    signed_by = c.get("signed_by", "?")
    signed_role = c.get("signed_by_role", "")
    issued = (c.get("issued_at") or "")[:10]
    
    spec = c.get("specialty", {})
    spec_name = spec.get("name", "?") if isinstance(spec, dict) else "?"
    
    acad = c.get("academy", {})
    acad_name = acad.get("name", "?") if isinstance(acad, dict) else "?"
    
    cohort = c.get("cohort", {})
    cohort_name = cohort.get("name", "?") if isinstance(cohort, dict) else "?"
    
    preview = c.get("preview_url", "")
    pdf = c.get("pdf_url", "")
    
    # Icono según estado
    icon = "✅" if status == "PERSISTED" else "⏳" if status == "PENDING" else "❓"
    
    print(f"{icon} {spec_name}")
    print(f"   📂 Academia: {acad_name} · Cohorte: {cohort_name}")
    print(f"   🖊️ Firmado por: {signed_by} ({signed_role})")
    print(f"   📅 Expedido: {issued}")
    print(f"   📌 Estado: {status}")
    if status_text:
        print(f"      {status_text}")
    if preview:
        print(f"   🔍 Vista previa: {preview}")
    if pdf:
        print(f"   📄 PDF: {pdf}")
    print()

# Mostrar solo datos relevantes para Telegram
cert_names = []
for c in certs:
    s = c.get("specialty", {})
    if isinstance(s, dict) and s.get("name"):
        cert_names.append(s["name"])
print(f"📊 Resumen: {len(certs)} certificado(s) — {', '.join(cert_names)}")