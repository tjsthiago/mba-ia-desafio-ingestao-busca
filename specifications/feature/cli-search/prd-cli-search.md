# 1. Consulta via CLI

## Objetivo

Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

# Tecnologias obrigatórias
- Linguagem: Python
- Framework: LangChain
- Banco de dados: PostgreSQL + pgVector
- Execução do banco de dados: Docker & Docker Compose (docker-compose fornecido no repositório de exemplo)

# Pacotes recomendados
- Split: from langchain_text_splitters import RecursiveCharacterTextSplitter
- Embeddings (OpenAI): from langchain_openai import OpenAIEmbeddings
- Embeddings (Gemini): from langchain_google_genai import GoogleGenerativeAIEmbeddings
- PDF: from langchain_community.document_loaders import PyPDFLoader
- Ingestãofrom langchain_postgres import PGVector


# OpenAI
- Utilizar a chave de API OPENAI_API_KEY contida no arquivo .env
- Modelo de embeddings: text-embedding-3-small
- Modelo de LLM para responder: gpt-5-nano

# Estrutura obrigatória do projeto
├── docker-compose.yml
├── requirements.txt      # Dependências
├── .env.example          # Template da variável OPENAI_API_KEY
├── src/
│   ├── ingest.py         # Script de ingestão do PDF (já existe)
│   ├── search.py         # Script de busca (deverá ser criado)
│   ├── chat.py           # CLI para interação com usuário (deverá ser criado)
├── document.pdf          # PDF para ingestão
└── README.md             # Instruções de execução

---

# Requisitos

## Busca
- Criar um script Python para simular um chat no terminal e executar os seguintes passos:
    - Passos ao receber uma pergunta:
        - Vetorizar a pergunta
        - Buscar os 10 resultados mais relevantes (k=10) no banco vetorial
        - Montar o prompt e chamar a LLM
        - Retornar a resposta ao usuário

## Exemplo no CLI

```
Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

```
---

Perguntas fora do contexto:

```
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## Prompt a ser utilizado para executar chamada para LLM com o questionamento do usuário após ter recuperados os embeddings do PGVector

````
CONTEXTO:
{resultados concatenados do banco de dados}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta do usuário}

RESPONDA A "PERGUNTA DO USUÁRIO"
```

# Caminho de projeto com exemplo de pesquisa usando PGVector
- Caminho: /Users/thiagojosedasilva/Documents/development/repositories/mba-full-cycle/mba-ia-niv-introducao-langchain
- Arquivo de exemplo de pesquisa usando PGVector: /Users/thiagojosedasilva/Documents/development/repositories/mba-full-cycle/mba-ia-niv-introducao-langchain/5-loaders-e-banco-de-dados-vetoriais/4-search-vector.py
