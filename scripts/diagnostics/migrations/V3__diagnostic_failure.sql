-- Проверка отката DDL при ошибке миграции. Горохов Георгий, 4П1.23.
CREATE TABLE diagnostic_probe (id bigint PRIMARY KEY);
INSERT INTO diagnostic_missing_table (id) VALUES (1);
