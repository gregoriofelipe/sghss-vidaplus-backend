from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db
from .auth import autenticar_usuario, criar_access_token
from .routers import pacientes, profissionais, consultas

# Cria as tabelas no banco na primeira subida
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS - VidaPlus")


# ---------- Rotas de autenticação ----------

@app.post("/auth/signup", response_model=schemas.UsuarioOut, tags=["auth"])
def signup(usuario_in: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Usuario).filter(models.Usuario.email == usuario_in.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Versão simplificada: guarda a senha em texto puro
    usuario = models.Usuario(
        email=usuario_in.email,
        senha_hash=usuario_in.senha,  # aqui não está mais com hash
        role=usuario_in.role,
        ativo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@app.post("/auth/login", response_model=schemas.Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )
    access_token = criar_access_token(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- Routers de domínio ----------

app.include_router(pacientes.router, prefix="/pacientes", tags=["pacientes"])
app.include_router(profissionais.router, prefix="/profissionais", tags=["profissionais"])
app.include_router(consultas.router, prefix="/consultas", tags=["consultas"])
