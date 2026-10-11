
from pathlib import Path

# Caminho do arquivo de log na pasta do projeto
LOG_FILE = Path(__file__).resolve().parent / "app.log"


def write_log(entry, log_path=LOG_FILE):
    # Abre o arquivo para acrescentar uma linha
    with open(log_path, "a", encoding="utf-8") as arquivo:
        arquivo.write(entry + "\n")


def read_logs(log_path=LOG_FILE):
    # Se o arquivo ainda não existe, retorna uma lista vazia
    if not Path(log_path).exists():
        return []

    # Lê todas as linhas sem o caractere de quebra de linha
    with open(log_path, "r", encoding="utf-8") as arquivo:
        return arquivo.read().splitlines()
