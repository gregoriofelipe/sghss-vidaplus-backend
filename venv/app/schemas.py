from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr
from .models import RoleEnum, StatusConsultaEnum


# --------- Usuário / Autenticação ---------

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    role: RoleEnum


class UsuarioOut(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum
    ativo: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


# --------- Paciente ---------

class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    dados_clinicos_resumidos: Optional[str] = None


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(PacienteBase):
    pass


class PacienteOut(PacienteBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True


# --------- Profissional ---------

class ProfissionalBase(BaseModel):
    nome: str
    documento_registro: str
    especialidade: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class ProfissionalCreate(ProfissionalBase):
    pass


class ProfissionalUpdate(ProfissionalBase):
    pass


class ProfissionalOut(ProfissionalBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True


# --------- Consulta ---------

class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    observacoes: Optional[str] = None


class ConsultaCreate(ConsultaBase):
    pass


class ConsultaUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    observacoes: Optional[str] = None
    status: Optional[StatusConsultaEnum] = None


class ConsultaOut(BaseModel):
    id: int
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    status: StatusConsultaEnum
    observacoes: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
