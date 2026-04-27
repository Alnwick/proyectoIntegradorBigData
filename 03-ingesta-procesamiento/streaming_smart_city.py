import json
import random
import time
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("output_smart_city")
OUTPUT_DIR.mkdir(exist_ok=True)

VALIDOS_FILE = OUTPUT_DIR / "eventos_validos.jsonl"
ANOMALIAS_FILE = OUTPUT_DIR / "anomalias.jsonl"
RECHAZADOS_FILE = OUTPUT_DIR / "eventos_rechazados.jsonl"


def guardar_jsonl(ruta, dato):
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(dato, ensure_ascii=False) + "\n")


def timestamp_actual():
    return datetime.now().isoformat()


def generar_evento_transporte():
    velocidad = round(random.uniform(-10, 140), 2)
    return {
        "timestamp": timestamp_actual(),
        "tipo_fuente": "transporte_publico",
        "unidad_id": f"BUS_{random.randint(1, 30)}",
        "ruta": f"R{random.randint(1, 12)}",
        "lat": round(random.uniform(19.30, 19.50), 6),
        "lon": round(random.uniform(-99.25, -99.05), 6),
        "velocidad": velocidad,
        "estado": random.choice(["en_ruta", "detenido", "fuera_servicio"])
    }


def generar_evento_ambiente():
    return {
        "timestamp": timestamp_actual(),
        "tipo_fuente": "sensor_ambiental",
        "sensor_id": f"AIR_{random.randint(1, 20)}",
        "zona": random.choice(["norte", "sur", "centro", "oriente", "poniente"]),
        "pm25": round(random.uniform(5, 220), 2),
        "temperatura": round(random.uniform(-20, 60), 2),
        "humedad": round(random.uniform(10, 100), 2)
    }


def generar_evento_camara():
    return {
        "timestamp": timestamp_actual(),
        "tipo_fuente": "camara_simulada",
        "camara_id": f"CAM_{random.randint(1, 15)}",
        "zona": random.choice(["norte", "sur", "centro", "oriente", "poniente"]),
        "evento": random.choice(["flujo_normal", "aglomeracion", "intrusion", "accidente"]),
        "nivel_confianza": round(random.uniform(-0.2, 1.2), 2)
    }


def generar_evento():
    tipo = random.choice(["transporte", "ambiente", "camara"])
    if tipo == "transporte":
        return generar_evento_transporte()
    elif tipo == "ambiente":
        return generar_evento_ambiente()
    else:
        return generar_evento_camara()


def validar_evento(evento):
    obligatorios = ["timestamp", "tipo_fuente"]
    for campo in obligatorios:
        if campo not in evento:
            return False, f"Falta campo obligatorio: {campo}"

    tipo = evento["tipo_fuente"]

    if tipo == "transporte_publico":
        if "velocidad" not in evento:
            return False, "Falta velocidad"
        if evento["velocidad"] < 0 or evento["velocidad"] > 120:
            return False, "Velocidad fuera de rango"

    elif tipo == "sensor_ambiental":
        if "temperatura" not in evento or "pm25" not in evento:
            return False, "Faltan campos ambientales"
        if evento["temperatura"] < -10 or evento["temperatura"] > 55:
            return False, "Temperatura fuera de rango"
        if evento["pm25"] < 0:
            return False, "PM2.5 inválido"

    elif tipo == "camara_simulada":
        if "nivel_confianza" not in evento:
            return False, "Falta nivel_confianza"
        if evento["nivel_confianza"] < 0 or evento["nivel_confianza"] > 1:
            return False, "Nivel de confianza fuera de rango"

    else:
        return False, "Tipo de fuente desconocido"

    return True, "Evento válido"


def detectar_anomalia(evento):
    tipo = evento["tipo_fuente"]

    if tipo == "transporte_publico":
        if evento["velocidad"] > 100:
            return {
                "tipo_anomalia": "velocidad_excesiva",
                "detalle": f"Unidad {evento['unidad_id']} con velocidad de {evento['velocidad']} km/h"
            }
        if evento["estado"] == "detenido" and evento["velocidad"] == 0:
            return {
                "tipo_anomalia": "unidad_detenida",
                "detalle": f"Unidad {evento['unidad_id']} detenida en ruta {evento['ruta']}"
            }

    elif tipo == "sensor_ambiental":
        if evento["pm25"] > 150:
            return {
                "tipo_anomalia": "contaminacion_alta",
                "detalle": f"Sensor {evento['sensor_id']} reporta PM2.5 de {evento['pm25']}"
            }
        if evento["temperatura"] > 45:
            return {
                "tipo_anomalia": "temperatura_extrema",
                "detalle": f"Sensor {evento['sensor_id']} reporta temperatura de {evento['temperatura']} °C"
            }

    elif tipo == "camara_simulada":
        if evento["evento"] in ["intrusion", "accidente"] and evento["nivel_confianza"] >= 0.8:
            return {
                "tipo_anomalia": "evento_critico_camara",
                "detalle": f"Cámara {evento['camara_id']} detecta {evento['evento']} con confianza {evento['nivel_confianza']}"
            }
        if evento["evento"] == "aglomeracion" and evento["nivel_confianza"] >= 0.75:
            return {
                "tipo_anomalia": "aglomeracion_detectada",
                "detalle": f"Cámara {evento['camara_id']} detecta aglomeración con confianza {evento['nivel_confianza']}"
            }

    return None


def limpiar_archivos():
    for ruta in [VALIDOS_FILE, ANOMALIAS_FILE, RECHAZADOS_FILE]:
        if ruta.exists():
            ruta.unlink()


def ejecutar_streaming_simulado(total_eventos=50, pausa=0.2):
    limpiar_archivos()

    metricas = {
        "total_generados": 0,
        "validos": 0,
        "rechazados": 0,
        "anomalias": 0
    }

    for _ in range(total_eventos):
        evento = generar_evento()
        metricas["total_generados"] += 1

        valido, motivo = validar_evento(evento)

        if not valido:
            guardar_jsonl(RECHAZADOS_FILE, {
                "evento": evento,
                "motivo_rechazo": motivo
            })
            metricas["rechazados"] += 1
        else:
            guardar_jsonl(VALIDOS_FILE, evento)
            metricas["validos"] += 1

            anomalia = detectar_anomalia(evento)
            if anomalia:
                guardar_jsonl(ANOMALIAS_FILE, {
                    "timestamp": evento["timestamp"],
                    "tipo_fuente": evento["tipo_fuente"],
                    "evento_original": evento,
                    "anomalia": anomalia
                })
                metricas["anomalias"] += 1

        time.sleep(pausa)

    return metricas


if __name__ == "__main__":
    resultado = ejecutar_streaming_simulado(total_eventos=60, pausa=0.1)
    print("Simulación finalizada")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print(f"Eventos válidos: {VALIDOS_FILE}")
    print(f"Anomalías: {ANOMALIAS_FILE}")
    print(f"Rechazados: {RECHAZADOS_FILE}")