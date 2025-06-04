-- Inserir categorias
INSERT INTO bba_categoria (nome) VALUES
('Churrasco'),
('Drinks'),
('Adicionais'),
('Combos'),
('Bebidas'),
('Tabacaria')
ON CONFLICT (nome) DO NOTHING;