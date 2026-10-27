import json
from pathlib import Path

SALIDA_DIR = Path("salidas_cubowu")
OBJETIVO = "F_REPORTEGESTION"

# Buscar el jsonl generado
jsonl = None
for p in SALIDA_DIR.glob("*.jsonl"):
    jsonl = p
    break

if not jsonl:
    print("No se encontró ningún .jsonl en salidas_cubowu")
    raise SystemExit

print(f"Leyendo: {jsonl}")
encontrado = []

with jsonl.open(encoding="utf-8-sig") as f:
    for linea in f:
        linea = linea.strip()
        if not linea:
            continue
        try:
            r = json.loads(linea)
        except:
            continue
        nombre = (r.get("nombre") or "").strip().upper()
        if nombre == OBJETIVO.upper():
            encontrado.append(r)

if not encontrado:
    print(f"No se encontró {OBJETIVO} en el jsonl")
    raise SystemExit

for i, obj in enumerate(encontrado):
    print("="*80)
    print(f"OBJETO #{i+1}")
    print("Clase:", obj.get("clase"))
    print("Nombre:", obj.get("nombre"))
    print("ObjetoId:", obj.get("objeto_id"))
    print("="*80)
    props = obj.get("propiedades") or {}
    # Mostrar solo las que nos interesan primero
    claves_interes = ["Definition","Comment","Long_Description","Entity.Comment","Entity.Definition","Table.Comment","Table.Definition","Physical_Name","User_Formatted_Physical_Name","Long_Id"]
    print("\n--- CLAVES INTERESANTES ---")
    for k in claves_interes:
        if k in props:
            print(f"{k}: {props[k]}")
    print("\n--- TODAS LAS PROPIEDADES ---")
    for k in sorted(props.keys()):
        v = props[k]
        # acortar un poco si es muy largo pero queremos verlo
        if isinstance(v, str) and len(v) > 200:
            print(f"{k}: {v[:200]} ... [truncado]")
        else:
            print(f"{k}: {v}")
    print("\n")

# Guardar completo
out = Path("f_reportegestion_crudo.json")
with out.open("w", encoding="utf-8") as f:
    json.dump(encontrado, f, ensure_ascii=False, indent=2)
print(f"Guardado completo en {out.resolve()}")
