# stack-sentinel

Hub de investigação técnica para devs. Parte 1: serviço mockado (FastAPI),
uma tool tipada (`fetch_ticket_context`) e um MCP Server mínimo expondo essa tool.

## Rodar

```bash
uv run uvicorn stack_sentinel.mock.api:app --port 8001   # sobe a mock API
uv run mcp dev src/stack_sentinel/mcp_server/server.py   # abre o MCP Inspector pra chamar a tool
uv run pytest                                            # roda os testes
```

Os testes sobem a mock API sozinhos (uvicorn em background), então
`uv run pytest` passa verde sem precisar subir nada manualmente.

A base da API usada pela tool vem de `STACK_SENTINEL_API`
(default `http://localhost:8001`).

## Documentação da API

Após rodar `uv run uvicorn stack_sentinel.mock.api:app --port 8001`, acesse:

- **Swagger UI (OpenAPI)**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc