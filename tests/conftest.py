import os
import socket
import threading
import time

import httpx
import pytest
import uvicorn


def _free_port() -> int:
    """Pega uma porta livre no loopback para evitar conflito com algo já rodando."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


# Escolhe a porta e aponta a env var ANTES de qualquer import de `server`,
# que lê STACK_SENTINEL_API no momento do import.
_PORT = _free_port()
_BASE = f"http://127.0.0.1:{_PORT}"
os.environ["STACK_SENTINEL_API"] = _BASE


@pytest.fixture(scope="session", autouse=True)
def mock_api_server():
    """Sobe a mock API (uvicorn) num thread daemon e espera ela responder."""
    from stack_sentinel.mock.api import app

    # Reafirma a base no módulo server, caso ele já tenha sido importado.
    from stack_sentinel.mcp_server import server
    server.BASE = _BASE

    config = uvicorn.Config(app, host="127.0.0.1", port=_PORT, log_level="warning")
    server_obj = uvicorn.Server(config)
    thread = threading.Thread(target=server_obj.run, daemon=True)
    thread.start()

    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            httpx.get(f"{_BASE}/services/auth/health", timeout=0.5)
            break
        except httpx.HTTPError:
            time.sleep(0.1)
    else:
        raise RuntimeError("mock API não respondeu a tempo")

    yield _BASE

    server_obj.should_exit = True
    thread.join(timeout=5)
