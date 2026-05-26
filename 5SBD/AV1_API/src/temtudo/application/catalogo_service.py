from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from temtudo.infrastructure.models import CompraORM, MovimentoEstoqueORM, ProdutoORM


class CatalogoService:
    def __init__(self, session: Session):
        self.session = session

    def listar_produtos(self) -> list[ProdutoORM]:
        return list(self.session.scalars(select(ProdutoORM).order_by(ProdutoORM.sku)))

    def listar_compras(self) -> list[CompraORM]:
        return list(self.session.scalars(select(CompraORM).order_by(CompraORM.data_solicitacao.desc())))

    def listar_movimentos(self) -> list[MovimentoEstoqueORM]:
        return list(self.session.scalars(select(MovimentoEstoqueORM).order_by(MovimentoEstoqueORM.data_movimento.desc())))
