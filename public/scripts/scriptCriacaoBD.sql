CREATE TABLE agenda (
    codigo       INT NOT NULL,
    data         DATE,
    horario      DATE,
    nome         VARCHAR(50) NOT NULL,
    email        VARCHAR(50),
    telefone     VARCHAR(50),
    codigomedico INT NOT NULL
);

ALTER TABLE agenda ADD CONSTRAINT agenda_pk PRIMARY KEY (codigo);

CREATE TABLE enderecos (
    cep        INT NOT NULL,
    logradouro VARCHAR(50) NOT NULL,
    bairro     VARCHAR(50),
    cidade     VARCHAR(50) NOT NULL,
    estado     VARCHAR(50) NOT NULL
);

ALTER TABLE enderecos ADD CONSTRAINT enderecos_pk PRIMARY KEY (cep);

CREATE TABLE funcionario (
    datacontrato DATE NOT NULL,
    salario      INT NOT NULL,
    senhahash    VARCHAR(50) NOT NULL,
    codigo       INT NOT NULL
);

ALTER TABLE funcionario ADD CONSTRAINT funcionario_pk PRIMARY KEY (codigo);

CREATE TABLE medico (
    especialidade VARCHAR(50) NOT NULL,
    crm           VARCHAR(50) NOT NULL,
    codigo        INT NOT NULL
);

ALTER TABLE medico ADD CONSTRAINT medico_pk PRIMARY KEY (codigo);

CREATE TABLE paciente (
    peso          INT NOT NULL,
    altura        INT NOT NULL,
    tiposanguineo VARCHAR(3) NOT NULL,
    codigo        INT NOT NULL
);

ALTER TABLE paciente ADD CONSTRAINT paciente_pk PRIMARY KEY (codigo);

CREATE TABLE pessoa (
    codigo   INT NOT NULL,
    nome     VARCHAR(50) NOT NULL,
    email    VARCHAR(50) NOT NULL,
    telefone VARCHAR(50),
    cep      INT NOT NULL
);

ALTER TABLE pessoa ADD CONSTRAINT pessoa_pk PRIMARY KEY (codigo);

CREATE TABLE prontuario (
    codigopaciente INT NOT NULL,
    anamnese       VARCHAR(50) NOT NULL,
    medicamentos   VARCHAR(50) NOT NULL,
    atestados      VARCHAR(50) NOT NULL,
    exames         VARCHAR(50) NOT NULL
);

ALTER TABLE prontuario ADD CONSTRAINT prontuario_pk PRIMARY KEY (codigopaciente);

ALTER TABLE agenda
    ADD CONSTRAINT agenda_medico_fk FOREIGN KEY (codigomedico)
        REFERENCES medico (codigo)
            ON DELETE CASCADE;

ALTER TABLE funcionario
    ADD CONSTRAINT funcionario_pessoa_fk FOREIGN KEY (codigo)
        REFERENCES pessoa (codigo)
            ON DELETE CASCADE;

ALTER TABLE medico
    ADD CONSTRAINT medico_funcionario_fk FOREIGN KEY (codigo)
        REFERENCES funcionario (codigo)
            ON DELETE CASCADE;

ALTER TABLE paciente
    ADD CONSTRAINT paciente_pessoa_fk FOREIGN KEY (codigo)
        REFERENCES pessoa (codigo)
            ON DELETE CASCADE;

ALTER TABLE pessoa
    ADD CONSTRAINT pessoa_enderecos_fk FOREIGN KEY (cep)
        REFERENCES enderecos (cep);

ALTER TABLE prontuario
    ADD CONSTRAINT prontuario_paciente_fk FOREIGN KEY (codigopaciente)
        REFERENCES paciente (codigo)
            ON DELETE CASCADE;
