SGHSS – VidaPlus 🏥

  Sistema de Gestão Hospitalar de Saúde (SGHSS) – VidaPlus é um backend em FastAPI para gestão de pacientes, profissionais de saúde e agendamento de consultas.
  O foco do projeto é demonstrar boas práticas de desenvolvimento back-end, autenticação e regras de negócio em um contexto de saúde.

✨ Funcionalidades

  Autenticação de usuários com JWT (login via e-mail e senha)
  
  Controle de acesso por papéis (roles):
  
  ADMIN, ATENDENTE, PACIENTE, PROFISSIONAL
  
  Módulo de Pacientes
  
  CRUD completo
  
  Validação de CPF único
  
  Inativação (soft delete)
  
  Módulo de Profissionais
  
  CRUD completo (restrito a ADMIN)
  
  Módulo de Consultas
  
  Agendamento de consultas entre paciente e profissional
  
  Validação de data/hora futura
  
  Bloqueio de conflito de horário para o mesmo profissional
  
  Cancelamento de consultas com regras de negócio
  
  Documentação automática da API via Swagger em /docs

🧱 Arquitetura (visão geral)
  FastAPI como framework web
  
  SQLAlchemy como ORM
  
  JWT (python-jose) para autenticação
  
  Organização em camadas:
  
  models.py – modelos de banco (SQLAlchemy)
  
  schemas.py – modelos de entrada/saída (Pydantic)
  
  routers/ – roteadores por domínio (pacientes, profissionais, consultas, auth)
  
  auth.py – regras de autenticação e autorização
  
  database.py – conexão e sessão com o banco

📂 Estrutura do projeto
    text
    sghss_backend/
    ├── app/
    │   ├── main.py              # Ponto de entrada FastAPI
    │   ├── auth.py              # Autenticação JWT e roles
    │   ├── database.py          # Conexão SQLAlchemy
    │   ├── models.py            # Modelos ORM (Usuario, Paciente, Profissional, Consulta)
    │   ├── schemas.py           # Schemas Pydantic
    │   ├── routers/
    │   │   ├── pacientes.py     # Endpoints de pacientes
    │   │   ├── profissionais.py # Endpoints de profissionais
    │   │   └── consultas.py     # Endpoints de consultas
    │   └── dependencies.py      # Dependências reutilizáveis
    ├── tests/                   # (opcional) testes automatizados
    ├── requirements.txt
    └── README.md


🚀 Como rodar o projeto
    1. Clonar o repositório
    bash
    git clone https://github.com/gregoriofelipe/sghss-vidaplus-backend.git
    cd sghss-vidaplus-backend
    2. Criar e ativar o ambiente virtual
    bash
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    # ou
    venv\Scripts\activate         # Windows
    3. Instalar dependências
    bash
    pip install -r requirements.txt
    4. Executar o servidor
    bash
    uvicorn app.main:app --reload
    A API estará disponível em:
    
    Swagger UI: http://127.0.0.1:8000/docs
    
    ReDoc: http://127.0.0.1:8000/redoc

🔐 Fluxo básico de uso
  Criar usuário ADMIN
  
  POST /auth/signup
  
  json
  {
    "email": "admin@vidaplus.com",
    "senha": "SenhaForte123",
    "role": "ADMIN"
  }
  Fazer login e obter token
  
  POST /auth/login
  (padrão OAuth2 – username = email, password = senha)
  
  Resposta:
  
  json
  {
    "access_token": "jwt_aqui",
    "token_type": "bearer"
  }
  Autorizar no Swagger
  
  Clicar em Authorize
  
  Informar: Bearer SEU_TOKEN_AQUI
  
  Consumir os endpoints protegidos
  
  Pacientes: /pacientes
  
  Profissionais: /profissionais
  
  Consultas: /consultas

🧪 Casos de teste principais
  Alguns dos casos de teste implementados/validados:
  
  CT001 – Criar usuário ADMIN (/auth/signup)
  
  CT002 – Login com credenciais válidas (/auth/login)
  
  CT004 – Criar paciente válido (/pacientes)
  
  CT006 – Listar pacientes ativos
  
  CT009 – Criar profissional de saúde (/profissionais)
  
  CT010 – Agendar consulta válida (/consultas)
  
  CT011 – Impedir conflito de horário do profissional
  
  CT012 – Cancelar consulta agendada
  

⚠️ Observações sobre segurança (LGPD)
  Este projeto tem fins acadêmicos. Para simplificar a implementação:
  
  A senha do usuário está armazenada em texto simples no banco.
  
  Não há criptografia de dados sensíveis.
  
  Em um ambiente real, seria obrigatório:
  
  Armazenar senhas com hash seguro (bcrypt/Argon2).
  
  Usar HTTPS.
  
  Implementar criptografia em repouso e logs de auditoria.
  
  Atender completamente aos requisitos da LGPD.

📄 Licença
  Projeto desenvolvido para fins educacionais.
  Sinta-se à vontade para clonar, estudar e adaptar.
