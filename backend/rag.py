import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_retriever(document_id):

    collection_name = f"doc_{document_id.replace('-', '')}"

    vector_db = Chroma(
        persist_directory="./chroma_db_minilm",
        collection_name=collection_name,
        embedding_function=embeddings
    )

    return vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10
        }
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key
)


def ask_question(question, document_id):

    retriever = get_retriever(document_id)

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    prompt = f"""
You are a helpful PDF assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer is not available in the context, say:

"I could not find the answer in the PDF."

Do not make up information.

Context:

{context}

User Question:

{question}
"""

    response = llm.invoke(prompt)
    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    sources=[]

    for doc in retrieved_docs:
        sources.append({
            "page": doc.metadata.get("page", 0) + 1,
            "text": doc.page_content
        })


    return {
        "answer": answer,
        "sources": sources
    }


def summarize_pdf(document_id):

    collection_name = f"doc_{document_id.replace('-', '')}"

    vector_db = Chroma(
        persist_directory="./chroma_db_minilm",
        collection_name=collection_name,
        embedding_function=embeddings
    )

    # Get all documents/chunks from this PDF
    data = vector_db.get()

    documents = data.get("documents", [])

    context = "\n\n".join(documents)

    prompt = f"""
You are a helpful study assistant.

Create a clear and useful summary of the following PDF content.

Include:
- Main topics
- Important concepts
- Key definitions
- Important points
- Important relationships or conclusions

Use only the information provided below.
Do not add information that is not present in the PDF.

PDF CONTENT:

{context}

Write the summary in a clear, structured format that a student
can use for revision.
"""

    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    return answer

def generate_quiz(document_id):

    collection_name = f"doc_{document_id.replace('-', '')}"

    vector_db = Chroma(
        persist_directory="./chroma_db_minilm",
        collection_name=collection_name,
        embedding_function=embeddings
    )

    # Get all chunks from the PDF
    data = vector_db.get()

    documents = data.get("documents", [])

    context = "\n\n".join(documents)

    prompt = f"""
You are a helpful study assistant.

Create a quiz with 5 multiple-choice questions
based ONLY on the PDF content provided below.

For each question provide:

1. The question
2. Four options labeled A, B, C, D
3. The correct answer
4. A short explanation of why it is correct

Important:
- Use ONLY information from the PDF.
- Do not invent facts.
- Make the questions useful for a student preparing for an exam.
- Cover different topics from the PDF when possible.

Return the quiz in this format:

### Question 1
What is ...?

- A. ...
- B. ...
- C. ...
- D. ...

**Answer:** B

**Explanation:** ...

PDF CONTENT:

{context}
"""

    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    return answer