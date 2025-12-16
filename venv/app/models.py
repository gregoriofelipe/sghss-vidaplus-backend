from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base
import enum


# --------- Enums de papéis e status ---------

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MEDICO = "MEDICO"
    ATENDENTE = "ATENDENTE"
    PACIENTE = "PACIENTE"


class StatusConsultaEnum(str, enum.Enum):
    AGENDADA = "AGENDADA"
    CANCELADA = "CANCELADA"
    REALIZADA = "REALIZADA"


# --------- Usuário (Autenticação / Autorização) ---------

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)


# --------- Paciente ---------

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    endereco = Column(String(255), nullable=True)
    dados_clinicos_resumidos = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    consultas = relationship("Consulta", back_populates="paciente")


# --------- Profissional de Saúde ---------

class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    documento_registro = Column(String(30), nullable=False)  # CRM, COREN, etc.
    especialidade = Column(String(120), nullable=True)
    email = Column(String(120), nullable=True)
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)

    consultas = relationship("Consulta", back_populates="profissional")


# --------- Consulta ---------

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(Enum(StatusConsultaEnum),
                    default=StatusConsultaEnum.AGENDADA,
                    nullable=False)
    observacoes = Column(String(500), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    paciente = relationship("Paciente", back_populates="consultas")
    profissional = relationship("Profissional", back_populates="consultas")
