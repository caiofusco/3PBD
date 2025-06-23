-- Tabela cliente
UPDATE Cliente
SET Telefone = '11999998888'
WHERE ClienteID = 1;


-- Tabela Quarto
UPDATE Quarto
SET QtdBanheiro = 1
WHERE QuartoID = 2;


-- Tabela Vaga
UPDATE Vaga
SET Posicao = 'Outra'
WHERE VagaID = 1;


-- Tabela Reserva
UPDATE Reserva
SET Status = 'Cancelada'
WHERE ReservaID = 1;


-- Tabela ReservaVaga
-- Não aplicável

-- Tabela Pagamento
UPDATE Pagamento
SET Status = 'Estornado'
WHERE PagamentoID = 2;
