from fastapi import FastAPI

# Importa os modelos para que o SQLAlchemy conheca os mapeamentos.
from temtudo.infrastructure import models as _models  # noqa: F401
from temtudo.interfaces.api.routes import router

app = FastAPI(
    title="API TemTudo - Marketplace",
    version="1.0.0",
    description="API academica em Python, FastAPI, DDD e ORM para processamento de pedidos de marketplace.",
)

app.include_router(router)
