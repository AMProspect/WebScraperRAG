# Original Code from https://github.com/pixegami/rag-tutorial-v2
# Edits made by Alkis Morellas

import argparse
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from companies import c


CHROMA_PATH = "chroma"
DATA_PATH = "Data"
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
embeddings = OpenAIEmbeddings()

change = ['7-Eleven, Inc', 'Alsco, Inc', 'Amarr Company, Inc', 'Aramark SCM, Inc', 'Arkema, Inc',
          'Avanath Communities, Inc', 'AvantStay, Inc', 'Baker Distributing Co., LLC', ]



PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

GET_COMPANY = """
Given the following question:

{question}

---

What company are they talking about from this list of companies: {companies}

Just respond with the company name as it is in the list.
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    response = query_rag(query_text)
    print(response)
    return



def query_rag(query_text: str):
    # Prepare the DB.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # print(results)

    model = init_chat_model("gpt-4o-mini", model_provider="openai")

    prompt_template = ChatPromptTemplate.from_template(GET_COMPANY)
    prompt = prompt_template.format(question=query_text, companies=c)

    company = model.invoke(prompt)

    if company.content[-1] == '.':
        file_path = f"Data\\{company.content[:-1]}\\{company.content}.pdf"
    else:
        file_path = f"Data\\{company.content}\\{company.content}.pdf"

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5, filter={"source": file_path})
    

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    # print(prompt)
    # print(sources)

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    # print(formatted_response)
    return response_text.content


if __name__ == "__main__":
    main()
