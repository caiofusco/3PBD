CREATE DATABASE AV2Albergue;
USE AV2Albergue;

CREATE TABLE Cliente (
    ClienteID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Telefone VARCHAR(20),
    CPF VARCHAR(11) NOT NULL
);

CREATE TABLE Quarto (
    QuartoID INT AUTO_INCREMENT PRIMARY KEY,
    Numero VARCHAR(10) NOT NULL,
    Capacidade INT NOT NULL,
    QtdBanheiro INT NOT NULL,
    Descricao VARCHAR(255)
);

CREATE TABLE Vaga (
    VagaID INT AUTO_INCREMENT PRIMARY KEY,
    QuartoID INT NOT NULL,
    TipoBeliche ENUM('Em cima', 'Em baixo', 'Não beliche') NOT NULL,
    Posicao ENUM('Perto da porta', 'Perto da janela', 'Outra') NOT NULL,
    Descricao VARCHAR(255),
    FOREIGN KEY (QuartoID) REFERENCES Quarto(QuartoID)
);

CREATE TABLE Reserva (
    ReservaID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT NOT NULL,
    DtInicio DATE NOT NULL,
    DtFim DATE NOT NULL,
    Status ENUM('Ativa', 'Cancelada', 'Concluída') NOT NULL DEFAULT 'Ativa',
    DataCriacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE ReservaVaga (
    ReservaID INT NOT NULL,
    VagaID INT NOT NULL,
    PRIMARY KEY (ReservaID, VagaID),
    FOREIGN KEY (ReservaID) REFERENCES Reserva(ReservaID),
    FOREIGN KEY (VagaID) REFERENCES Vaga(VagaID)
);

CREATE TABLE Pagamento (
    PagamentoID INT AUTO_INCREMENT PRIMARY KEY,
    ReservaID INT NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    DtPagamento DATE,
    Metodo VARCHAR(30),
    Status ENUM('Pago', 'Pendente', 'Estornado') NOT NULL DEFAULT 'Pendente',
    FOREIGN KEY (ReservaID) REFERENCES Reserva(ReservaID)
);