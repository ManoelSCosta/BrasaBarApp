-- database/schema.sql

-- Tabela de contas (mesas/entregas)
CREATE TABLE IF NOT EXISTS bba_conta (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('salão', 'entrega')),
    aberta BOOLEAN DEFAULT TRUE,
    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fechamento TIMESTAMP,
    embalagem BOOLEAN DEFAULT FALSE,
    total NUMERIC(10,2) DEFAULT 0.00
);

-- Tabela de categorias de produtos
CREATE TABLE IF NOT EXISTS bba_categoria (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Tabela de itens do menu
CREATE TABLE IF NOT EXISTS bba_item (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria_id INTEGER REFERENCES bba_categoria(id),
    preco NUMERIC(10,2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

-- Tabela de pedidos
CREATE TABLE IF NOT EXISTS bba_pedido (
    id SERIAL PRIMARY KEY,
    conta_id INTEGER REFERENCES bba_conta(id) NOT NULL,
    item_id INTEGER REFERENCES bba_item(id) NOT NULL,
    quantidade INTEGER DEFAULT 1,
    observacoes TEXT,
    horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    impresso BOOLEAN DEFAULT FALSE
);

-- Tabela de pagamentos
CREATE TABLE IF NOT EXISTS bba_pagamento (
    id SERIAL PRIMARY KEY,
    conta_id INTEGER REFERENCES bba_conta(id) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('Pix', 'Cartão', 'Caixa')),
    valor NUMERIC(10,2) NOT NULL,
    horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de caixas (abertura/fechamento)
CREATE TABLE IF NOT EXISTS bba_caixa (
    id SERIAL PRIMARY KEY,
    data_abertura TIMESTAMP NOT NULL,
    data_fechamento TIMESTAMP,
    saldo_inicial NUMERIC(10,2) NOT NULL,
    saldo_final NUMERIC(10,2)
);