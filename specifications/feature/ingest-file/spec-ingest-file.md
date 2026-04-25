# Especificação Técnica — Ingestão de PDF com LangChain e pgVector

## Visão Geral
Esta especificação detalha a implementação da funcionalidade de ingestão de arquivos PDF, convertendo seu conteúdo em embeddings e armazenando-os em um banco PostgreSQL com extensão pgVector, conforme o PRD.

---

## 1. Requisitos Funcionais

1.1. O sistema deve ler um arquivo PDF definido por variável de ambiente (`PDF_PATH`).
1.2. O conteúdo do PDF deve ser dividido em chunks de 1000 caracteres, com overlap de 150 caracteres.
1.3. Cada chunk deve ser convertido em embedding utilizando exclusivamente o modelo OpenAI (`OpenAIEmbeddings`).
1.4. Os embeddings devem ser persistidos em uma coleção do banco PostgreSQL com pgVector.
1.5. O processo deve ser idempotente: reprocessar o mesmo PDF não deve duplicar embeddings.
1.6. O script deve ser executável via CLI (`python src/ingest.py`).

---

## 2. Requisitos Não Funcionais

2.1. O código deve seguir as boas práticas Python (PEP8, tipagem, docstrings, logging ao invés de print, tratamento de exceções).
2.2. Utilizar variáveis de ambiente para credenciais e parâmetros sensíveis.
2.3. O projeto deve ser compatível com Docker Compose e `.env`.
2.4. O código deve ser modular e testável.

---

## 3. Fluxo de Ingestão

1. Carregar variáveis de ambiente (`dotenv`).
2. Validar presença das variáveis obrigatórias:
   - `PDF_PATH`
	- `OPENAI_API_KEY`
   - `PG_VECTOR_COLLECTION_NAME`
   - `DATABASE_URL` (ou `PGVECTOR_URL`)
3. Carregar PDF usando `PyPDFLoader`.
4. Dividir texto com `RecursiveCharacterTextSplitter` (`chunk_size=1000`, `chunk_overlap=150`).
5. Gerar embeddings com:
	- `OpenAIEmbeddings(model="text-embedding-3-small")`
6. Persistir chunks e embeddings no banco via `PGVector`.
7. Logar início, progresso e conclusão do processo.
8. Tratar e logar exceções.

---

## 4. Estrutura Esperada do Código (src/ingest.py)

```python
import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

def ingest_pdf():
	"""Executa o pipeline de ingestão do PDF para o banco vetorial."""
	# 1. Carregar variáveis e validar
	# 2. Carregar PDF
	# 3. Split
	# 4. Embeddings (OpenAIEmbeddings)
	# 5. Persistência
	# 6. Logging e tratamento de erros

if __name__ == "__main__":
	ingest_pdf()
```

---

## 5. Boas Práticas Python (OpenAI)

- Use tipagem estática (`def foo(x: int) -> str:`)
- Sempre documente funções públicas com docstrings.
- Prefira logging configurável ao invés de `print()`.
- Trate exceções específicas e forneça mensagens úteis.
- Separe lógica de configuração, processamento e persistência em funções/módulos distintos.
- Utilize variáveis de ambiente para segredos e parâmetros.
- Siga PEP8 para nomes, espaçamento e organização.

---

## 6. Critérios de Aceite

- PDF é processado e embeddings são persistidos corretamente.
- Não há duplicidade de embeddings ao reprocessar.
- Logs claros de início, progresso e fim.
- Código limpo, modular, com tipagem e docstrings.
- Compatível com Docker Compose e `.env`.
