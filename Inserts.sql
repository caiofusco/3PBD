-- Cliente
INSERT INTO Cliente VALUES (1, 'João Silva', 'joao@email.com', '11999990001', '123.456.789-00', 'senha1');
INSERT INTO Cliente VALUES (2, 'Maria Souza', 'maria@email.com', '11999990002', '987.654.321-00', 'senha2');
INSERT INTO Cliente VALUES (3, 'Carlos Lima', 'carlos@email.com', '11999990003', '111.222.333-44', 'senha3');
INSERT INTO Cliente VALUES (4, 'Ana Beatriz', 'ana@email.com', '11999990004', '222.333.444-55', 'senha4');
INSERT INTO Cliente VALUES (5, 'Lucas Mendes', 'lucas@email.com', '11999990005', '333.444.555-66', 'senha5');
-- Pacote
INSERT INTO Pacote VALUES (1, 'Pacote Bronze', 150.00, 10.00);
INSERT INTO Pacote VALUES (2, 'Pacote Prata', 250.00, 20.00);
INSERT INTO Pacote VALUES (3, 'Pacote Ouro', 350.00, 30.00);
INSERT INTO Pacote VALUES (4, 'Pacote Premium', 500.00, 50.00);
INSERT INTO Pacote VALUES (5, 'Pacote Express', 100.00, 5.00);
-- Servico
INSERT INTO Servico VALUES (1, 'Corte de Cabelo', 30, 50.00, 'Corte masculino', 'S');
INSERT INTO Servico VALUES (2, 'Manicure', 45, 40.00, 'Serviço completo de manicure', 'S');
INSERT INTO Servico VALUES (3, 'Massagem', 60, 100.00, 'Relaxante', 'S');
INSERT INTO Servico VALUES (4, 'Depilação', 30, 70.00, 'Depilação corporal', 'S');
INSERT INTO Servico VALUES (5, 'Sobrancelha', 20, 30.00, 'Design de sobrancelha', 'N');
-- AgrupaPacoteServico
INSERT INTO AgrupaPacoteServico VALUES (1, 1, 1, 45.00);
INSERT INTO AgrupaPacoteServico VALUES (2, 1, 2, 35.00);
INSERT INTO AgrupaPacoteServico VALUES (3, 2, 3, 90.00);
INSERT INTO AgrupaPacoteServico VALUES (4, 3, 4, 60.00);
INSERT INTO AgrupaPacoteServico VALUES (5, 4, 5, 25.00);
-- Profissional
INSERT INTO Profissional VALUES (1, 'Patrícia Gomes', 'patricia@email.com', '11999990010', '444.555.666-77');
INSERT INTO Profissional VALUES (2, 'Fernando Rocha', 'fernando@email.com', '11999990011', '555.666.777-88');
INSERT INTO Profissional VALUES (3, 'Juliana Costa', 'juliana@email.com', '11999990012', '666.777.888-99');
INSERT INTO Profissional VALUES (4, 'Roberta Lima', 'roberta@email.com', '11999990013', '777.888.999-00');
INSERT INTO Profissional VALUES (5, 'Eduardo Silva', 'eduardo@email.com', '11999990014', '888.999.000-11');
-- AgrupaProfissionalServico
INSERT INTO AgrupaProfissionalServico VALUES (1, 1, 1);
INSERT INTO AgrupaProfissionalServico VALUES (2, 2, 2);
INSERT INTO AgrupaProfissionalServico VALUES (3, 3, 3);
INSERT INTO AgrupaProfissionalServico VALUES (4, 4, 4);
INSERT INTO AgrupaProfissionalServico VALUES (5, 5, 5);
-- Credito
INSERT INTO Credito VALUES (1, 1, 100.00, '2025-12-31');
INSERT INTO Credito VALUES (2, 2, 150.00, '2025-11-30');
INSERT INTO Credito VALUES (3, 3, 200.00, '2025-10-31');
INSERT INTO Credito VALUES (4, 4, 50.00, '2025-09-30');
INSERT INTO Credito VALUES (5, 5, 300.00, '2026-01-31');
-- Notificacao
INSERT INTO Notificacao VALUES (1, 1, 'SMS', 'Promoção imperdível!', '2025-05-26 10:00:00', 'Enviado');
INSERT INTO Notificacao VALUES (2, 2, 'EMAIL', 'Agendamento confirmado.', '2025-05-26 11:00:00', 'Lido');
INSERT INTO Notificacao VALUES (3, 3, 'SMS', 'Seu crédito expirará em breve.', '2025-05-25 15:30:00', 'Pendente');
INSERT INTO Notificacao VALUES (4, 4, 'EMAIL', 'Nova avaliação disponível.', '2025-05-24 09:00:00', 'Lido');
INSERT INTO Notificacao VALUES (5, 5, 'SMS', 'Agendamento cancelado.', '2025-05-23 08:45:00', 'Enviado');
-- FilaEspera
INSERT INTO FilaEspera VALUES (1, 1, '2025-05-26 08:00:00', 1, 1);
INSERT INTO FilaEspera VALUES (2, 2, '2025-05-26 08:05:00', 2, 2);
INSERT INTO FilaEspera VALUES (3, 3, '2025-05-26 08:10:00', 3, 3);
INSERT INTO FilaEspera VALUES (4, 4, '2025-05-26 08:15:00', 4, 1);
INSERT INTO FilaEspera VALUES (5, 5, '2025-05-26 08:20:00', 5, 2);
-- HorarioDisponivel
INSERT INTO HorarioDisponivel VALUES (1, 1, 1, '2025-05-27 09:00:00', '2025-05-27 09:30:00');
INSERT INTO HorarioDisponivel VALUES (2, 2, 2, '2025-05-27 10:00:00', '2025-05-27 10:45:00');
INSERT INTO HorarioDisponivel VALUES (3, 3, 3, '2025-05-27 11:00:00', '2025-05-27 12:00:00');
INSERT INTO HorarioDisponivel VALUES (4, 4, 4, '2025-05-27 13:00:00', '2025-05-27 13:30:00');
INSERT INTO HorarioDisponivel VALUES (5, 5, 5, '2025-05-27 14:00:00', '2025-05-27 14:20:00');
-- AgendaProfissional
INSERT INTO AgendaProfissional VALUES (1, 1, 'Segunda-feira', '08:00:00', '18:00:00');
INSERT INTO AgendaProfissional VALUES (2, 2, 'Terça-feira', '08:00:00', '18:00:00');
INSERT INTO AgendaProfissional VALUES (3, 3, 'Quarta-feira', '08:00:00', '18:00:00');
INSERT INTO AgendaProfissional VALUES (4, 4, 'Quinta-feira', '08:00:00', '18:00:00');
INSERT INTO AgendaProfissional VALUES (5, 5, 'Sexta-feira', '08:00:00', '18:00:00');
-- Reserva
INSERT INTO Reserva VALUES (1, '2025-05-28 09:00:00', 'Confirmado', 90.00, NULL, NULL, 1, 1, 1, 1);
INSERT INTO Reserva VALUES (2, '2025-05-28 10:00:00', 'Cancelado', 0.00, 'Cliente não compareceu', NULL, 2, 2, 2, 2);
INSERT INTO Reserva VALUES (3, '2025-05-28 11:00:00', 'Finalizado', 100.00, NULL, '2025-05-28 12:00:00', 3, 3, 3, 3);
INSERT INTO Reserva VALUES (4, '2025-05-28 13:00:00', 'Confirmado', 70.00, NULL, NULL, 4, 4, 4, 4);
INSERT INTO Reserva VALUES (5, '2025-05-28 14:00:00', 'Confirmado', 50.00, NULL, NULL, 5, 5, 5, 5);
-- Avaliacao
INSERT INTO Avaliacao VALUES (1, 1, 5, 'Excelente atendimento!', '2025-05-28 12:00:00');
INSERT INTO Avaliacao VALUES (2, 2, 3, 'Houve um atraso.', '2025-05-28 12:30:00');
INSERT INTO Avaliacao VALUES (3, 3, 4, 'Muito bom, voltarei.', '2025-05-28 13:00:00');
INSERT INTO Avaliacao VALUES (4, 4, 2, 'Serviço não realizado.', '2025-05-28 13:30:00');
INSERT INTO Avaliacao VALUES (5, 5, 5, 'Perfeito!', '2025-05-28 14:00:00');
-- Pagamento
INSERT INTO Pagamento VALUES (1, 1, 90.00, 'N', '2025-05-28 09:30:00');
INSERT INTO Pagamento VALUES (2, 2, 0.00, 'N', '2025-05-28 10:30:00');
INSERT INTO Pagamento VALUES (3, 3, 100.00, 'S', '2025-05-28 12:00:00');
INSERT INTO Pagamento VALUES (4, 4, 70.00, 'N', '2025-05-28 13:30:00');
INSERT INTO Pagamento VALUES (5, 5, 50.00, 'S', '2025-05-28 14:30:00');
-- AgrupaPagamentos
INSERT INTO AgrupaPagamentos VALUES (1, 1, 1);
INSERT INTO AgrupaPagamentos VALUES (2, 2, 2);
INSERT INTO AgrupaPagamentos VALUES (3, 3, 3);
INSERT INTO AgrupaPagamentos VALUES (4, 4, 4);
INSERT INTO AgrupaPagamentos VALUES (5, 5, 5);
