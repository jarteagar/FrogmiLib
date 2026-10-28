import json, sys
from pathlib import Path

BUSCAR = sys.argv[1].upper() if len(sys.argv) > 1 else None
jsonl = next(Path("salidas_cubowu_ent").glob("*.jsonl"), None)
if not jsonl:
    raise SystemExit("No hay .jsonl en salidas_cubowu_ent")

def fisico(p):
    return p.get("User_Formatted_Physical_Name") or p.get("Physical_Name")

entidades, attrs = [], []
with jsonl.open(encoding="utf-8-sig") as f:
    for linea in f:
        if not linea.strip():
            continue
        r = json.loads(linea)
        if r.get("clase") == "Entity":
            entidades.append(r)
        elif r.get("clase") == "Attribute":
            attrs.append(r)

print(f"Entity: {len(entidades)} | Attribute: {len(attrs)}")

if not BUSCAR:
    print("Primeras 30 entidades (Name | nombre fisico | Long_Id):")
    for e in entidades[:30]:
        p = e["propiedades"]
        print(f" - {e['nombre']} | {fisico(p)} | {p.get('Long_Id')}")
    raise SystemExit("Uso: python inspeccionar_entidad.py NOMBRE_LOGICO_O_FISICO")

def coincide(e):
    p = e["propiedades"]
    return BUSCAR in {
        (e["nombre"] or "").upper(),
        (p.get("Physical_Name") or "").upper(),
        (p.get("User_Formatted_Physical_Name") or "").upper(),
    }

ent = [e for e in entidades if coincide(e)]
print(f"Entidades que coinciden con '{BUSCAR}': {len(ent)}")
if not ent:
    raise SystemExit("Sin coincidencias")

nombres_dueno = set()
for e in ent:
    p = e["propiedades"]
    print("\n=== ENTIDAD ===")
    print("Name:", e["nombre"])
    print("Physical_Name:", p.get("Physical_Name"))
    print("User_Formatted_Physical_Name:", p.get("User_Formatted_Physical_Name"))
    print("Long_Id:", p.get("Long_Id"))
    print(json.dumps(p, ensure_ascii=False, indent=2)[:5000])
    for n in (e["nombre"], p.get("Physical_Name"),
              p.get("User_Formatted_Physical_Name")):
        if n:
            nombres_dueno.add(n.upper())

def dueno(a):
    return (a["propiedades"].get("Owner_Path") or "").split(".")[-1].upper()

cols = [a for a in attrs if dueno(a) in nombres_dueno]
print(f"\n=== ATRIBUTOS que apuntan a esta entidad: {len(cols)} ===")

CLAVES = ("defin", "comment", "descr", "note", "annot", "remark")
con_desc, union = 0, set()
for a in cols:
    p = a["propiedades"]
    union |= set(p)
    if any(any(c in k.lower() for c in CLAVES) and v not in (None, "", [])
           for k, v in p.items()):
        con_desc += 1
print(f"Con alguna propiedad descriptiva no vacia: {con_desc}/{len(cols)}")
print("Claves de propiedad vistas en los atributos:")
for k in sorted(union):
    print("  ", k)

print("\n=== 3 ATRIBUTOS: Name | nombre fisico ===")
for a in cols[:3]:
    print(f" - {a['nombre']} | {fisico(a['propiedades'])}")
    print(json.dumps(a, ensure_ascii=False, indent=2)[:3000])
