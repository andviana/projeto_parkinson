-- Habilita a extensão para geração de UUID se não estiver ativa
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar ENUM para tipo de paciente
-- HC: Healthy Control (Controle Saudável)
-- PR: Prodromal (Família/Outros)
-- PD: Parkinson's Disease (Paciente de Parkinson)
CREATE TYPE tipo_paciente AS ENUM ('HC', 'PR', 'PD');

-- Tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('usuario', 'admin')),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Grupos
CREATE TABLE grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de Pacientes
CREATE TABLE pacientes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F', 'O')), -- M: Masculino, F: Feminino, O: Outro
    tipo tipo_paciente NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Vínculos com Grupos
CREATE TABLE vinculos_grupo (
    id SERIAL PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    id_grupo INT NOT NULL REFERENCES grupos(id) ON DELETE CASCADE,
    data_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    data_fim DATE,
    CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

-- Índices para otimização de pesquisas comuns
CREATE INDEX idx_pacientes_nome ON pacientes (nome_completo);
CREATE INDEX idx_vinculos_paciente ON vinculos_grupo (id_paciente);
CREATE INDEX idx_vinculos_grupo ON vinculos_grupo (id_grupo);

-- Tabelas de Exames Clínicos

-- 1. GDS (Geriatric Depression Scale)
CREATE TABLE gds (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_gds_paciente_data ON gds (id_paciente, data_exame);

-- 2. MoCA (Montreal Cognitive Assessment)
CREATE TABLE moca (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_moca_paciente_data ON moca (id_paciente, data_exame);

-- 3. SPDDS (Screening for Parkinson's Disease Cognitive Impairment)
CREATE TABLE spdds (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_spdds_paciente_data ON spdds (id_paciente, data_exame);

-- 4. UPDRS I (MDS-UPDRS Parte I - Experiências Não Motoras da Vida Diária)
CREATE TABLE updrs_i (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_updrs_i_paciente_data ON updrs_i (id_paciente, data_exame);

-- 5. UPDRS II (MDS-UPDRS Parte II - Experiências Motoras da Vida Diária)
CREATE TABLE updrs_ii (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_updrs_ii_paciente_data ON updrs_ii (id_paciente, data_exame);

-- 6. UPDRS III (MDS-UPDRS Parte III - Exame Motor)
CREATE TABLE updrs_iii (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_updrs_iii_paciente_data ON updrs_iii (id_paciente, data_exame);

-- 7. UPDRS IV (MDS-UPDRS Parte IV - Complicações Motoras)
CREATE TABLE updrs_iv (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_updrs_iv_paciente_data ON updrs_iv (id_paciente, data_exame);

-- 8. Hoehn & Yahr (Escala de Estágio de Incapacidade - aceita valores decimais como 1.5, 2.5)
CREATE TABLE hoehn_yahr (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(3,1) NOT NULL CHECK (nota_final >= 0.0 AND nota_final <= 5.0)
);
CREATE INDEX idx_hy_paciente_data ON hoehn_yahr (id_paciente, data_exame);

-- 9. Beck (Inventário de Depressão/Ansiedade de Beck)
CREATE TABLE beck (
    id_exame UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_paciente UUID NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    data_exame DATE NOT NULL DEFAULT CURRENT_DATE,
    nota_final NUMERIC(5,2) NOT NULL
);
CREATE INDEX idx_beck_paciente_data ON beck (id_paciente, data_exame);

-- 10. Tabelas de Ficha de Dados Clínicos

-- Tabela de Domínio: Sintomas Iniciais
CREATE TABLE sintomas_dominio (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela de Domínio: Localizações de Início
CREATE TABLE localizacoes_dominio (
    id SERIAL PRIMARY KEY,
    sigla VARCHAR(20) UNIQUE NOT NULL
);

-- Tabela Principal de Dados Clínicos (1:1 com Paciente)
CREATE TABLE dados_clinicos (
    id_paciente UUID PRIMARY KEY REFERENCES pacientes(id) ON DELETE CASCADE,
    tempo_inicio_sintomas_anos INT NULL,
    resposta_motora VARCHAR(50) CHECK (resposta_motora IN ('nenhuma melhora', 'pouca melhora', 'melhora parcial', 'melhora total')) NULL,
    tolerancia_levodopa VARCHAR(50) CHECK (tolerancia_levodopa IN ('sem problemas', 'teve dificuldade', 'intolerancia')) NULL,
    uso_regular_cafe BOOLEAN DEFAULT FALSE,
    frequencia_por_dia INT DEFAULT 0,
    cirurgia_dp BOOLEAN DEFAULT FALSE,
    abuso_substancia BOOLEAN DEFAULT FALSE,
    qual_substancia VARCHAR(255) NULL,
    ancestrais VARCHAR(255) NULL,
    familiar_com_dp VARCHAR(20) CHECK (familiar_com_dp IN ('sim', 'não', 'não sabe')) DEFAULT 'não',
    qual_familiar_dp VARCHAR(255) NULL,
    familiar_com_tremor VARCHAR(20) CHECK (familiar_com_tremor IN ('sim', 'não', 'não sabe')) DEFAULT 'não',
    qual_familiar_tremor VARCHAR(255) NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Relacionamento Many-to-Many: Sintomas Iniciais
CREATE TABLE dados_clinicos_sintomas (
    id_paciente UUID REFERENCES dados_clinicos(id_paciente) ON DELETE CASCADE,
    id_sintoma INT REFERENCES sintomas_dominio(id) ON DELETE CASCADE,
    PRIMARY KEY (id_paciente, id_sintoma)
);

-- Tabela de Relacionamento Many-to-Many: Localizações
CREATE TABLE dados_clinicos_localizacoes (
    id_paciente UUID REFERENCES dados_clinicos(id_paciente) ON DELETE CASCADE,
    id_localizacao INT REFERENCES localizacoes_dominio(id) ON DELETE CASCADE,
    PRIMARY KEY (id_paciente, id_localizacao)
);

-- Índices adicionais para otimização
CREATE INDEX idx_dados_clinicos_sintomas ON dados_clinicos_sintomas (id_paciente);
CREATE INDEX idx_dados_clinicos_localizacoes ON dados_clinicos_localizacoes (id_paciente);

-- Tabela Principal de Dados Complementares
CREATE TABLE dados_complementares (
    id_paciente UUID PRIMARY KEY REFERENCES pacientes(id) ON DELETE CASCADE,
    telefone VARCHAR(11) NOT NULL,
    dominio_manual VARCHAR(20) CHECK (dominio_manual IN ('destro(a)', 'sinistro(a)')) NOT NULL,
    cor VARCHAR(20) CHECK (cor IN ('pardo(a)', 'branco(a)', 'negro(a)', 'amarelo(a)')) NOT NULL,
    estado_civil VARCHAR(20) CHECK (estado_civil IN ('solteiro(a)', 'casado(a)', 'separado(a)', 'viuvo(a)', 'divorciado(a)')) NOT NULL,
    escolaridade VARCHAR(50) CHECK (escolaridade IN ('fundamental incompleto', 'fundamental completo', 'medio incompleto', 'medio completo', 'superior incompleto', 'superior completo', 'pós graduação')) NOT NULL,
    atividade_profissional VARCHAR(50) CHECK (atividade_profissional IN ('aposentado(a)', 'desempregado(a)', 'trabalhador(a) ativo(a)', 'auxilio doença', 'beneficiario(a)', 'amparo social')) NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dados_complementares_paciente ON dados_complementares (id_paciente);
