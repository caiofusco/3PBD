-- Tabela cliente
SELECT * FROM Cliente;

SELECT * FROM Cliente
WHERE CPF = '12345678901';

-- Tabela Quarto
SELECT * FROM Quarto;

SELECT * FROM Quarto
WHERE Numero = '101A';

-- Tabela Vaga
SELECT * FROM Vaga;

SELECT * FROM Vaga
WHERE QuartoID = 1;

-- Tabela Reserva
SELECT * FROM Reserva;

SELECT * FROM Reserva
WHERE ClienteID = 1 AND Status = 'Ativa';

-- Tabela ReservaVaga
SELECT * FROM ReservaVaga;

SELECT VagaID FROM ReservaVaga
WHERE ReservaID = 1;

-- Tabela Pagamento
SELECT * FROM Pagamento;

SELECT * FROM Pagamento
WHERE ReservaID = 1;

-- Consulta de vagas disponíveis
SELECT V.*
FROM Vaga V
WHERE V.VagaID NOT IN (
    SELECT RV.VagaID
    FROM ReservaVaga RV
    INNER JOIN Reserva R ON RV.ReservaID = R.ReservaID
    WHERE R.DtInicio < '2025-07-05' AND R.DtFim > '2025-07-01'
);
