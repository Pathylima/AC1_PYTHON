
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from log_service import LOG_FILE, write_log, read_logs

# Cria a aplicação
app = FastAPI()


# Define os dados que a API aceita
class LogEntry(BaseModel):
    level: Literal["INFO", "WARNING", "ERROR"]
    message: str

    @field_validator("message", mode="before")
    @classmethod
    def validate_message(cls, value):
        # Não permite valores que não sejam texto
        if not isinstance(value, str):
            raise ValueError("A mensagem deve ser um texto.")

        # Não permite quebras de linha
        if "\n" in value or "\r" in value:
            raise ValueError("A mensagem não pode ter quebras de linha.")

        # Remove os espaços das extremidades
        value = value.strip()

        # Exige entre 1 e 200 caracteres
        if not 1 <= len(value) <= 200:
            raise ValueError(
                "A mensagem deve ter entre 1 e 200 caracteres."
            )

        return value


# Endpoint para registrar uma mensagem
@app.post("/logs", status_code=201)
def create_log(data: LogEntry):
    entry = f"[{data.level}] {data.message}"

    try:
        write_log(entry, log_path=LOG_FILE)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível gravar o log."
        )

    return {
        "status": "registrado",
        "entry": entry
    }


# Endpoint para consultar as mensagens
@app.get("/logs")
def get_logs():
    try:
        logs = read_logs(log_path=LOG_FILE)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível ler o log."
        )

    return {
        "total": len(logs),
        "logs": logs
    }
