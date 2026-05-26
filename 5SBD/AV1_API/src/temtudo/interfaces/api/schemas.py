from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProdutoOut(BaseModel):
    id_produto: int
    sku: str
    upc: str | None = None
    nome_produto: str | None = None
    qtd_estoque: int

    model_config = ConfigDict(from_attributes=True)


class PedidoOut(BaseModel):
    id_pedido: str
    data_pedido: datetime | None = None
    data_pagamento: datetime | None = None
    id_cliente: int
    vl_total: Decimal
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CompraOut(BaseModel):
    id_compra: int
    id_pedido: str
    id_produto: int
    qtd_solicitada: int
    status: str
    data_solicitacao: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class MovimentoOut(BaseModel):
    id_movimento: int
    id_pedido: str
    id_produto: int
    qtd_movimentada: int
    estoque_antes: int
    estoque_depois: int
    data_movimento: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
