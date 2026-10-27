import json
import sys
from pathlib import Path

# Ruta del JSON
RUTA_JSON = Path("modelos/UDV_Modelo_de_Datos_Logico_V0.640.json")
NOMBRE_ENTIDAD = "f_reportegestion"

def main():
    if not RUTA_JSON.exists():
        print(f"No se encuentra el archivo: {RUTA_JSON}")
        sys.exit(1)

    try:
        with RUTA_JSON.open(encoding="utf-8-sig") as f:
            doc = json.load(f)
    except Exception as e:
        print(f"Error al leer el JSON: {e}")
        sys.exit(1)

    entidades = doc.get("entidades", [])
    atributos = doc.get("atributos", [])

    # Buscar la entidad por nombre (case-insensitive)
    objetivo = None
    for e in entidades:
        nombre = (e.get("nombre") or "").strip().lower()
        if nombre == NOMBRE_ENTIDAD.lower():
            objetivo = e
            break

    if not objetivo:
        print(f"No se encontró la entidad con nombre: '{NOMBRE_ENTIDAD}'")
        sys.exit(1)

    eid_objetivo = objetivo.get("id")

    if not eid_objetivo:
        print("La entidad encontrada no tiene 'id'. Revisa el JSON.")
        sys.exit(1)

    # Filtrar atributos por entidad_id
    atributos_entidad = [a for a in atributos if a.get("entidad_id") == eid_objetivo]

    # Ordenar igual que como se consume (por orden, luego por columna física)
    atributos_entidad.sort(
        key=lambda x: (
            x.get("orden") is None,
            x.get("orden") if x.get("orden") is not None else 0,
            (x.get("columna_fisica") or "").lower(),
        )
    )

    # Imprimir resultado
    print("=== ENTIDAD ===")
    print(json.dumps(objetivo, ensure_ascii=False, indent=2))
    print(f"\n=== ATRIBUTOS ({len(atributos_entidad)}) ===")

    for a in atributos_entidad:
        print(
            f"- columna_fisica: {a.get('columna_fisica') or 'NULL'} | "
            f"atributo: {a.get('atributo') or 'NULL'} | "
            f"pk: {a.get('pk')} | fk: {a.get('fk')} | "
            f"obligatorio: {a.get('obligatorio')} | "
            f"orden: {a.get('orden')} | "
            f"descripcion: {a.get('descripcion') or 'NULL'}"
        )

    # Guardar salida completa
    salida = Path("f_reportegestion_extraccion_json.json")
    with salida.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "entidad": objetivo,
                "atributos": atributos_entidad,
                "total_atributos": len(atributos_entidad),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\nGuardado completo en: {salida.resolve()}")

if __name__ == "__main__":
    main()
