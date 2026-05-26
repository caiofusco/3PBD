class DomainError(Exception):
    """Erro de regra de negocio do dominio."""


class NotFoundError(DomainError):
    """Recurso nao encontrado."""
