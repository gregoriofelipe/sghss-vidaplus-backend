from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import exigir_role
from ..database import get_db

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.ProfissionalOut,
    status_code=status.HTTP_201_CREATED,
)
def criar_profissional(
    prof_in: schemas.ProfissionalCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN)),
):
    """
    Cria um profissional de saúde.
    Apenas ADMIN pode criar.
    """
    profissional = models.Profissional(**prof_in.dict())
    db.add(profissional)
    db.commit()
    db.refresh(profissional)
    return profissional


@router.get(
    "/",
    response_model=List[schemas.ProfissionalOut],
)
def listar_profissionais(
    ativo: bool = True,
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_role(
            models.RoleEnum.ADMIN,
            models.RoleEnum.ATENDENTE,
            models.RoleEnum.MEDICO,
        )
    ),
):
    """
    Lista profissionais, filtrando por ativo/inativo.
    """
    profissionais = (
        db.query(models.Profissional)
        .filter(models.Profissional.ativo == ativo)
        .all()
    )
    return profissionais


@router.get(
    "/{profissional_id}",
    response_model=schemas.ProfissionalOut,
)
def obter_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_role(
            models.RoleEnum.ADMIN,
            models.RoleEnum.ATENDENTE,
            models.RoleEnum.MEDICO,
        )
    ),
):
    """
    Obtém um profissional pelo ID.
    """
    profissional = db.query(models.Profissional).get(profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return profissional


@router.put(
    "/{profissional_id}",
    response_model=schemas.ProfissionalOut,
)
def atualizar_profissional(
    profissional_id: int,
    prof_in: schemas.ProfissionalUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN)),
):
    """
    Atualiza dados de um profissional.
    """
    profissional = db.query(models.Profissional).get(profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    for campo, valor in prof_in.dict(exclude_unset=True).items():
        setattr(profissional, campo, valor)

    db.commit()
    db.refresh(profissional)
    return profissional


@router.delete(
    "/{profissional_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def inativar_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN)),
):
    """
    Inativa profissional (não apaga do banco).
    """
    profissional = db.query(models.Profissional).get(profissional_id)
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    profissional.ativo = False
    db.commit()
    return
