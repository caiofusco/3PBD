# API TemTudo - DDD + ORM + SQL Server

Projeto academico em Python para processar pedidos de marketplaces a partir de arquivos CSV.

A API foi organizada em camadas inspiradas em DDD:

```text
src/temtudo/
  domain/          Regras e conceitos de dominio, como status de pedido e compra
  application/     Casos de uso: importar CSV, processar carga, atender pedidos, receber fornecedor
  infrastructure/  Banco de dados, ORM SQLAlchemy e modelos das tabelas
  interfaces/api/  Rotas HTTP FastAPI e schemas de resposta
scripts/           Scripts SQL para criar e consultar as tabelas no SQL Server
samples/           CSVs de exemplo
```

## Regras implementadas

1. O CSV de pedidos e importado para a tabela de carga `CARGA_CARG`.
2. Cada importacao recebe um `LOTE_ID`.
3. O processamento do lote cadastra:
   - clientes novos em `CLIENTES_CLI`;
   - produtos novos em `PRODUTOS_PRD`;
   - pedidos unicos em `PEDIDOS_PED`, agrupando pelo `order-id`;
   - itens em `ITPEDIDO_ITP`, uma linha para cada `order-item-id`.
4. O atendimento dos pedidos avalia pedidos `NULL` ou `PENDENTE` por ordem de maior `VL_TOTAL` para menor.
5. Um pedido so e atendido se todos os produtos tiverem estoque suficiente.
6. Pedido atendido gera registros em `MOVIMENTO_MOV` e debita o estoque em `PRODUTOS_PRD`.
7. Pedido sem estoque suficiente fica `PENDENTE` e gera registro em `COMPRAS_COM` com a quantidade faltante.
8. O CSV do fornecedor atualiza o estoque dos produtos entregues.
9. Depois da entrada do fornecedor, rode novamente o atendimento para tentar atender pedidos pendentes.

## Requisitos

- Python 3.10 ou superior.
- SQL Server instalado.
- SQL Server Management Studio para criar o banco/tabelas.
- Driver ODBC do SQL Server instalado na maquina.

## Como executar

### 1. Criar o banco no SQL Server

No SQL Server Management Studio:

```sql
CREATE DATABASE TemTudo;
GO
USE TemTudo;
GO
```

Depois execute o arquivo:

```text
scripts/create_tables.sql
```

### 2. Criar ambiente virtual e instalar dependencias

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux/macOS, a ativacao e:

```bash
source .venv/bin/activate
```

### 3. Configurar conexao com o SQL Server

Copie o arquivo `.env.example` para `.env` e edite a variavel `DATABASE_URL`.

Exemplo com usuario e senha SQL Server:

```env
DATABASE_URL=mssql+pyodbc://sa:SUA_SENHA@localhost:1433/TemTudo?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
INITIAL_STOCK_DEFAULT=100
```

Exemplo com autenticacao Windows:

```env
DATABASE_URL=mssql+pyodbc://@localhost:1433/TemTudo?driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes
INITIAL_STOCK_DEFAULT=100
```

O valor `INITIAL_STOCK_DEFAULT=100` foi mantido para bater com o SQL original, que cadastrava produtos novos com estoque inicial 100. Para um sistema mais realista, altere para `0` e alimente o estoque apenas pelo CSV do fornecedor.

### 4. Subir a API

```bash
uvicorn temtudo.main:app --reload --app-dir src
```

A documentacao interativa ficara disponivel em:

```text
http://127.0.0.1:8000/docs
```

## Fluxo de teste com os CSVs enviados

1. `POST /cargas/pedidos/csv`
   - envie `samples/CARGA.csv` no campo `arquivo`.
   - a resposta retorna um `lote_id`.

2. `POST /cargas/pedidos/{lote_id}/processar`
   - use o `lote_id` retornado na etapa anterior.

3. `POST /pedidos/atender`
   - atende os pedidos completos por ordem de maior valor.
   - pedidos incompletos ficam pendentes e geram compras.

4. `GET /pedidos`
   - veja os status dos pedidos.

5. `GET /produtos`
   - veja o estoque atualizado.

6. `GET /compras`
   - veja produtos que precisam ser comprados.

7. `POST /fornecedores/entregas/csv`
   - envie `samples/CARGA_FORNECEDOR.csv` no campo `arquivo`.

8. `POST /pedidos/atender`
   - rode novamente para tentar atender pedidos pendentes apos a entrada do fornecedor.

## Endpoints principais

| Metodo | Rota | O que faz |
|---|---|---|
| GET | `/health` | Testa se a API esta no ar |
| POST | `/cargas/pedidos/csv` | Importa o CSV de pedidos para a carga |
| POST | `/cargas/pedidos/{lote_id}/processar` | Processa a carga para clientes, produtos, pedidos e itens |
| POST | `/pedidos/atender` | Aplica a regra de atendimento e estoque |
| POST | `/fornecedores/entregas/csv` | Importa entrega do fornecedor e atualiza estoque |
| GET | `/pedidos` | Lista pedidos |
| GET | `/produtos` | Lista produtos e estoque |
| GET | `/compras` | Lista compras solicitadas |
| GET | `/movimentos` | Lista movimentacoes de estoque |

## Teste via cURL

```bash
curl -X POST "http://127.0.0.1:8000/cargas/pedidos/csv" \
  -F "arquivo=@samples/CARGA.csv"
```

```bash
curl -X POST "http://127.0.0.1:8000/cargas/pedidos/COLE_O_LOTE_AQUI/processar"
```

```bash
curl -X POST "http://127.0.0.1:8000/pedidos/atender"
```

```bash
curl -X POST "http://127.0.0.1:8000/fornecedores/entregas/csv" \
  -F "arquivo=@samples/CARGA_FORNECEDOR.csv"
```
