# Projeto Parkinson - Instituto Viva

Este é o sistema de prontuários clínicos e registro de avaliações clínicas desenvolvido para o **Instituto Viva**. A aplicação é estruturada em Python Flask, com estilização em Bootstrap 5, e banco de dados PostgreSQL integrado nativamente via API oficial do **Supabase**.

---

## 🛠️ Arquitetura e Estrutura do Projeto

O sistema foi refatorado seguindo o padrão de arquitetura em camadas para facilitar manutenções futuras e escalabilidade:

```
parkinson/
├── app.py                 # Fábrica da aplicação Flask e rotas centrais (Dashboard)
├── app_decorators.py      # Decoradores de permissões (ex: @admin_required)
├── build.sh               # Script de compilação automatizado para o Render
├── config.py              # Configurações do Flask e leitura de variáveis de ambiente
├── db.py                  # Inicializador do Cliente do Supabase (com Mock local automático)
├── requirements.txt       # Dependências de produção (gunicorn, supabase, python-dotenv)
├── seed_db.py             # Script de inicialização (Seed) para inserção de dados e usuários padrão
├── supabase_mock.py       # Emulador local do Supabase sobre SQLite (para desenvolvimento offline)
├── wsgi.py                # Ponto de entrada do servidor Gunicorn
├── blueprints/            # Roteadores encapsulados
│   ├── auth.py            # Autenticação e Gestão de Usuários
│   ├── exames.py          # Lançamento rápido de escalas
│   ├── grupos.py          # Cadastro e visualização de Grupos de Atividade
│   └── pacientes.py       # Gestão de prontuários e vínculos
├── models/                # Camada de Persistência (Modelos/Repositórios)
│   ├── exam_repo.py
│   ├── group_repo.py
│   ├── patient_repo.py
│   └── user_repo.py
├── services/              # Camada de Regras de Negócio (Serviços)
│   ├── auth_service.py
│   ├── exam_service.py
│   ├── group_service.py
│   └── patient_service.py
├── static/                # Arquivos estáticos (style.css, main.js)
└── templates/             # Arquivos HTML do Jinja2
```

---

## 💾 Scripts SQL de Criação no Supabase (PostgreSQL)

Caso precise recriar ou inicializar as tabelas no painel do Supabase, execute o seguinte script SQL no **SQL Editor** do Supabase:

```sql
-- 1. Tabela de Usuários do Sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'usuario', -- 'admin' ou 'usuario'
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Grupos de Atividades
CREATE TABLE IF NOT EXISTS grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) UNIQUE NOT NULL
);

-- 3. Tabela de Pacientes (Prontuário Central)
CREATE TABLE IF NOT EXISTS pacientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
    tipo VARCHAR(2) NOT NULL CHECK (tipo IN ('HC', 'PR', 'PD')), -- PD (Parkinson), HC (Controle), PR (Prodromal)
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela de Vínculos com Grupos (Histórico de Participações)
CREATE TABLE IF NOT EXISTS vinculos_grupo (
    id SERIAL PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    id_grupo INTEGER NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
    data_inicio DATE NOT NULL,
    data_fim DATE NULL,
    CONSTRAINT chk_datas_vinculo CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

-- 5. Tabelas de Exames Clínicos
CREATE TABLE IF NOT EXISTS gds (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS moca (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS spdds (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS updrs_i (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS updrs_ii (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS updrs_iii (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS updrs_iv (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS hoehn_yahr (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS beck (
    id_exame UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL,
    nota_final NUMERIC NOT NULL
);
```

---

## 🚀 Como Executar Localmente

### 1. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto (copie o modelo de `.env.example`) e configure suas chaves do Supabase. 
> Se as variáveis `SUPABASE_URL` e `SUPABASE_KEY` forem mantidas vazias ou ausentes, o sistema ativará automaticamente o **Modo de Simulação Offline (SQLite)**, criando e semeando o banco local `parkinson_local.db`.

Exemplo de conteúdo para o `.env`:
```env
SECRET_KEY=sua_chave_secreta_flask_aqui
SUPABASE_URL=https://sua-url-do-supabase.supabase.co
SUPABASE_KEY=sua-chave-anon-key-do-supabase
```

### 2. Semeando o Banco de Dados (Seed)
Execute o script independente para popular dados básicos e registrar o administrador inicial do sistema:
```bash
python3 seed_db.py
```
Esse script criará:
- Um usuário Administrador: **admin** / **Institutoviv@** (senha criptografada).
- Um usuário Clínico Comum de testes: **clinico** / **clinico**.
- 3 Grupos de atividade padrão.

### 3. Executando o Servidor Local
Para executar no modo de desenvolvimento tradicional:
```bash
python3 app.py
```
O servidor estará acessível em `http://localhost:5000`.

Para rodar localmente utilizando o Gunicorn (idêntico à produção):
```bash
gunicorn -w 4 -b 0.0.0.0:5005 wsgi:app
```
O servidor estará acessível em `http://localhost:5005`.

---

## ☁️ Instruções de Deploy no Render

Para hospedar a aplicação no Render conectando com o banco de dados do Supabase:

1. **Criar um Novo Web Service** no painel do Render.
2. **Vincular o repositório Git** onde o código da aplicação está hospedado.
3. Configure as propriedades básicas do serviço:
   - **Environment/Language**: `Python`
   - **Branch**: `main` (ou de sua preferência)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app`
4. Na aba **Environment Variables**, adicione as seguintes variáveis obrigatórias:
   - `SECRET_KEY`: Uma sequência de caracteres aleatórios para proteger as sessões.
   - `SUPABASE_URL`: A URL do seu projeto no Supabase (encontrada em Settings > API).
   - `SUPABASE_KEY`: A Anon Key pública do seu projeto no Supabase.
5. Clique em **Deploy Web Service**.
6. Após a conclusão bem-sucedida do deploy, execute o semeamento de banco de dados rodando um script manual na aba **Shell** do Render ou temporariamente no build command (se desejado). Exemplo de comando no Shell do Render:
   ```bash
   python seed_db.py
   ```
   *Isso garantirá a presença do usuário administrador inicial no banco do Supabase.*
