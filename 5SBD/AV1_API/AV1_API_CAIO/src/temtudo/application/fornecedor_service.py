from __future__ import annotations

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from temtudo.application.csv_parser import CsvValidationError, optional, parse_int, read_csv_bytes, required
from temtudo.infrastructure.models import EntregaFornecedorORM, ProdutoORM


class FornecedorService:
    def __init__(self, session: Session):
        self.session = session

    def importar_csv_entrega(self, content: bytes) -> dict[str, object]:
        rows = read_csv_bytes(content)
        if not rows:
            raise CsvValidationError("CSV de fornecedor sem linhas para importar.")

        lote_id = str(uuid4())
        produtos_atualizados = 0
        skus_nao_encontrados: list[str] = []

        for row in rows:
            sku = required(row, "sku")
            qtd_entregue = parse_int(optional(row, "qtd_entregue"), "qtd_entregue")

            self.session.add(
                EntregaFornecedorORM(
                    lote_id=lote_id,
                    sku=sku,
                    qtd_entregue=qtd_entregue,
                )
            )

            produto = self.session.scalar(select(ProdutoORM).where(ProdutoORM.sku == sku))
            if produto is None:
                skus_nao_encontrados.append(sku)
                continue

            produto.qtd_estoque += qtd_entregue
            produtos_atualizados += 1

        self.session.commit()
        return {
            "lote_id": lote_id,
            "linhas_importadas": len(rows),
            "produtos_atualizados": produtos_atualizados,
            "skus_nao_encontrados": skus_nao_encontrados,
        }
