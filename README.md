# Desafio MBA Engenharia de Software com IA - Full Cycle


# Instruções de Execução

## 1. Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Chave de API OpenAI e Google Gemini (para embeddings e LLM)

## 2. Setup do Ambiente Python

Recomenda-se usar o mesmo ambiente virtual do projeto principal (ou crie um novo):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Subir o Banco PostgreSQL + pgvector

No diretório do projeto, execute:

```bash
docker-compose up -d
```
Isso irá subir o banco PostgreSQL já com a extensão pgvector habilitada.

## 4. Configuração do .env

Preencha o arquivo `.env` na raiz do projeto com as variáveis necessárias:

```
OPENAI_API_KEY=...           # sua chave OpenAI
GOOGLE_API_KEY=...           # sua chave Google Gemini
OPENAI_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:55432/rag
PG_VECTOR_COLLECTION_NAME=gpt5_collection
PDF_PATH=document.pdf        # caminho do PDF a ser ingerido
```

## 5. Ingestão do PDF

Antes de usar o chat, é necessário ingerir o PDF para o banco vetorial:

```bash
python src/ingest.py
```
Isso irá carregar o PDF, gerar embeddings e persistir no banco vetorial.

## 6. Executando o Chat CLI

Com o banco populado, execute:

```bash
python src/chat.py
```
Você poderá digitar perguntas em português. O sistema irá buscar a resposta exclusivamente no conteúdo do PDF ingerido.

## 7. Exemplo de Uso

```
Faça sua pergunta (ou 'sair' para encerrar):

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## 8. Observações

- O modelo LLM padrão é `gemini-2.5-flash-lite` (ajuste no código ou variável de ambiente se necessário).
- O sistema só responde com base no PDF. Perguntas fora do contexto retornam a mensagem padrão.
- Para dúvidas sobre dependências, consulte o `requirements.txt`.

---
Para detalhes técnicos, veja o arquivo `specifications/feature/cli-search/spec-cli-search.md`.