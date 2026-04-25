
import os
import logging
from dotenv import load_dotenv
import sys
from langchain_google_genai import ChatGoogleGenerativeAI

# Ajusta o sys.path para garantir import do search.py ao rodar diretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from search import search_question

load_dotenv()

PROMPT_TEMPLATE = '''\
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
	"Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
'''

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    while True:
        try:
            question = input("\nFaça sua pergunta (ou 'sair' para encerrar):\n\nPERGUNTA: ")
            if question.strip().lower() in ("sair", "exit", "quit"):
                print("Encerrando...")
                break
            context_chunks = search_question(question)
            context = "\n".join(context_chunks)
            prompt = PROMPT_TEMPLATE.format(context=context, question=question)

            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
            response = llm.invoke(prompt)
            answer = response.content.strip() if hasattr(response, 'content') else str(response)
            print(f"RESPOSTA: {answer}\n")
        except Exception as e:
            logging.error(f"Erro: {e}")
            print(f"Erro: {e}\n")

if __name__ == "__main__":
    main()
