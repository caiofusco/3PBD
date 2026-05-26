from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Select, and_, asc, desc, func, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from temtudo.application.csv_parser import (
    CsvValidationError,
    optional,
    parse_datetime,
    parse_decimal,
    parse_int,
    read_csv_bytes,
    required,
)
from temtudo.domain.status import CompraStatus, PedidoStatus
from temtudo.infrastructure.models import (
    CargaPedidoORM,
    ClienteORM,
    CompraORM,
    ItemPedidoORM,
    MovimentoEstoqueORM,
    PedidoORM,
    ProdutoORM,
)
from temtudo.settings import settings


class PedidoService:
    def __init__(self, session: Session):
        self.session = session

    def importar_csv_pedidos(self, content: bytes) -> dict[str, object]:
        rows = read_csv_bytes(content)
        if not rows:
            raise CsvValidationError("CSV sem linhas para importar.")

        lote_id = str(uuid4())
        for row in rows:
            carga = CargaPedidoORM(
                lote_id=lote_id,
                order_id=required(row, "order-id"),
                order_item_id=required(row, "order-item-id"),
                purchase_date=parse_datetime(optional(row, "purchase-date"), "purchase-date"),
                payments_date=parse_datetime(optional(row, "payments-date"), "payments-date"),
                buyer_email=required(row, "buyer-email"),
                buyer_name=optional(row, "buyer-name"),
                cpf=optional(row, "cpf"),
                buyer_phone_number=optional(row, "buyer-phone-number"),
                sku=required(row, "sku"),
                upc=optional(row, "upc"),
                product_name=optional(row, "product-name"),
                quantity_purchased=parse_int(optional(row, "quantity-purchased"), "quantity-purchased"),
                currency=optional(row, "currency"),
                item_price=parse_decimal(optional(row, "item-price"), "item-price"),
                ship_service_level=optional(row, "ship-service-level"),
                recipient_name=optional(row, "recipient-name"),
                ship_address_1=optional(row, "ship-address-1"),
                ship_address_2=optional(row, "ship-address-2"),
                ship_address_3=optional(row, "ship-address-3"),
                ship_city=optional(row, "ship-city"),
                ship_state=optional(row, "ship-state"),
                ship_postal_code=optional(row, "ship-postal-code"),
                ship_country=optional(row, "ship-country"),
                ioss_number=optional(row, "ioss-number"),
            )
            self.session.add(carga)

        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise CsvValidationError(
                "O CSV possui item de pedido duplicado dentro do mesmo lote. "
                "Verifique a coluna order-item-id."
            ) from exc

        return {"lote_id": lote_id, "linhas_importadas": len(rows)}

    def processar_lote_pedidos(self, lote_id: str) -> dict[str, int | str]:
        cargas = list(
            self.session.scalars(
                select(CargaPedidoORM)
                .where(CargaPedidoORM.lote_id == lote_id, CargaPedidoORM.processado == 0)
                .order_by(CargaPedidoORM.order_id, CargaPedidoORM.order_item_id)
            )
        )
        if not cargas:
            return {
                "lote_id": lote_id,
                "linhas_processadas": 0,
                "clientes_criados": 0,
                "produtos_criados": 0,
                "pedidos_criados": 0,
                "itens_criados": 0,
            }

        clientes_criados = self._criar_clientes_inexistentes(cargas)
        produtos_criados = self._criar_produtos_inexistentes(cargas)
        pedidos_criados = self._criar_pedidos_inexistentes(cargas)
        itens_criados = self._criar_itens_inexistentes(cargas)

        for carga in cargas:
            carga.processado = True

        self.session.commit()
        return {
            "lote_id": lote_id,
            "linhas_processadas": len(cargas),
            "clientes_criados": clientes_criados,
            "produtos_criados": produtos_criados,
            "pedidos_criados": pedidos_criados,
            "itens_criados": itens_criados,
        }

    def atender_pedidos(self) -> dict[str, int]:
        pedidos = list(
            self.session.scalars(
                select(PedidoORM)
                .where(or_(PedidoORM.status.is_(None), PedidoORM.status == PedidoStatus.PENDENTE.value))
                .order_by(desc(PedidoORM.vl_total), asc(PedidoORM.data_pedido))
            )
        )

        atendidos = 0
        pendentes = 0
        movimentos = 0
        compras_criadas = 0

        for pedido in pedidos:
            itens = list(
                self.session.scalars(
                    select(ItemPedidoORM).where(ItemPedidoORM.id_pedido == pedido.id_pedido)
                )
            )
            if not itens:
                continue

            qtd_por_produto: dict[int, int] = defaultdict(int)
            for item in itens:
                qtd_por_produto[item.id_produto] += item.qtd

            produtos = {
                produto.id_produto: produto
                for produto in self.session.scalars(
                    select(ProdutoORM).where(ProdutoORM.id_produto.in_(qtd_por_produto.keys()))
                )
            }

            faltas: dict[int, int] = {}
            for id_produto, qtd_necessaria in qtd_por_produto.items():
                produto = produtos[id_produto]
                if produto.qtd_estoque < qtd_necessaria:
                    faltas[id_produto] = qtd_necessaria - produto.qtd_estoque

            if faltas:
                pendentes += 1
                pedido.status = PedidoStatus.PENDENTE.value
                for id_produto, qtd_faltante in faltas.items():
                    compra_existente = self.session.scalar(
                        select(CompraORM).where(
                            CompraORM.id_pedido == pedido.id_pedido,
                            CompraORM.id_produto == id_produto,
                            CompraORM.status == CompraStatus.ABERTA.value,
                        )
                    )
                    if compra_existente is None:
                        self.session.add(
                            CompraORM(
                                id_pedido=pedido.id_pedido,
                                id_produto=id_produto,
                                qtd_solicitada=qtd_faltante,
                                status=CompraStatus.ABERTA.value,
                            )
                        )
                        compras_criadas += 1
                continue

            for item in itens:
                produto = produtos[item.id_produto]
                estoque_antes = produto.qtd_estoque
                estoque_depois = estoque_antes - item.qtd
                self.session.add(
                    MovimentoEstoqueORM(
                        id_pedido=pedido.id_pedido,
                        id_produto=item.id_produto,
                        qtd_movimentada=item.qtd,
                        estoque_antes=estoque_antes,
                        estoque_depois=estoque_depois,
                    )
                )
                produto.qtd_estoque = estoque_depois
                movimentos += 1

            pedido.status = PedidoStatus.ATENDIDO.value
            self.session.execute(
                update(CompraORM)
                .where(
                    CompraORM.id_pedido == pedido.id_pedido,
                    CompraORM.status == CompraStatus.ABERTA.value,
                )
                .values(status=CompraStatus.ATENDIDA.value)
            )
            atendidos += 1

        self.session.commit()
        return {
            "pedidos_avaliados": len(pedidos),
            "pedidos_atendidos": atendidos,
            "pedidos_pendentes": pendentes,
            "movimentos_criados": movimentos,
            "compras_criadas": compras_criadas,
        }

    def listar_pedidos(self) -> list[PedidoORM]:
        return list(self.session.scalars(select(PedidoORM).order_by(desc(PedidoORM.vl_total))))

    def _criar_clientes_inexistentes(self, cargas: list[CargaPedidoORM]) -> int:
        emails = {c.buyer_email for c in cargas if c.buyer_email}
        existentes = set(
            self.session.scalars(select(ClienteORM.email).where(ClienteORM.email.in_(emails)))
        )

        criados = 0
        vistos: set[str] = set()
        for carga in cargas:
            if carga.buyer_email in existentes or carga.buyer_email in vistos:
                continue
            self.session.add(
                ClienteORM(
                    nome=carga.buyer_name,
                    email=carga.buyer_email,
                    cpf=carga.cpf,
                    telefone=carga.buyer_phone_number,
                )
            )
            vistos.add(carga.buyer_email)
            criados += 1
        self.session.flush()
        return criados

    def _criar_produtos_inexistentes(self, cargas: list[CargaPedidoORM]) -> int:
        skus = {c.sku for c in cargas if c.sku}
        existentes = set(self.session.scalars(select(ProdutoORM.sku).where(ProdutoORM.sku.in_(skus))))

        criados = 0
        vistos: set[str] = set()
        for carga in cargas:
            if carga.sku in existentes or carga.sku in vistos:
                continue
            self.session.add(
                ProdutoORM(
                    sku=carga.sku,
                    upc=carga.upc,
                    nome_produto=carga.product_name,
                    qtd_estoque=settings.initial_stock_default,
                )
            )
            vistos.add(carga.sku)
            criados += 1
        self.session.flush()
        return criados

    def _criar_pedidos_inexistentes(self, cargas: list[CargaPedidoORM]) -> int:
        pedidos_por_id: dict[str, list[CargaPedidoORM]] = defaultdict(list)
        for carga in cargas:
            pedidos_por_id[carga.order_id].append(carga)

        existentes = set(
            self.session.scalars(
                select(PedidoORM.id_pedido).where(PedidoORM.id_pedido.in_(pedidos_por_id.keys()))
            )
        )
        clientes = {
            cliente.email: cliente
            for cliente in self.session.scalars(
                select(ClienteORM).where(
                    ClienteORM.email.in_({c.buyer_email for c in cargas if c.buyer_email})
                )
            )
        }

        criados = 0
        for order_id, linhas in pedidos_por_id.items():
            if order_id in existentes:
                continue
            primeira_linha = linhas[0]
            total = sum(
                Decimal(linha.quantity_purchased) * Decimal(linha.item_price)
                for linha in linhas
            )
            datas_pedido = [linha.purchase_date for linha in linhas if linha.purchase_date is not None]
            datas_pagamento = [linha.payments_date for linha in linhas if linha.payments_date is not None]

            self.session.add(
                PedidoORM(
                    id_pedido=order_id,
                    data_pedido=min(datas_pedido) if datas_pedido else None,
                    data_pagamento=max(datas_pagamento) if datas_pagamento else None,
                    id_cliente=clientes[primeira_linha.buyer_email].id_cliente,
                    vl_total=total,
                    status=None,
                )
            )
            criados += 1
        self.session.flush()
        return criados

    def _criar_itens_inexistentes(self, cargas: list[CargaPedidoORM]) -> int:
        order_item_ids = {c.order_item_id for c in cargas if c.order_item_id}
        existentes = set(
            self.session.scalars(
                select(ItemPedidoORM.order_item_id).where(ItemPedidoORM.order_item_id.in_(order_item_ids))
            )
        )
        produtos = {
            produto.sku: produto
            for produto in self.session.scalars(
                select(ProdutoORM).where(ProdutoORM.sku.in_({c.sku for c in cargas if c.sku}))
            )
        }

        criados = 0
        for carga in cargas:
            if carga.order_item_id in existentes:
                continue
            self.session.add(
                ItemPedidoORM(
                    order_item_id=carga.order_item_id,
                    id_pedido=carga.order_id,
                    id_produto=produtos[carga.sku].id_produto,
                    qtd=carga.quantity_purchased,
                    vl_unit=carga.item_price,
                )
            )
            criados += 1
        self.session.flush()
        return criados
