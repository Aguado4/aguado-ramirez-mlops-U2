import json
import os
from collections import Counter
from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

STATS_FILE = os.environ.get("STATS_FILE", "predictions.log")

CATEGORIAS = [
    "NO ENFERMO",
    "ENFERMEDAD LEVE",
    "ENFERMEDAD AGUDA",
    "ENFERMEDAD CRÓNICA",
    "ENFERMEDAD TERMINAL",
]


def predecir(temperatura: float, nivel_dolor: int, dias_sintomas: int) -> str:
    """
    Simula un modelo de clasificacion de enfermedad.
    Retorna uno de: NO ENFERMO, ENFERMEDAD LEVE, ENFERMEDAD AGUDA,
    ENFERMEDAD CRONICA, ENFERMEDAD TERMINAL.

    Parametros:
      - temperatura:    temperatura corporal en grados Celsius
      - nivel_dolor:    nivel de dolor autoreportado de 0 a 10
      - dias_sintomas:  cantidad de dias con sintomas presentes
    """
    score = 0

    if temperatura >= 40.5:
        score += 8
    elif temperatura >= 39.5:
        score += 6
    elif temperatura >= 38.5:
        score += 4
    elif temperatura >= 37.5:
        score += 2

    if nivel_dolor >= 9:
        score += 4
    elif nivel_dolor >= 8:
        score += 3
    elif nivel_dolor >= 5:
        score += 2
    elif nivel_dolor >= 3:
        score += 1

    if dias_sintomas > 21:
        score += 4
    elif dias_sintomas > 14:
        score += 3
    elif dias_sintomas >= 8:
        score += 2
    elif dias_sintomas >= 3:
        score += 1

    if score <= 2:
        return "NO ENFERMO"
    elif score <= 5:
        return "ENFERMEDAD LEVE"
    elif score <= 8:
        return "ENFERMEDAD AGUDA"
    elif score <= 12:
        return "ENFERMEDAD CRÓNICA"
    else:
        return "ENFERMEDAD TERMINAL"


def registrar_prediccion(entrada: dict, resultado: str) -> None:
    registro = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "entrada": entrada,
        "resultado": resultado,
    }
    with open(STATS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def leer_predicciones() -> list[dict]:
    if not os.path.exists(STATS_FILE):
        return []
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predecir", methods=["POST"])
def predecir_endpoint():
    try:
        temperatura = float(request.form["temperatura"])
        nivel_dolor = int(request.form["nivel_dolor"])
        dias_sintomas = int(request.form["dias_sintomas"])

        if not (35.0 <= temperatura <= 42.0):
            raise ValueError("Temperatura fuera de rango (35-42 °C).")
        if not (0 <= nivel_dolor <= 10):
            raise ValueError("Nivel de dolor debe estar entre 0 y 10.")
        if dias_sintomas < 0:
            raise ValueError("Los días de síntomas no pueden ser negativos.")

        resultado = predecir(temperatura, nivel_dolor, dias_sintomas)
        registrar_prediccion(
            {
                "temperatura": temperatura,
                "nivel_dolor": nivel_dolor,
                "dias_sintomas": dias_sintomas,
            },
            resultado,
        )
        return render_template("index.html", resultado=resultado)

    except (ValueError, KeyError) as e:
        return render_template("index.html", error=str(e))


@app.route("/stats", methods=["GET"])
def stats_endpoint():
    predicciones = leer_predicciones()
    conteo = Counter(p["resultado"] for p in predicciones)
    total_por_categoria = {cat: conteo.get(cat, 0) for cat in CATEGORIAS}
    ultimas_5 = predicciones[-5:][::-1]
    fecha_ultima = predicciones[-1]["timestamp"] if predicciones else None

    return jsonify(
        {
            "total_predicciones": len(predicciones),
            "total_por_categoria": total_por_categoria,
            "ultimas_5": ultimas_5,
            "fecha_ultima_prediccion": fecha_ultima,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
