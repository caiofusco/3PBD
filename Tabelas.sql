CREATE TABLE Cliente (
    ClienteID INT PRIMARY KEY,
    Nome VARCHAR(255),
    Email VARCHAR(100),
    Telefone VARCHAR(11),
    CPF VARCHAR(14),
    Senha VARCHAR(255)
);

CREATE TABLE Pacote (
    PacoteID INT PRIMARY KEY,
    Nome VARCHAR(255),
    Preco DECIMAL(10, 2),
    Desconto DECIMAL(10, 2)
);

CREATE TABLE Servico (
    ServicoID INT PRIMARY KEY,
    Nome VARCHAR(255),
    DuracaoMinutos INT,
    Preco DECIMAL(10,2),
    Descricao VARCHAR(255),
    RequerAgendamento VARCHAR(1)
);

CREATE TABLE AgrupaPacoteServico (
    AgrupaPacoteServicoID INT PRIMARY KEY,
    PacoteID INT,
    ServicoID INT,
    NovoPreco DECIMAL(10,2),
    FOREIGN KEY (PacoteID) REFERENCES Pacote(PacoteID),
    FOREIGN KEY (ServicoID) REFERENCES Servico(ServicoID)
);

CREATE TABLE Profissional (
    ProfissionalID INT PRIMARY KEY,
    Nome VARCHAR(255),
    Email VARCHAR(100),
    Telefone VARCHAR(11),
    CPF VARCHAR(14)
);

CREATE TABLE AgrupaProfissionalServico (
    AgrupaProfissionalServicoID INT PRIMARY KEY,
    ProfissionalID INT,
    ServicoID INT,
    FOREIGN KEY (ProfissionalID) REFERENCES Profissional(ProfissionalID),
    FOREIGN KEY (ServicoID) REFERENCES Servico(ServicoID)
);

CREATE TABLE Credito (
    CreditoID INT PRIMARY KEY,
    ClienteID INT,
    Valor DECIMAL(10, 2),
    DataExpiracao DATE,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE Notificacao (
    NotificacaoID INT PRIMARY KEY,
    ClienteID INT,
    Tipo VARCHAR(10),
    Mensagem VARCHAR(255),
    DataEnvio DATETIME,
    Status VARCHAR(10),
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE FilaEspera (
    FilaID INT PRIMARY KEY,
    ClienteID INT,
    DataHoraSolicitacao DATETIME,
    ServicoID INT,
    Prioridade INT,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE HorarioDisponivel (
    HorarioID INT PRIMARY KEY,
    ProfissionalID INT,
    ServicoID INT,
    DataHoraInicio DATETIME,
    DataHoraFim DATETIME,
    FOREIGN KEY (ProfissionalID) REFERENCES Profissional(ProfissionalID),
    FOREIGN KEY (ServicoID) REFERENCES Servico(ServicoID)
);

CREATE TABLE AgendaProfissional (
    AgendaID INT PRIMARY KEY,
    ProfissionalID INT,
    DiaSemana VARCHAR(20),
    HoraInicio TIME,
    HoraFim TIME,
    FOREIGN KEY (ProfissionalID) REFERENCES Profissional(ProfissionalID)
);

CREATE TABLE Reserva (
    ReservaID INT PRIMARY KEY,
    DataHora DATETIME,
    Status VARCHAR(10),
    ValPago DECIMAL(10, 2),
    MotivoCancelamento VARCHAR(255) NULL,
    DataConclusao DATETIME NULL,
    ClienteID INT,
    AgrupaPacoteServicoID INT,
    AgrupaProfissionalServicoID INT,
    AgrupaPagamentoID INT,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID),
    FOREIGN KEY (AgrupaPacoteServicoID) REFERENCES AgrupaPacoteServico(AgrupaPacoteServicoID),
    FOREIGN KEY (AgrupaProfissionalServicoID) REFERENCES AgrupaProfissionalServico(AgrupaProfissionalServicoID)
);

CREATE TABLE Avaliacao (
    AvaliacaoID INT PRIMARY KEY,
    ReservaID INT,
    Nota INT,
    Comentario VARCHAR(255),
    DataAvaliacao DATETIME,
    FOREIGN KEY (ReservaID) REFERENCES Reserva(ReservaID)
);

CREATE TABLE Pagamento (
    PagamentoID INT PRIMARY KEY,
    ReservaID INT,
    Valor DECIMAL(10, 2),
    UsoCredito VARCHAR(1),
    DataPagamento DATETIME,
    FOREIGN KEY (ReservaID) REFERENCES Reserva(ReservaID)
);

CREATE TABLE AgrupaPagamentos (
    AgrupaPagamentoID INT PRIMARY KEY,
    ReservaID INT,
    PagamentoID INT,
    FOREIGN KEY (ReservaID) REFERENCES Reserva(ReservaID),
    FOREIGN KEY (PagamentoID) REFERENCES Pagamento(PagamentoID)
);

ALTER TABLE Reserva
ADD CONSTRAINT FK_Reserva_AgrupaPagamentos
FOREIGN KEY (AgrupaPagamentoID) REFERENCES AgrupaPagamentos(AgrupaPagamentoID);