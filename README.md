import json, sys
from pathlib import Path

TABLA = sys.argv[1].upper() if len(sys.argv) > 1 else None
jsonl = next(Path("salidas_cubowu_ent").glob("*.jsonl"), None)
if not jsonl:
    raise SystemExit("No hay .jsonl en salidas_cubowu_ent")

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
if not TABLA:
    print("Primeras 30 entidades:")
    for e in entidades[:30]:
        print(" -", e["nombre"])
    raise SystemExit("Vuelve a correr: python inspeccionar_entidad.py NOMBRE_TABLA")

ent = [e for e in entidades if (e["nombre"] or "").upper() == TABLA]
cols = [a for a in attrs
        if (a["propiedades"].get("Owner_Path") or "").upper().endswith("." + TABLA)]
print(f"Entidad(es) '{TABLA}': {len(ent)} | Atributos: {len(cols)}")

CLAVES = ("defin", "comment", "descr", "note", "annot", "remark")
def descriptivas(props):
    return {k: v for k, v in props.items()
            if any(c in k.lower() for c in CLAVES) and v not in (None, "", [])}

for e in ent:
    print("\n=== ENTIDAD (todas las propiedades) ===")
    print(json.dumps(e, ensure_ascii=False, indent=2)[:6000])

print("\n=== ATRIBUTOS: propiedades tipo descripcion ===")
con_desc = 0
claves_union = set()
for a in cols:
    claves_union |= set(a["propiedades"])
    d = descriptivas(a["propiedades"])
    if d:
        con_desc += 1
print(f"Atributos con alguna propiedad descriptiva no vacia: {con_desc}/{len(cols)}")
print("Claves de propiedad vistas en los atributos:")
for k in sorted(claves_union):
    print("  ", k)

print("\n=== 3 ATRIBUTOS COMPLETOS ===")
for a in cols[:3]:
    print(json.dumps(a, ensure_ascii=False, indent=2)[:3000])
