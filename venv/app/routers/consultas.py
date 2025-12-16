from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import exigir_role
from ..database import get_db

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.ConsultaOut,
    status_code=status.HTTP_201_CREATED,
)
def agendar_consulta(
    cons_in: schemas.ConsultaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_role(models.RoleEnum.ADMIN, models.RoleEnum.ATENDENTE)),
):
    """
    Agenda uma nova consulta.
    Regras:
    - Paciente e profissional devem existir e estar ativos.
    - Não permitir duas consultas para o mesmo profissional no mesmo horário.
    """
    paciente = db.query(models.Paciente).get(cons_in.paciente_id)
    if not paciente or not paciente.ativo:
        raise HTTPException(status_code=400, detail="Paciente inválido")

    profissional = db.query(models.Profissional).get(cons_in.profissional_id)
    if not profissional or not profissional.ativo:
        raise HTTPException(status_code=400, detail="Profissional inválido")

    conflito = (
        db.query(models.Consulta)
        .filter(
            models.Consulta.profissional_id == cons_in.profissional_id,
            models.Consulta.data_hora == cons_in.data_hora,
            models.Consulta.status == models.StatusConsultaEnum.AGENDADA,
        )
        .first()
    )
    if conflito:
        raise HTTPException(
            status_code=400,
            detail="Profissional já possui consulta nesse horário",
        )

    consulta = models.Consulta(
        paciente_id=cons_in.paciente_id,
        profissional_id=cons_in.profissional_id,
        data_hora=cons_in.data_hora,
        observacoes=cons_in.observacoes,
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


@router.get(
    "/",
    response_model=List[schemas.ConsultaOut],
)
def listar_consultas(
    db: Session = Depends(get_db),
    usuario=Depends(
        exigir_role(
            models.RoleEnum.ADMIN,
            models.RoleEnum.ATENDENTE,
            models.RoleEnum.MEDICO,
        )
    ),
    paciente_id: Optional[int] = None,
    profissional_id: Optional[int] = None,
    status_consulta: Optional[models.StatusConsultaEnum] = Query(default=None),
):
    """
    Lista consultas com filtros opcionais por paciente, profissional e status.
    """
    query = db.query(models.Consulta)
    if paciente_id is not None:
        query = query.filter(models.Consulta.paciente_id == paciente_id)
    if profissional_id is not None:
        query = query.filter(models.Consulta.profissional_id == profissional_id)
    if status_consulta is not None:
        query = query.filter(models.Consulta.status == status_consulta)

    return query.all()


@router.put(
    "/{consulta_id}/cancelar",
    response_model=schemas.ConsultaOut,
)
def cancelar_consulta(
    consulta_id: int,
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
    Cancela uma consulta:
    - Só pode cancelar se estiver AGENDADA.
    - Não pode cancelar se a data/hora já passou.
    """
    consulta = db.query(models.Consulta).get(consulta_id)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    if consulta.status != models.StatusConsultaEnum.AGENDADA:
        raise HTTPException(
            status_code=400,
            detail="Apenas consultas agendadas podem ser canceladas",
        )

    if consulta.data_hora <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Não é possível cancelar consulta passada",
        )

    consulta.status = models.StatusConsultaEnum.CANCELADA
    db.commit()
    db.refresh(consulta)
    return consulta
