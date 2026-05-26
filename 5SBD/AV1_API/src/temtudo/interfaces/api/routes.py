from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from temtudo.application.catalogo_service import CatalogoService
from temtudo.application.csv_parser import CsvValidationError
from temtudo.application.fornecedor_service import FornecedorService
from temtudo.application.pedido_service import PedidoService
from temtudo.infrastructure.database import get_session
from temtudo.interfaces.api.schemas import CompraOut, MovimentoOut, PedidoOut, ProdutoOut

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/cargas/pedidos/csv", status_code=status.HTTP_201_CREATED)
async def importar_csv_pedidos(
    arquivo: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        content = await arquivo.read()
        return PedidoService(session).importar_csv_pedidos(content)
    except CsvValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/cargas/pedidos/{lote_id}/processar")
def processar_lote_pedidos(
    lote_id: str,
    session: Session = Depends(get_session),
) -> dict[str, int | str]:
    return PedidoService(session).processar_lote_pedidos(lote_id)


@router.post("/pedidos/atender")
def atender_pedidos(session: Session = Depends(get_session)) -> dict[str, int]:
    return PedidoService(session).atender_pedidos()


@router.get("/pedidos", response_model=list[PedidoOut])
def listar_pedidos(session: Session = Depends(get_session)) -> list[PedidoOut]:
    return PedidoService(session).listar_pedidos()


@router.post("/fornecedores/entregas/csv", status_code=status.HTTP_201_CREATED)
async def importar_csv_entrega_fornecedor(
    arquivo: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        content = await arquivo.read()
        return FornecedorService(session).importar_csv_entrega(content)
    except CsvValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/produtos", response_model=list[ProdutoOut])
def listar_produtos(session: Session = Depends(get_session)) -> list[ProdutoOut]:
    return CatalogoService(session).listar_produtos()


@router.get("/compras", response_model=list[CompraOut])
def listar_compras(session: Session = Depends(get_session)) -> list[CompraOut]:
    return CatalogoService(session).listar_compras()


@router.get("/movimentos", response_model=list[MovimentoOut])
def listar_movimentos(session: Session = Depends(get_session)) -> list[MovimentoOut]:
    return CatalogoService(session).listar_movimentos()
