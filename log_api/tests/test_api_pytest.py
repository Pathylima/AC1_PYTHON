
import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Cada teste utiliza seu próprio arquivo de log
    arquivo_teste = tmp_path / "app.log"

    monkeypatch.setattr(main, "LOG_FILE", arquivo_teste)

    return TestClient(main.app)


def test_get_inicial_retorna_lista_vazia(client):
    resposta = client.get("/logs")

    assert resposta.status_code == 200
    assert resposta.json() == {"total": 0, "logs": []}


def test_post_registra_mensagem(client):
    resposta = client.post(
        "/logs",
        json={"level": "INFO", "message": "Cadastro concluído."}
    )

    assert resposta.status_code == 201
    assert resposta.json() == {
        "status": "registrado",
        "entry": "[INFO] Cadastro concluído."
    }

    assert main.LOG_FILE.read_text(encoding="utf-8") == (
        "[INFO] Cadastro concluído.\n"
    )


def test_get_retorna_registros_em_ordem(client):
    client.post(
        "/logs",
        json={"level": "INFO", "message": "Primeiro"}
    )
    client.post(
        "/logs",
        json={"level": "WARNING", "message": "Segundo"}
    )

    resposta = client.get("/logs")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "total": 2,
        "logs": ["[INFO] Primeiro", "[WARNING] Segundo"]
    }


def test_post_aceita_mensagem_duplicada(client):
    dados = {"level": "INFO", "message": "Repetido"}

    primeira = client.post("/logs", json=dados)
    segunda = client.post("/logs", json=dados)

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert client.get("/logs").json()["total"] == 2


@pytest.mark.parametrize(
    "mensagem",
    [
        "",
        "   ",
        None,
        123,
        "linha 1\nlinha 2",
        "linha 1\rlinha 2",
        "a" * 201,
    ],
)
def test_post_rejeita_mensagens_invalidas(client, mensagem):
    resposta = client.post(
        "/logs",
        json={"level": "INFO", "message": mensagem}
    )

    assert resposta.status_code == 422
    assert not main.LOG_FILE.exists()


@pytest.mark.parametrize("tamanho", [1, 200])
def test_post_aceita_limites_de_caracteres(client, tamanho):
    mensagem = "a" * tamanho

    resposta = client.post(
        "/logs",
        json={"level": "INFO", "message": mensagem}
    )

    assert resposta.status_code == 201


def test_post_remove_espacos_externos(client):
    resposta = client.post(
        "/logs",
        json={"level": "INFO", "message": "  Olá mundo  "}
    )

    assert resposta.status_code == 201
    assert resposta.json()["entry"] == "[INFO] Olá mundo"


@pytest.mark.parametrize("nivel", ["DEBUG", "info", "error"])
def test_post_rejeita_nivel_invalido(client, nivel):
    resposta = client.post(
        "/logs",
        json={"level": nivel, "message": "Teste"}
    )

    assert resposta.status_code == 422
    assert not main.LOG_FILE.exists()


@pytest.mark.parametrize(
    "dados",
    [
        {"message": "Teste"},
        {"level": "INFO"},
    ],
)
def test_post_rejeita_campos_obrigatorios_ausentes(client, dados):
    resposta = client.post("/logs", json=dados)

    assert resposta.status_code == 422
    assert not main.LOG_FILE.exists()


def test_get_nao_modifica_arquivo(client):
    client.post(
        "/logs",
        json={"level": "INFO", "message": "Registro"}
    )

    conteudo_antes = main.LOG_FILE.read_bytes()

    resposta = client.get("/logs")

    conteudo_depois = main.LOG_FILE.read_bytes()

    assert resposta.status_code == 200
    assert conteudo_depois == conteudo_antes
