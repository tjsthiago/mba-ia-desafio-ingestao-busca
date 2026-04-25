# Ingestão e Busca Semântica com LangChain e Postgres

## Objetivo
Você deve entregar um software capaz de ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector.

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

# Gemini
- Utilizar a chave de API GOOGLE_API_KEY contida no arquivo .env
- Modelo de embeddings: models/embedding-001
- Modelo de LLM para responder: gemini-2.5-flash-lite

# Requisitos
## Ingestão do PDF
- O PDF deve ser dividido em chunks de 1000 caracteres com overlap de 150.
- Cada chunk deve ser convertido em embedding.
- Os vetores devem ser armazenados no banco de dados PostgreSQL com pgVector.

# Estrutura obrigatória do projeto
├── docker-compose.yml
├── requirements.txt      # Dependências
├── .env.example          # Template da variável OPENAI_API_KEY
├── src/
│   ├── ingest.py         # Script de ingestão do PDF (será criado neste outro PRD)
│   ├── search.py         # Script de busca (será criado em outro PRD)
│   ├── chat.py           # CLI para interação com usuário (será criado em outro PRD)
├── document.pdf          # PDF para ingestão
└── README.md             # Instruções de execução



