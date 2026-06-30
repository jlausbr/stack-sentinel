import os
import re
import httpx
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

BASE = os.getenv("STACK_SENTINEL_API", "http://localhost:8001")
mcp = FastMCP("stack-sentinel")


class TicketContext(BaseModel):
    summary: str
    severity: str
    service: str
    status: str


@mcp.tool()
def fetch_ticket_context(ticket_id: str) -> TicketContext:
    """Retorna summary, severity, service e status de um ticket."""
    # Validar formato do ticket_id: TCK-\d+
    if not re.match(r"^TCK-\d+$", ticket_id):
        raise ValueError(f"formato inválido para ticket_id: {ticket_id}. Esperado: TCK-<número>")
    
    try:
        r = httpx.get(f"{BASE}/tickets/{ticket_id}", timeout=5)
        r.raise_for_status()
    except httpx.HTTPError:
        raise ValueError(f"ticket {ticket_id} indisponível")
    return TicketContext(**r.json())


if __name__ == "__main__":
    mcp.run()
