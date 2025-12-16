from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ajuste a URL se o usuário/senha/banco forem diferentes
DATABASE_URL = "postgresql+psycopg2://sghss_user:sghss_pass@localhost:5432/sghss"

# echo=True mostra os SQLs no terminal, ajuda no desenvolvimento
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency para FastAPI injetar a sessão de banco em cada requisição.
    Fecha a sessão automaticamente no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
