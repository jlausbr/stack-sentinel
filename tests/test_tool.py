import pytest
from stack_sentinel.mcp_server.server import fetch_ticket_context

def test_ticket_existente():
    ctx = fetch_ticket_context("TCK-101")
    assert ctx.severity in {"low", "medium", "high", "critical"}

def test_ticket_inexistente():
    with pytest.raises(ValueError):
        fetch_ticket_context("NAO-EXISTE")


# Testes de validação de formato
class TestTicketIdValidation:
    """Testes para validação do formato de ticket_id (TCK-\\d+)."""
    
    def test_formato_valido_padrao(self):
        """Teste com formato válido padrão (TCK-101)."""
        ctx = fetch_ticket_context("TCK-101")
        assert ctx.summary == "Login cai sob carga"
    
    def test_formato_valido_multiplos_digitos(self):
        """Teste com múltiplos dígitos (TCK-9999)."""
        # Vai falhar com 'indisponível' mas a validação de formato passa
        with pytest.raises(ValueError, match="indisponível"):
            fetch_ticket_context("TCK-9999")
    
    def test_formato_invalido_sem_prefixo_tck(self):
        """Teste com formato inválido - sem prefixo TCK."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("101")
    
    def test_formato_invalido_prefixo_incorreto(self):
        """Teste com formato inválido - prefixo incorreto."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("TICKET-101")
    
    def test_formato_invalido_sem_hifen(self):
        """Teste com formato inválido - sem hífen."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("TCK101")
    
    def test_formato_invalido_com_letras(self):
        """Teste com formato inválido - dígitos com letras."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("TCK-10A")
    
    def test_formato_invalido_minuscula(self):
        """Teste com formato inválido - prefixo em minúscula."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("tck-101")
    
    def test_formato_invalido_espaco(self):
        """Teste com formato inválido - com espaço."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("TCK - 101")
    
    def test_formato_invalido_vazio(self):
        """Teste com formato inválido - string vazia."""
        with pytest.raises(ValueError, match="formato inválido"):
            fetch_ticket_context("")

