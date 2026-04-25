import os
import logging
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# Função de busca vetorial para consulta PGVector e retorno do contexto

def search_question(question: str, k: int = 10) -> list:
    """
    Vetoriza a pergunta, consulta PGVector e retorna os textos dos k chunks mais relevantes.
    """
    # Validação de variáveis de ambiente
    db_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    if not db_url or not collection_name:
        raise EnvironmentError("Variáveis de ambiente DATABASE_URL e PG_VECTOR_COLLECTION_NAME são obrigatórias.")

    # Vetorização da pergunta
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))
    store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=db_url,
        use_jsonb=True,
    )
    try:
        results = store.similarity_search_with_score(question, k=k)
    except Exception as e:
        logging.error(f"Erro ao consultar PGVector: {e}")
        raise
    # Retorna apenas o texto dos chunks
    return [doc.page_content.strip() for doc, _ in results]
