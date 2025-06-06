# Brasa Bar App

## 🚀 Instalação e Configuração Inicial

### ✅ Pré-requisitos

- Python 3.10+
- PostgreSQL (ex: `brasa_bar_db` já criado)
- pip (gerenciador de pacotes Python)
- (Opcional) virtualenv

---

### 📦 1. Clonar o projeto

```bash
git clone https://github.com/ManoelSCosta/BrasaBarApp.git
cd BrasaBarApp
```

---

### 🧪 2. Criar ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

---

### 📥 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### ⚙️ 4. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=brasa_bar_db
DB_USER=
DB_PASSWORD=
DB_SCHEMA=brasa_bar
```

---

### 🧱 5. Inicializar o banco

Com o PostgreSQL rodando e o banco `brasa_bar_db` já criado:

```bash
python app/database/db_connection.py --init
```

---

### 🧪 6. Testar a conexão

```bash
python app/database/db_connection.py
```

---

### ▶️ 7. Executar o sistema

```bash
python main.py
```

---

### 📄 Exemplo de `requirements.txt`

```txt
python-dotenv
sqlalchemy
psycopg2-binary
PySide6
```

---

## 🧭 Visões de Uso

### 🔹 Visão: Atendente

#### Funcionalidades
- Abrir nova comanda
  - Adicionar pedidos (com base em categorias pré-definidas)
    - Incluir observações por pedido
    - Adicionar "Embalagem" 
  - Inserir nome do cliente
  - Associar mesa (única ou múltiplas)
- Cancelar pedido de uma comanda
- Enviar pedidos para o app da gerência
- Listar mesas existentes
- Adicionar nova mesa
- Fechar comanda
  - Selecionar múltiplas formas de pagamento
  - Enviar comanda para impressão final

### 🔹 Visão: Gerência

#### Funcionalidades
- Receber e **imprimir automaticamente** pedidos enviados
  - Incluir aviso de **"EMBALAGEM"** caso ativado pelo atendente
- Abrir caixa
- Fechar caixa
  - Gerar **PDF com resumo financeiro**, detalhamento de vendas por categoria e método de pagamento
- Gerar relatório de produção do dia
  - Contagem por categoria: drinks, bebidas, espetos, combos, tabacaria
- Acessar **aba FINANÇAS** (protegida por senha)
  - Monitorar recebimentos por forma de pagamento
  - Exibir histórico de transações
  - Diferenciar visualmente pedidos por tipo: *Entrega* vs *Salão*

## 🧾 Entidades e Dados

### 🔸 Constantes

#### Categorias (Menu)
- Churrasco  
- Adicionais  
- Combos  
- Drinks  
- Bebidas  
- Tabacaria  

#### Formas de Pagamento
- Dinheiro  
- Cartão Débito  
- Cartão Crédito  
- PIX  

#### Tipos de Transação
- RECEBIMENTO  
- TROCO  
- DESPESA  
- SANGRIA  
- SUPRIMENTO  

### 🔸 Entidades de Domínio

#### 📌 Comanda
| Atributo             | Tipo              |
|----------------------|-------------------|
| id                   | UUID / SERIAL     |
| data_abertura        | datetime          |
| data_fechamento      | datetime (null)   |
| numero_mesa          | int               |
| mesas_adicionais     | array[int]        |
| nome_cliente         | text              |
| status               | enum: {ABERTA, FECHADA, CANCELADA} |
| pedidos              | list[Pedido]      |
| valor_total          | decimal           |
| forma_pagamento      | list[FormaPagamento] |
| observações          | text              |

#### 📌 Pedido
| Atributo          | Tipo          |
|-------------------|---------------|
| id                | UUID / SERIAL |
| quantidade        | int           |
| preco_unitario    | decimal       |
| itens             | list[Item]    |
| observacoes       | text          |
| embalagem         | bool          |
| data_hora_pedido  | datetime      |

#### 📌 Item
| Atributo     | Tipo          |
|--------------|---------------|
| id           | UUID / SERIAL |
| descricao    | text          |
| categoria    | enum[Categoria] |
| preco        | decimal       |

#### 📌 Caixa
| Atributo              | Tipo              |
|------------------------|-------------------|
| id                     | UUID / SERIAL     |
| data_hora_abertura     | datetime          |
| data_hora_fechamento   | datetime (null)   |
| responsavel            | text              |
| valor_abertura         | decimal           |
| valor_entradas         | decimal           |
| valor_saidas           | decimal           |
| valor_final            | decimal           |
| comandas               | list[Comanda]     |
| observacoes            | text              |
| status                 | enum: {ABERTO, FECHADO} |

#### 📌 Transação
| Atributo             | Tipo              |
|----------------------|-------------------|
| id                   | UUID / SERIAL     |
| data_hora_transacao  | datetime          |
| tipo_transacao       | enum[TipoTransacao] |
| valor                | decimal           |
| forma_pagamento      | enum[FormaPagamento] |
| responsavel          | text              |
| comanda_associada    | FK -> Comanda     |
| caixa_associado      | FK -> Caixa       |
| observacoes          | text              |

## 📜 Regras de Negócio

### Atendimento
- Adição de pedidos deve respeitar categorias existentes
- Exibir preferencia por embalagem for marcada
- Comandas podem ser associadas a mais de uma mesa
- Cancelamentos devem ser registrados e notificados à gerência

### Impressão (via gerência)
- Pedido deve ser impresso automaticamente ao ser enviado
- Formato:
  ```
  Nome || Horário
  x Item; - Observação;
  !!! EMBALAGEM (se houver)
  ```
- Impressão do fechamento:
  ```
  Nome || Total || Salão/Entrega
  R$X Pix | R$Y Cartão
  -> x Carne; x Caipirinha; x Coca...
  ```

### Finanças
- A aba “FINANÇAS” deve ser protegida por senha
- Relatórios de fechamento devem conter:
  - Totais por forma de pagamento
  - Separação de pedidos Salão vs Entrega
  - Contador por categoria
  - Categoria com mais pedidos deve ser destacada

## ⚙️ Requisitos Técnicos

| Componente     | Tecnologia                         |
|----------------|-------------------------------------|
| UI             | QtDesign                           |
| Backend        | Python (FastAPI / Flask sugerido)  |
| Banco de Dados | PostgreSQL                         |
| Impressão      | Suporte a impressora térmica       |
| Relatórios     | PDF (via ReportLab, FPDF, etc.)    |
| Segurança      | Acesso a aba Finanças com senha    |

## 🧪 Exemplo de Operação (Fechamento)

```
Mauro || 57,50 || Entrega
R$22,50 Pix | R$35,00 Dinheiro
-> x Carne; x Caipirinha; x Coca; etc...

Resumo Financeiro:
Pix: R$350,00 || Cartão: R$470,00 || Dinheiro: R$280,00
Pedidos:
15 Drinks | 32 Bebidas | 48 Espetos | 9 Combos | 6 Tabacaria
Mais vendido: Espetos
```