-- Tabela cliente
DELETE FROM Cliente
WHERE ClienteID = 2;

-- Tabela Quarto
DELETE FROM Quarto
WHERE QuartoID = 2;

-- Tabela Vaga
DELETE FROM Vaga
WHERE VagaID = 2;

-- Tabela Reserva
DELETE FROM Reserva
WHERE ReservaID = 1;

-- Tabela ReservaVaga
DELETE FROM ReservaVaga
WHERE ReservaID = 1 AND VagaID = 2;

-- Tabela Pagamento
DELETE FROM Pagamento
WHERE PagamentoID = 1;