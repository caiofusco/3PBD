from enum import Enum


class PedidoStatus(str, Enum):
    ATENDIDO = "ATENDIDO"
    PENDENTE = "PENDENTE"


class CompraStatus(str, Enum):
    ABERTA = "ABERTA"
    ATENDIDA = "ATENDIDA"
