import json
import os

import pytest

import app as app_module
from app import app, predecir


@pytest.fixture(autouse=True)
def aislar_archivo_stats(tmp_path, monkeypatch):
    """Cada test usa un archivo de log temporal aislado."""
    log_file = tmp_path / "predictions.log"
    monkeypatch.setattr(app_module, "STATS_FILE", str(log_file))
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_predecir_cubre_las_cinco_categorias():
    """
    Prueba 1: dado un grupo de parametros de entrada por categoria,
    se debe obtener la respuesta esperada del modelo. Cubre las 5
    categorias posibles, incluyendo ENFERMEDAD TERMINAL.
    """
    casos = [
        ((36.0, 0, 0), "NO ENFERMO"),
        ((37.8, 3, 4), "ENFERMEDAD LEVE"),
        ((38.7, 6, 5), "ENFERMEDAD AGUDA"),
        ((39.6, 8, 10), "ENFERMEDAD CRÓNICA"),
        ((41.0, 10, 30), "ENFERMEDAD TERMINAL"),
    ]

    for entrada, esperado in casos:
        obtenido = predecir(*entrada)
        assert obtenido == esperado, (
            f"Entrada {entrada}: esperado '{esperado}', obtenido '{obtenido}'"
        )


def test_stats_vacias_y_se_actualizan_tras_prediccion(client):
    """
    Prueba 2: antes de cualquier prediccion las estadisticas deben estar
    vacias; luego de realizar una prediccion, /stats debe reflejar el
    resultado mas reciente.
    """
    respuesta = client.get("/stats")
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert datos["total_predicciones"] == 0
    assert all(v == 0 for v in datos["total_por_categoria"].values())
    assert datos["ultimas_5"] == []
    assert datos["fecha_ultima_prediccion"] is None

    respuesta = client.post(
        "/predecir",
        data={"temperatura": "41.0", "nivel_dolor": "10", "dias_sintomas": "30"},
    )
    assert respuesta.status_code == 200

    respuesta = client.get("/stats")
    datos = respuesta.get_json()
    assert datos["total_predicciones"] == 1
    assert datos["total_por_categoria"]["ENFERMEDAD TERMINAL"] == 1
    assert len(datos["ultimas_5"]) == 1
    assert datos["ultimas_5"][0]["resultado"] == "ENFERMEDAD TERMINAL"
    assert datos["fecha_ultima_prediccion"] is not None
