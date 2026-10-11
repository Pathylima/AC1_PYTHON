# API de Logs

## Descrição do projeto

Este projeto consiste em uma API desenvolvida em Python utilizando FastAPI. Sua finalidade é registrar e consultar mensagens de log, armazenadas em um arquivo de texto chamado `app.log`.

A API aceita três níveis de registro: INFO, WARNING e ERROR.

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- HTTPX
- pytest

## Estrutura do projeto

log_api/
├── main.py
├── log_service.py
├── requirements.txt
├── README.md
├── resultados_testes.txt
├── app.log
└── tests/
    ├── __init__.py
    ├── test_log_service_unittest.py
    └── test_api_pytest.py
    

O arquivo `app.log` será criado automaticamente quando o primeiro registro for gravado.

## Como executar o projeto

### Instalar as dependências

python -m pip install -r requirements.txt


### Iniciar a API

python -m uvicorn main:app --reload


### Acessar a documentação interativa

Com a API em execução, acesse:

http://127.0.0.1:8000/docs

## Endpoints

### POST /logs

Registra uma nova mensagem de log.

Exemplo de entrada:

json
{
  "level": "INFO",
  "message": "Cadastro concluído."
}


Resposta esperada: HTTP 201.

json
{
  "status": "registrado",
  "entry": "[INFO] Cadastro concluído."
}


Os níveis permitidos são INFO, WARNING e ERROR. A mensagem deve conter entre 1 e 200 caracteres após a remoção dos espaços externos e não pode conter quebras de linha.

### GET /logs

Consulta os registros armazenados no arquivo `app.log`.

Exemplo de resposta:

json
{
  "total": 1,
  "logs": [
    "[INFO] Cadastro concluído."
  ]
}


Se o arquivo não existir ou estiver vazio, a API deverá retornar uma lista vazia e total igual a zero.

## Armazenamento dos registros

Os registros são armazenados em arquivo de texto utilizando codificação UTF-8. As novas mensagens são acrescentadas ao final do arquivo, preservando o histórico existente.

A consulta utiliza os registros salvos no arquivo, permitindo recuperar o histórico mesmo após reiniciar a aplicação.

## Testes

O projeto contará com testes utilizando unittest e pytest.

O unittest verificará diretamente as funções de leitura e gravação de logs. O pytest verificará os endpoints da API, suas respostas, validações e tratamento de erros.

Os testes utilizarão arquivos temporários para evitar alterações no arquivo de log utilizado normalmente pela aplicação.

## Respostas às questões do projeto

### Como uma nova mensagem é acrescentada sem apagar o histórico?

A função de gravação abre o arquivo no modo `a` (append), que acrescenta o novo registro ao final do arquivo, preservando as linhas anteriores.

### Como você provou que o GET consulta o arquivo, e não apenas uma lista em memória?

A implementação do GET chama a função `read_logs`, que abre e lê o arquivo `app.log` a cada consulta. A persistência pode ser demonstrada reiniciando a aplicação e consultando novamente os registros.

### O que cada suíte verifica e como os testes evitam alaterar o log normal?

O unittest verifica as funções de leitura e gravação. O pytest verifica o comportamento dos endpoints HTTP. Ambos utilizarão arquivos temporários ou caminhos isolados para que os testes não alterem o arquivo de log normal.

## Uso de inteligência artificial

A inteligência artificial foi utilizada como ferramenta de apoio para compreender requisitos, organizar a estrutura do projeto e ajudar no desenvolvimento e na explicação do código.