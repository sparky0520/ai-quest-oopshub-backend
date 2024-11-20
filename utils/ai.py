from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_DIR = "./chroma_db"


vectorstore = Chroma(
    collection_name="questions_answers",
    persist_directory=CHROMA_DB_DIR, 
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"),
)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

PROMPT_TEMPLATE = """
You are a bot to answer questions in a company.
Use the following context to answer the question.


{context}

---
Answer the question without using the word context: {question}

If you do create up an answer without using anything from the context, say you might not be 100% sure.
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
setup_and_retrieval = RunnableParallel(
    {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
)

output_parser = StrOutputParser()
qa_chain = setup_and_retrieval | prompt | llm | output_parser

# TODO: only fetch docs that have the same company id
async def generate_ai_answer(question_title: str, question_description: str) -> str:
    query = f"{question_title}\n{question_description}"
    try:
        response = await qa_chain.ainvoke(query)
        return response
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# TODO: use docs to store answers with metadata
async def add_to_db(question_title: str, question_description: str, answer: str) -> bool:
    try:
        await vectorstore.aadd_texts(texts=[f"Question:{question_title}\n{question_description}\n------\nAnswer:{answer}\n------\n"])
        return True
    except Exception as e:
        print(f"Error adding to database: {str(e)}")
        return False
