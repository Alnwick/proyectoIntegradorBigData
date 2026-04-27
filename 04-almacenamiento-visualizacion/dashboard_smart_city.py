import json
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(".")
VALIDOS = BASE_DIR / "eventos_validos.jsonl"
ANOMALIAS = BASE_DIR / "anomalias.jsonl"
RECHAZADOS = BASE_DIR / "eventos_rechazados.jsonl"

def leer_jsonl(ruta):
    datos = []
    if not ruta.exists():
        return datos
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                datos.append(json.loads(linea))
    return datos

eventos_validos = leer_jsonl(VALIDOS)
anomalias = leer_jsonl(ANOMALIAS)
rechazados = leer_jsonl(RECHAZADOS)

conteo_fuentes = Counter()
conteo_anomalias = Counter()
anomalias_por_fuente = Counter()
eventos_por_zona = Counter()
alertas_por_zona = Counter()

for ev in eventos_validos:
    fuente = ev.get("tipo_fuente", "desconocido")
    conteo_fuentes[fuente] += 1

    zona = ev.get("zona")
    if zona:
        eventos_por_zona[zona] += 1

for a in anomalias:
    tipo_anomalia = a.get("anomalia", {}).get("tipo_anomalia", "desconocida")
    fuente = a.get("tipo_fuente", "desconocido")
    zona = a.get("evento_original", {}).get("zona")

    conteo_anomalias[tipo_anomalia] += 1
    anomalias_por_fuente[fuente] += 1

    if zona:
        alertas_por_zona[zona] += 1

total_validos = len(eventos_validos)
total_anomalias = len(anomalias)
total_rechazados = len(rechazados)
total_eventos = total_validos + total_rechazados

porcentaje_validos = (total_validos / total_eventos * 100) if total_eventos else 0
porcentaje_rechazados = (total_rechazados / total_eventos * 100) if total_eventos else 0
tasa_anomalias = (total_anomalias / total_validos * 100) if total_validos else 0

print("\n===== DASHBOARD OPERATIVO SMART CITY =====\n")
print(f"Total de eventos procesados: {total_eventos}")
print(f"Eventos válidos: {total_validos} ({porcentaje_validos:.2f}%)")
print(f"Eventos rechazados: {total_rechazados} ({porcentaje_rechazados:.2f}%)")
print(f"Anomalías detectadas: {total_anomalias}")
print(f"Tasa de anomalías sobre válidos: {tasa_anomalias:.2f}%")

print("\n--- Eventos por fuente ---")
for fuente, total in conteo_fuentes.items():
    print(f"{fuente}: {total}")

print("\n--- Anomalías por tipo ---")
for tipo, total in conteo_anomalias.items():
    print(f"{tipo}: {total}")

print("\n--- Anomalías por fuente ---")
for fuente, total in anomalias_por_fuente.items():
    print(f"{fuente}: {total}")

print("\n--- Eventos por zona ---")
for zona, total in eventos_por_zona.items():
    print(f"{zona}: {total}")

print("\n--- Alertas por zona ---")
for zona, total in alertas_por_zona.items():
    print(f"{zona}: {total}")

# Guardar resumen estructurado
resumen = {
    "total_eventos_procesados": total_eventos,
    "eventos_validos": total_validos,
    "eventos_rechazados": total_rechazados,
    "anomalias_detectadas": total_anomalias,
    "porcentaje_validos": round(porcentaje_validos, 2),
    "porcentaje_rechazados": round(porcentaje_rechazados, 2),
    "tasa_anomalias_sobre_validos": round(tasa_anomalias, 2),
    "eventos_por_fuente": dict(conteo_fuentes),
    "anomalias_por_tipo": dict(conteo_anomalias),
    "anomalias_por_fuente": dict(anomalias_por_fuente),
    "eventos_por_zona": dict(eventos_por_zona),
    "alertas_por_zona": dict(alertas_por_zona),
}

with open("resumen_dashboard.json", "w", encoding="utf-8") as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2)

print("\nResumen guardado en: resumen_dashboard.json")