
CREATE TABLE logs(
    id_log SERIAL PRIMARY KEY,
    occurred_at TIMESTAMP NOT NULL,
    received_at TIMESTAMP NOT NULL,
    service VARCHAR(100) NOT NULL,
    severity VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
)

SELECT * FROM logs;


