import json
from pathlib import Path
jsonl = next(Path("salidas_cubowu_ent").glob("*.jsonl"))
OBJ = "LFI_CODAGENCIAFIN"
with jsonl.open(encoding="utf-8-sig") as f:
    for linea in f:
        if not linea.strip():
            continue
        r = json.loads(linea)
        if r.get("clase") != "Entity":
            continue
        p = r["propiedades"]
        nombres = {r["nombre"], p.get("Physical_Name"),
                   p.get("User_Formatted_Physical_Name")}
        if OBJ not in {(n or "") for n in nombres}:
            continue
        print("Name:", r["nombre"], "| Long_Id:", p.get("Long_Id"))
        print("Total de claves:", len(p))
        for k, v in p.items():
            if any(s in k.lower() for s in ("comment", "defin", "descr", "note")):
                print(f"  {k!r} = {v!r}")
        print("Todas las claves:", sorted(p))
