import mysql.connector

meubd = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root000"
)

mycursor = meubd.cursor()

#? Criação do banco:
mycursor.execute("CREATE DATABASE ecolaço DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;")

#? Selecionando o banco cadastros:
mycursor.execute("USE ecolaço")

#? Tabelas Criadas:
mycursor.execute("""CREATE TABLE fornecedor (
    id_user int NOT NULL AUTO_INCREMENT,
    cpf varchar(14) UNIQUE NOT NULL,
    nome varchar(60) NOT NULL,
    telefone varchar(20) NOT NULL,
    email varchar(100) UNIQUE NOT NULL,
    senha varchar(20) NOT NULL,
    pontuação smallint DEFAULT 0,
    primary key(id_user)
    ) default charset = utf8mb4""")

mycursor.execute("""CREATE TABLE coletor(
    id_org int NOT NULL AUTO_INCREMENT,
    nome varchar(60) NOT NULL,
    cnpj varchar(40) UNIQUE NOT NULL,
    email varchar(100) UNIQUE NOT NULL,
    telefone varchar(20) NOT NULL,
    chave_login varchar(12) UNIQUE NOT NULL,
    senha varchar(20) NOT NULL,
    primary key(id_org)
) default charset = utf8mb4""")

mycursor.execute("""CREATE TABLE recompensas(
    id_recompensa int NOT NULL,
    id_coletor int,
    nome varchar(100) NOT NULL,
    custo int NOT NULL,
    FOREIGN KEY (id_coletor) REFERENCES coletor(id_org),
    PRIMARY KEY (id_recompensa)
) default charset = utf8mb4""")

mycursor.execute("""CREATE TABLE trocas(
    id_troca int NOT NULL AUTO_INCREMENT,
    id_user int,
    id_org int,
    id_recompensa int,
    quantidade int NOT NULL,
    custototal int NOT NULL,
    FOREIGN KEY (id_user) REFERENCES fornecedor(id_user),
    FOREIGN KEY (id_org) REFERENCES coletor(id_org),
    FOREIGN KEY (id_recompensa) REFERENCES recompensas(id_recompensa),
    PRIMARY KEY (id_troca)
) default charset = utf8mb4""")

mycursor.execute("""CREATE TABLE endereço(
    id_coletor int,
    rua varchar(60) not null,
    numero varchar(5) not null,
    bairro varchar(60) not null,
    cidade varchar(60) not null,
    estado varchar(30) not null,
    cep varchar(9) not null UNIQUE,
    PRIMARY KEY (cep),
    FOREIGN KEY (id_coletor) REFERENCES coletor (id_org)
) default charset = utf8mb4;""")

mycursor.execute("""CREATE TABLE entregas(
    id_coletor int,
    id_user int,
    codigo_resgate VARCHAR(15) NOT NULL,
    material varchar(20) NOT NULL,
    peso smallint NOT NULL,
    pontos smallint NOT NULL,
    status_codigo enum('DISP','INDISP') NOT NULL DEFAULT 'DISP',
    PRIMARY KEY (codigo_resgate),
    FOREIGN KEY (id_coletor) REFERENCES coletor (id_org),
    FOREIGN KEY (id_user) REFERENCES fornecedor (id_user)
) default charset = utf8mb4;""")
