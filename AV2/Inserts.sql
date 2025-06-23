-- Tabela cliente
INSERT INTO Cliente (Nome, Email, Telefone, CPF)
VALUES 
('João da Silva', 'joao.silva@email.com', '11988887777', '12345678901'),
('Maria Oliveira', 'maria.oliveira@email.com', '21999998888', '98765432100');

-- Tabela Quarto
INSERT INTO Quarto (Numero, Capacidade, QtdBanheiro, Descricao)
VALUES 
('101A', 4, 1, 'Quarto com banheiro e vista para o jardim'),
('102B', 8, 0, 'Quarto sem banheiro, beliches disponíveis');

-- Tabela Vaga
INSERT INTO Vaga (QuartoID, TipoBeliche, Posicao, Descricao)
VALUES 
(1, 'Em cima', 'Perto da janela', 'Beliche superior com boa ventilação'),
(1, 'Em baixo', 'Perto da porta', 'Beliche inferior próxima à entrada');

-- Tabela Reserva
INSERT INTO Reserva (ClienteID, DtInicio, DtFim, Status)
VALUES 
(1, '2025-07-01', '2025-07-05', 'Ativa');

-- Tabela ReservaVaga
INSERT INTO ReservaVaga (ReservaID, VagaID)
VALUES 
(1, 1),
(1, 2);

-- Tabela Pagamento
INSERT INTO Pagamento (ReservaID, Valor, DtPagamento, MetodoPagamento, Status)
VALUES 
(1, 250.00, '2025-06-28', 'Cartão Visa', 'Pago'),
(1, 250.00, '2025-06-28', 'Cartão Mastercard', 'Pago');