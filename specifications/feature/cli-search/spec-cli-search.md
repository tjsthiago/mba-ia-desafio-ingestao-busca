(# Especificação Técnica — CLI Search)

## 1. Visão Geral
Implementar uma interface de linha de comando (CLI) para que o usuário possa realizar perguntas baseadas exclusivamente no conteúdo de um PDF previamente ingerido, utilizando LangChain, PostgreSQL + pgVector e LLMs.

---

## 2. Requisitos Funcionais

### 2.1. Entrada do Usuário
- O usuário deve ser capaz de digitar perguntas no terminal.
- O sistema deve aceitar perguntas em português natural.

### 2.2. Processamento
1. **Vetorizar a pergunta** usando o mesmo modelo de embeddings utilizado na ingestão (`text-embedding-3-small`).
2. **Buscar os 10 chunks mais relevantes** no banco vetorial (PGVector) via similaridade de embeddings.
3. **Montar o prompt** conforme template do PRD, concatenando os resultados do banco.
4. **Chamar a LLM** (modelo: `gpt-5-nano`) para gerar a resposta, seguindo as regras do prompt.
5. **Exibir a resposta** ao usuário no terminal.

### 2.3. Restrições
- A resposta deve ser baseada **exclusivamente** no contexto retornado do banco vetorial.
- Se a resposta não estiver no contexto, retornar: "Não tenho informações necessárias para responder sua pergunta."
- Não utilizar conhecimento externo ou opiniões.
- Utilize os mesmos imports e classes que são utilizados no [Exemplo de busca PGVector](../../../../mba-ia-niv-introducao-langchain/5-loaders-e-banco-de-dados-vetoriais/4-search-vector.py)
- A conexão do banco de dados estárá no .env como nome DATABASE_URL
- a execução do arquivo chat.py será feita com o comando `python src/chat.py` então utilize imports que funcionem ao chamar search.py a partir de chat.py

---

## 3. Requisitos Não Funcionais

- Código em Python 3.10+.
- Utilizar boas práticas de modularização, tipagem e logging.
- Utilizar variáveis de ambiente para segredos e configurações sensíveis.
- Seguir as recomendações de código seguro e limpo do [OpenAI Python Best Practices](https://context7.com/openai/openai-python).
- Utilizar tratamento de erros robusto para falhas de conexão, variáveis ausentes e respostas inesperadas.

---

## 4. Estrutura dos Arquivos

- `src/search.py`: Função de busca vetorial (consulta PGVector e retorna contexto).
- `src/chat.py`: Interface CLI, orquestra o fluxo pergunta → busca → prompt → LLM → resposta.
- `src/ingest.py`: (Já existente) Responsável pela ingestão do PDF e persistência dos embeddings.

---

## 5. Fluxo Detalhado

1. **Usuário digita a pergunta** no terminal (via `chat.py`).
2. `chat.py` chama função de busca em `search.py`.
3. `search.py`:
		- Vetoriza a pergunta.
		- Consulta PGVector (k=10).
		- Retorna os textos dos chunks mais relevantes.
4. `chat.py` monta o prompt conforme template do PRD.
5. `chat.py` chama a LLM (gpt-5-nano) via LangChain.
6. Exibe a resposta ao usuário.

---

## 6. Exemplo de Prompt para LLM

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
````

---

## 7. Exemplo de Uso no Terminal

```
Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

---

## 8. Validação e Testes

- Testar perguntas dentro e fora do contexto do PDF.
- Validar tratamento de erros para variáveis de ambiente ausentes, falha de conexão com banco e resposta da LLM.
- Garantir que o código siga as recomendações de segurança e boas práticas do OpenAI Python Best Practices.

---

## 9. Referências

- [PRD - CLI Search](./prd-cli-search.md)
- [Projeto com exemplos de utilização de LangChain e PGVector](../../../../mba-ia-niv-introducao-langchain)
- [Exemplo de busca PGVector](../../../../mba-ia-niv-introducao-langchain/5-loaders-e-banco-de-dados-vetoriais/4-search-vector.py)
- [OpenAI Python Best Practices](https://context7.com/openai/openai-python)
