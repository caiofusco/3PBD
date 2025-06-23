-- Vagas disponíveis em um dia específico
SELECT V.*
FROM Vaga V
WHERE V.VagaID NOT IN (
    SELECT RV.VagaID
    FROM ReservaVaga RV
    JOIN Reserva R ON RV.ReservaID = R.ReservaID
    WHERE '2025-07-02' BETWEEN R.DtInicio AND R.DtFim
);

-- Vagas reservadas em um dia específico
SELECT V.*, R.ReservaID, R.ClienteID
FROM Vaga V
JOIN ReservaVaga RV ON V.VagaID = RV.VagaID
JOIN Reserva R ON RV.ReservaID = R.ReservaID
WHERE '2025-07-02' BETWEEN R.DtInicio AND R.DtFim;
