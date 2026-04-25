import os
import logging
from dotenv import load_dotenv

load_dotenv()


def validate_env_vars() -> dict:
    """Valida a presença das variáveis de ambiente obrigatórias e retorna um dicionário com seus valores."""
    required_vars = [
        "PDF_PATH",
        "OPENAI_API_KEY",
        "PG_VECTOR_COLLECTION_NAME",
        "DATABASE_URL"
    ]
    env = {}
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(var)
        else:
            env[var] = value
    if missing:
        raise EnvironmentError(f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}")
    return env

def load_pdf(pdf_path: str):
    """Carrega o PDF e retorna os documentos extraídos."""
    from langchain_community.document_loaders import PyPDFLoader
    # Garante que o caminho seja absoluto
    if not os.path.isabs(pdf_path):
        # Considera o diretório do arquivo .env como base, ou o diretório do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(base_dir, pdf_path)
        pdf_path = os.path.abspath(pdf_path)
    if not os.path.isfile(pdf_path):
        raise ValueError(f"Arquivo PDF não encontrado: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    if not docs:
        raise ValueError("Nenhum conteúdo encontrado no PDF.")
    return docs

def split_documents(docs):
    """Divide os documentos em chunks usando RecursiveCharacterTextSplitter."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False)
    splits = splitter.split_documents(docs)
    if not splits:
        raise ValueError("Nenhum chunk gerado a partir do PDF.")
    return splits

def persist_embeddings(splits, env):
    """Gera embeddings e persiste no banco PGVector, garantindo idempotência."""
    from langchain_openai import OpenAIEmbeddings
    from langchain_postgres import PGVector
    from langchain_core.documents import Document
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    collection_name = env["PG_VECTOR_COLLECTION_NAME"]
    connection = env["DATABASE_URL"]
    store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True,
    )
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]
    ids = [f"doc-{i}" for i in range(len(enriched))]
    try:
        store.delete(ids=ids)
    except Exception:
        pass
    store.add_documents(documents=enriched, ids=ids)
    return len(enriched)

def ingest_pdf():
    """Executa o pipeline de ingestão do PDF para o banco vetorial."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    try:
        logging.info("Iniciando pipeline de ingestão de PDF para banco vetorial.")
        env = validate_env_vars()
        logging.info("Variáveis de ambiente validadas com sucesso.")

        logging.info(f"Carregando PDF: {env['PDF_PATH']}")
        docs = load_pdf(env["PDF_PATH"])
        logging.info(f"PDF carregado com sucesso. Total de páginas extraídas: {len(docs)}")

        logging.info("Dividindo texto em chunks...")
        splits = split_documents(docs)
        logging.info(f"Texto dividido em {len(splits)} chunks.")

        logging.info("Gerando embeddings e persistindo no banco PGVector...")
        total = persist_embeddings(splits, env)
        logging.info(f"Persistência concluída. Total de embeddings inseridos: {total}")
        logging.info("Pipeline de ingestão finalizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro na ingestão: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    ingest_pdf()