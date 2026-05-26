from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from temtudo.infrastructure.database import Base


class CargaPedidoORM(Base):
    __tablename__ = "CARGA_CARG"

    id_carga: Mapped[int] = mapped_column("ID_CARGA", Integer, primary_key=True, autoincrement=True)
    lote_id: Mapped[str] = mapped_column("LOTE_ID", String(36), index=True, nullable=False)

    order_id: Mapped[str] = mapped_column("ORDER_ID", String(50), index=True, nullable=False)
    order_item_id: Mapped[str] = mapped_column("ORDER_ITEM_ID", String(50), index=True, nullable=False)
    purchase_date: Mapped[datetime | None] = mapped_column("PURCHASE_DATE", DateTime, nullable=True)
    payments_date: Mapped[datetime | None] = mapped_column("PAYMENTS_DATE", DateTime, nullable=True)
    buyer_email: Mapped[str] = mapped_column("BUYER_EMAIL", String(150), index=True, nullable=False)
    buyer_name: Mapped[str | None] = mapped_column("BUYER_NAME", String(150), nullable=True)
    cpf: Mapped[str | None] = mapped_column("CPF", String(14), nullable=True)
    buyer_phone_number: Mapped[str | None] = mapped_column("BUYER_PHONE_NUMBER", String(20), nullable=True)

    sku: Mapped[str] = mapped_column("SKU", String(50), index=True, nullable=False)
    upc: Mapped[str | None] = mapped_column("UPC", String(50), nullable=True)
    product_name: Mapped[str | None] = mapped_column("PRODUCT_NAME", String(200), nullable=True)
    quantity_purchased: Mapped[int] = mapped_column("QUANTITY_PURCHASED", Integer, nullable=False)
    currency: Mapped[str | None] = mapped_column("CURRENCY", String(10), nullable=True)
    item_price: Mapped[Decimal] = mapped_column("ITEM_PRICE", Numeric(12, 2), nullable=False)

    ship_service_level: Mapped[str | None] = mapped_column("SHIP_SERVICE_LEVEL", String(100), nullable=True)
    recipient_name: Mapped[str | None] = mapped_column("RECIPIENT_NAME", String(150), nullable=True)
    ship_address_1: Mapped[str | None] = mapped_column("SHIP_ADDRESS_1", String(200), nullable=True)
    ship_address_2: Mapped[str | None] = mapped_column("SHIP_ADDRESS_2", String(200), nullable=True)
    ship_address_3: Mapped[str | None] = mapped_column("SHIP_ADDRESS_3", String(200), nullable=True)
    ship_city: Mapped[str | None] = mapped_column("SHIP_CITY", String(100), nullable=True)
    ship_state: Mapped[str | None] = mapped_column("SHIP_STATE", String(50), nullable=True)
    ship_postal_code: Mapped[str | None] = mapped_column("SHIP_POSTAL_CODE", String(20), nullable=True)
    ship_country: Mapped[str | None] = mapped_column("SHIP_COUNTRY", String(50), nullable=True)
    ioss_number: Mapped[str | None] = mapped_column("IOSS_NUMBER", String(50), nullable=True)

    processado: Mapped[bool] = mapped_column("PROCESSADO", Boolean, nullable=False, default=False)
    data_importacao: Mapped[datetime] = mapped_column("DATA_IMPORTACAO", DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("LOTE_ID", "ORDER_ITEM_ID", name="UQ_CARGA_LOTE_ORDER_ITEM"),
    )


class EntregaFornecedorORM(Base):
    __tablename__ = "ENTREGA_ENT"

    id_entrega: Mapped[int] = mapped_column("ID_ENTREGA", Integer, primary_key=True, autoincrement=True)
    lote_id: Mapped[str] = mapped_column("LOTE_ID", String(36), index=True, nullable=False)
    sku: Mapped[str] = mapped_column("SKU", String(50), index=True, nullable=False)
    qtd_entregue: Mapped[int] = mapped_column("QTD_ENTREGUE", Integer, nullable=False)
    data_entrega: Mapped[datetime] = mapped_column("DATA_ENTREGA", DateTime, server_default=func.now())


class ClienteORM(Base):
    __tablename__ = "CLIENTES_CLI"

    id_cliente: Mapped[int] = mapped_column("ID_CLIENTE", Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str | None] = mapped_column("NOME", String(150), nullable=True)
    email: Mapped[str] = mapped_column("EMAIL", String(150), unique=True, index=True, nullable=False)
    cpf: Mapped[str | None] = mapped_column("CPF", String(14), nullable=True)
    telefone: Mapped[str | None] = mapped_column("TELEFONE", String(20), nullable=True)

    pedidos: Mapped[list[PedidoORM]] = relationship(back_populates="cliente")


class ProdutoORM(Base):
    __tablename__ = "PRODUTOS_PRD"

    id_produto: Mapped[int] = mapped_column("ID_PRODUTO", Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column("SKU", String(50), unique=True, index=True, nullable=False)
    upc: Mapped[str | None] = mapped_column("UPC", String(50), nullable=True)
    nome_produto: Mapped[str | None] = mapped_column("NOME_PRODUTO", String(200), nullable=True)
    qtd_estoque: Mapped[int] = mapped_column("QTD_ESTOQUE", Integer, nullable=False, default=0)

    itens: Mapped[list[ItemPedidoORM]] = relationship(back_populates="produto")


class PedidoORM(Base):
    __tablename__ = "PEDIDOS_PED"

    id_pedido: Mapped[str] = mapped_column("ID_PEDIDO", String(50), primary_key=True)
    data_pedido: Mapped[datetime | None] = mapped_column("DATA_PEDIDO", DateTime, nullable=True)
    data_pagamento: Mapped[datetime | None] = mapped_column("DATA_PAGAMENTO", DateTime, nullable=True)
    id_cliente: Mapped[int] = mapped_column("ID_CLIENTE", ForeignKey("CLIENTES_CLI.ID_CLIENTE"), nullable=False)
    vl_total: Mapped[Decimal] = mapped_column("VL_TOTAL", Numeric(12, 2), nullable=False)
    status: Mapped[str | None] = mapped_column("STATUS", String(20), nullable=True)

    cliente: Mapped[ClienteORM] = relationship(back_populates="pedidos")
    itens: Mapped[list[ItemPedidoORM]] = relationship(back_populates="pedido")


class ItemPedidoORM(Base):
    __tablename__ = "ITPEDIDO_ITP"

    id_item: Mapped[int] = mapped_column("ID_ITEM", Integer, primary_key=True, autoincrement=True)
    order_item_id: Mapped[str] = mapped_column("ORDER_ITEM_ID", String(50), unique=True, index=True, nullable=False)
    id_pedido: Mapped[str] = mapped_column("ID_PEDIDO", ForeignKey("PEDIDOS_PED.ID_PEDIDO"), index=True, nullable=False)
    id_produto: Mapped[int] = mapped_column("ID_PRODUTO", ForeignKey("PRODUTOS_PRD.ID_PRODUTO"), index=True, nullable=False)
    qtd: Mapped[int] = mapped_column("QTD", Integer, nullable=False)
    vl_unit: Mapped[Decimal] = mapped_column("VL_UNIT", Numeric(12, 2), nullable=False)

    pedido: Mapped[PedidoORM] = relationship(back_populates="itens")
    produto: Mapped[ProdutoORM] = relationship(back_populates="itens")

    __table_args__ = (
        UniqueConstraint("ID_PEDIDO", "ORDER_ITEM_ID", name="UQ_ITPEDIDO_PEDIDO_ORDER_ITEM"),
    )


class MovimentoEstoqueORM(Base):
    __tablename__ = "MOVIMENTO_MOV"

    id_movimento: Mapped[int] = mapped_column("ID_MOVIMENTO", Integer, primary_key=True, autoincrement=True)
    id_pedido: Mapped[str] = mapped_column("ID_PEDIDO", ForeignKey("PEDIDOS_PED.ID_PEDIDO"), index=True, nullable=False)
    id_produto: Mapped[int] = mapped_column("ID_PRODUTO", ForeignKey("PRODUTOS_PRD.ID_PRODUTO"), index=True, nullable=False)
    qtd_movimentada: Mapped[int] = mapped_column("QTD_MOVIMENTADA", Integer, nullable=False)
    estoque_antes: Mapped[int] = mapped_column("ESTOQUE_ANTES", Integer, nullable=False)
    estoque_depois: Mapped[int] = mapped_column("ESTOQUE_DEPOIS", Integer, nullable=False)
    data_movimento: Mapped[datetime] = mapped_column("DATA_MOVIMENTO", DateTime, server_default=func.now())


class CompraORM(Base):
    __tablename__ = "COMPRAS_COM"

    id_compra: Mapped[int] = mapped_column("ID_COMPRA", Integer, primary_key=True, autoincrement=True)
    id_pedido: Mapped[str] = mapped_column("ID_PEDIDO", ForeignKey("PEDIDOS_PED.ID_PEDIDO"), index=True, nullable=False)
    id_produto: Mapped[int] = mapped_column("ID_PRODUTO", ForeignKey("PRODUTOS_PRD.ID_PRODUTO"), index=True, nullable=False)
    qtd_solicitada: Mapped[int] = mapped_column("QTD_SOLICITADA", Integer, nullable=False)
    status: Mapped[str] = mapped_column("STATUS", String(20), nullable=False, default="ABERTA")
    data_solicitacao: Mapped[datetime] = mapped_column("DATA_SOLICITACAO", DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("ID_PEDIDO", "ID_PRODUTO", "STATUS", name="UQ_COMPRA_PEDIDO_PRODUTO_STATUS"),
    )
