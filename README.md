import json
import sys
from pathlib import Path

# Ruta del NDJSON
RUTA_NDJSON = Path("modelos/UDV_Modelo_de_Datos_Logico_V0.640.ndjson")
NOMBRE_ENTIDAD = "f_reportegestion"

def main():
    if not RUTA_NDJSON.exists():
        print(f"No se encuentra el archivo: {RUTA_NDJSON}")
        sys.exit(1)

    entidades = {}
    campos = []

    # Leer NDJSON línea por línea
    with RUTA_NDJSON.open(encoding="utf-8-sig") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                r = json.loads(linea)
            except json.JSONDecodeError:
                continue

            if r.get("tipo") == "entidad":
                eid = r.get("entidad_id")
                if eid:
                    entidades[eid] = r
            elif r.get("tipo") == "campo":
                campos.append(r)

    # Buscar la entidad por nombre (case-insensitive)
    objetivo = None
    eid_objetivo = None
    for eid, ent in entidades.items():
        nombre = (ent.get("nombre") or "").strip().lower()
        if nombre == NOMBRE_ENTIDAD.lower():
            objetivo = ent
            eid_objetivo = eid
            break

    if not objetivo or not eid_objetivo:
        print(f"No se encontró la entidad con nombre: '{NOMBRE_ENTIDAD}'")
        print("Revisa mayúsculas/minúsculas o que exista en el NDJSON.")
        sys.exit(1)

    # Filtrar campos de esa entidad
    campos_entidad = [c for c in campos if c.get("entidad_id") == eid_objetivo]

    # Ordenar igual que en el NDJSON (por orden, luego por campo_fisico)
    campos_entidad.sort(
        key=lambda x: (
            x.get("orden") is None,
            x.get("orden") if x.get("orden") is not None else 0,
            (x.get("campo_fisico") or "").lower(),
        )
    )

    # Imprimir resultado
    print("=== ENTIDAD ===")
    print(json.dumps(objetivo, ensure_ascii=False, indent=2))
    print(f"\n=== CAMPOS ({len(campos_entidad)}) ===")

    for c in campos_entidad:
        print(
            f"- campo_fisico: {c.get('campo_fisico') or 'NULL'} | "
            f"campo_logico: {c.get('campo_logico') or 'NULL'} | "
            f"pk: {c.get('pk')} | fk: {c.get('fk')} | "
            f"obligatorio: {c.get('obligatorio')} | "
            f"orden: {c.get('orden')} | "
            f"definicion: {c.get('definicion') or 'NULL'}"
        )

    # Guardar salida completa a un archivo para revisarlo con calma
    salida = Path(f"f_reportegestion_extraccion.json")
    with salida.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "entidad": objetivo,
                "campos": campos_entidad,
                "total_campos": len(campos_entidad),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\nGuardado completo en: {salida.resolve()}")

if __name__ == "__main__":
    main()
