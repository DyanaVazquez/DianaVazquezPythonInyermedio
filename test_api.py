"""Contrato de la actividad: se aplica a la referencia o a la práctica."""

import importlib
import os
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

api = importlib.import_module(os.environ.get("API_MODULO", "main"))
datos_iniciales = deepcopy(api.libros)


@pytest.fixture
def client():
    # Cada prueba comienza con los mismos datos, sin depender de las anteriores.
    api.libros[:] = deepcopy(datos_iniciales)
    with TestClient(api.app) as cliente:
        yield cliente
    api.libros[:] = deepcopy(datos_iniciales)


def test_inicio(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["documentacion"] == "/docs"


def test_listar_libros(client):
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200
    assert [libro["id"] for libro in respuesta.json()] == [1, 2, 3]


def test_filtrar_antes_de_limitar(client):
    respuesta = client.get("/libros", params={"q": "PYTHON", "limite": 1})
    assert respuesta.status_code == 200
    assert [libro["id"] for libro in respuesta.json()] == [2]


def test_busqueda_sin_coincidencias(client):
    respuesta = client.get("/libros", params={"q": "inexistente"})
    assert respuesta.status_code == 200
    assert respuesta.json() == []


@pytest.mark.parametrize("consulta", [
    {"limite": 0}, {"limite": 21}, {"limite": "abc"},
    {"q": ""}, {"q": "a" * 51},
])
def test_validacion_query(client, consulta):
    respuesta = client.get("/libros", params=consulta)
    assert respuesta.status_code == 422
    assert respuesta.json()["detail"][0]["loc"][0] == "query"


def test_obtener_libro(client):
    respuesta = client.get("/libros/2")
    assert respuesta.status_code == 200
    assert respuesta.json() == datos_iniciales[1]


def test_libro_inexistente(client):
    respuesta = client.get("/libros/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Libro no encontrado"


@pytest.mark.parametrize("libro_id", ["abc", "0", "-1"])
def test_validacion_path(client, libro_id):
    respuesta = client.get(f"/libros/{libro_id}")
    assert respuesta.status_code == 422
    assert respuesta.json()["detail"][0]["loc"][0] == "path"


def test_crear_y_consultar_libros(client):
    cuerpo = {"titulo": "Nuevo libro", "autor": "Estudiante", "paginas": 120}
    primero = client.post("/libros", json=cuerpo)
    segundo = client.post("/libros", json=cuerpo)
    assert primero.status_code == segundo.status_code == 201
    assert primero.json() == {"id": 4, **cuerpo}
    assert segundo.json()["id"] == 5
    assert client.get("/libros/4").json() == primero.json()
    assert len(client.get("/libros").json()) == 5


@pytest.mark.parametrize("cambio", [
    {"titulo": ""}, {"titulo": "a" * 101},
    {"autor": ""}, {"autor": "a" * 81},
    {"paginas": 0}, {"paginas": -1}, {"paginas": 2001}, {"paginas": "abc"},
])
def test_validacion_body(client, cambio):
    cuerpo = {"titulo": "Válido", "autor": "Ana", "paginas": 100, **cambio}
    respuesta = client.post("/libros", json=cuerpo)
    assert respuesta.status_code == 422
    assert respuesta.json()["detail"][0]["loc"][0] == "body"
    assert len(client.get("/libros").json()) == 3


def test_campos_obligatorios(client):
    respuesta = client.post("/libros", json={})
    assert respuesta.status_code == 422
    assert {error["loc"][-1] for error in respuesta.json()["detail"]} == {
        "titulo", "autor", "paginas",
    }


def test_limites_validos(client):
    respuesta = client.post("/libros", json={
        "titulo": "a" * 100, "autor": "b" * 80, "paginas": 2000,
    })
    assert respuesta.status_code == 201
    assert client.get("/libros", params={"limite": 20}).status_code == 200
