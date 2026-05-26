from temtudo.infrastructure import models as _models  # noqa: F401
from temtudo.infrastructure.database import Base, engine


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas/validadas com sucesso.")
