from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import exigir_role
from ..database import get_db

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.PacienteOut,
    status_code=status.HTTP_201_CREATED,
)
def criar_paciente(
    paciente_in: schemas.PacienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN, models.RoleEnum.ATENDENTE)),
):
    """
    Cria um novo paciente.
    Regra: CPF deve ser único.
    """
    existente = (
        db.query(models.Paciente)
        .filter(models.Paciente.cpf == paciente_in.cpf)
        .first()
    )
    if existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    paciente = models.Paciente(**paciente_in.dict())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.get(
    "/",
    response_model=List[schemas.PacienteOut],
)
def listar_pacientes(
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
    Lista pacientes, filtrando por ativo/inativo.
    """
    pacientes = (
        db.query(models.Paciente)
        .filter(models.Paciente.ativo == ativo)
        .all()
    )
    return pacientes


@router.get(
    "/{paciente_id}",
    response_model=schemas.PacienteOut,
)
def obter_paciente(
    paciente_id: int,
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
    Obtém um paciente pelo ID.
    """
    paciente = db.query(models.Paciente).get(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.put(
    "/{paciente_id}",
    response_model=schemas.PacienteOut,
)
def atualizar_paciente(
    paciente_id: int,
    paciente_in: schemas.PacienteUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN, models.RoleEnum.ATENDENTE)),
):
    """
    Atualiza dados de um paciente.
    """
    paciente = db.query(models.Paciente).get(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    for campo, valor in paciente_in.dict(exclude_unset=True).items():
        setattr(paciente, campo, valor)

    db.commit()
    db.refresh(paciente)
    return paciente


@router.delete(
    "/{paciente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def inativar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN)),
):
    """
    Inativa paciente (não apaga do banco).
    """
    paciente = db.query(models.Paciente).get(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    paciente.ativo = False
    db.commit()
    return
