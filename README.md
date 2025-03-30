# Ecutando a API com docker

## Requisitos

Antes de começar, certifique-se de ter os seguintes requisitos instalados:

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- Projeto clonado em sua máquina local

## Configuração

Certifique-se de criar um arquivo .env na raiz do seu projeto seguindo o modelo de .env.example

## Executando o projeto

1. Na raiz do projeto, execute o seguinte comando para construir e iniciar os containers:
```bash
docker compose up --build -d