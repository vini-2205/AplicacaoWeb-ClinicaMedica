CREATE TABLE agenda (
    codigo       NUMBER(11) NOT NULL,
    data         DATE,
    horario      DATE,
    nome         VARCHAR2(50) NOT NULL,
    email        VARCHAR2(50),
    telefone     VARCHAR2(50),
    codigomedico NUMBER(11) NOT NULL
);

ALTER TABLE agenda ADD CONSTRAINT agenda_pk PRIMARY KEY ( codigo );

CREATE TABLE enderecos (
    cep        NUMBER(8) NOT NULL,
    logradouro VARCHAR2(50) NOT NULL,
    bairro     VARCHAR2(50),
    cidade     VARCHAR2(50) NOT NULL,
    estado     VARCHAR2(50) NOT NULL
);

ALTER TABLE enderecos ADD CONSTRAINT enderecos_pk PRIMARY KEY ( cep );

CREATE TABLE funcionario (
    datacontrato DATE NOT NULL,
    salario      NUMBER(8, 2) NOT NULL,
    senhahash    VARCHAR2(50) NOT NULL,
    codigo       NUMBER(11) NOT NULL
);

ALTER TABLE funcionario ADD CONSTRAINT funcionario_pk PRIMARY KEY ( codigo );

CREATE TABLE medico (
    especialidade VARCHAR2(50) NOT NULL,
    crm           VARCHAR2(50) NOT NULL,
    codigo        NUMBER(11) NOT NULL
);

ALTER TABLE medico ADD CONSTRAINT medico_pk PRIMARY KEY ( codigo );

CREATE TABLE paciente (
    peso          NUMBER(5, 2) NOT NULL,
    altura        NUMBER(3, 2) NOT NULL,
    tiposanguineo VARCHAR2(3) NOT NULL,
    codigo        NUMBER(11) NOT NULL
);

ALTER TABLE paciente ADD CONSTRAINT paciente_pk PRIMARY KEY ( codigo );

CREATE TABLE pessoa (
    codigo   NUMBER(11) NOT NULL,
    nome     VARCHAR2(50) NOT NULL,
    email    VARCHAR2(50) NOT NULL,
    telefone VARCHAR2(50),
    cep      NUMBER(8) NOT NULL
);

ALTER TABLE pessoa ADD CONSTRAINT pessoa_pk PRIMARY KEY ( codigo );

CREATE TABLE prontuario (
    codigopaciente NUMBER(11) NOT NULL,
    anamnese       VARCHAR2(50) NOT NULL,
    medicamentos   VARCHAR2(50) NOT NULL,
    atestados      VARCHAR2(50) NOT NULL,
    exames         VARCHAR2(50) NOT NULL
);

ALTER TABLE prontuario ADD CONSTRAINT prontuario_pk PRIMARY KEY ( codigopaciente );

ALTER TABLE agenda
    ADD CONSTRAINT agenda_medico_fk FOREIGN KEY ( codigomedico )
        REFERENCES medico ( codigo )
            ON DELETE CASCADE;

ALTER TABLE funcionario
    ADD CONSTRAINT funcionario_pessoa_fk FOREIGN KEY ( codigo )
        REFERENCES pessoa ( codigo )
            ON DELETE CASCADE;

ALTER TABLE medico
    ADD CONSTRAINT medico_funcionario_fk FOREIGN KEY ( codigo )
        REFERENCES funcionario ( codigo )
            ON DELETE CASCADE;

ALTER TABLE paciente
    ADD CONSTRAINT paciente_pessoa_fk FOREIGN KEY ( codigo )
        REFERENCES pessoa ( codigo )
            ON DELETE CASCADE;

ALTER TABLE pessoa
    ADD CONSTRAINT pessoa_enderecos_fk FOREIGN KEY ( cep )
        REFERENCES enderecos ( cep );

ALTER TABLE prontuario
    ADD CONSTRAINT prontuario_paciente_fk FOREIGN KEY ( codigopaciente )
        REFERENCES paciente ( codigo )
            ON DELETE CASCADE;