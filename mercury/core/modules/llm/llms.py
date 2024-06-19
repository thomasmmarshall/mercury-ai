from typing import Any, Dict

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from mercury.core.modules.document_store.loader import format_docs


async def rag_agent(model: Any, vector_db: Any, top_k: int = 3) -> RunnablePassthrough:

    # TODO: Implement conversational memory buffer for RAG agent

    """
    Creates a runnable pipeline for retrieval-augmented generation (RAG).

    Args:
        model (Any): The model used for generation.
        vector_db (Any): The vector database used for retrieval.

    Returns:
        RunnablePassthrough: The runnable pipeline for RAG.
    """
    # Define the template for retrieval-augmented generation (RAG)
    template = """You are Hermes, a helpful assistant. Answer the question based only on the following context:

    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Create a retriever from the vector database
    retriever = vector_db.as_retriever(search_kwargs={"k": top_k})

    # Define the runnable pipeline
    runnable = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    return runnable


async def chat_agent(model: Any) -> RunnablePassthrough:

    # TODO: Implement conversational memory buffer for chat agent

    # Define the template for retrieval-augmented generation (RAG)
    template = """You are Hermes, a helpful assistant. Please answer the user's question as best you can.
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Define the runnable pipeline
    runnable = prompt | model | StrOutputParser()

    return runnable


async def rag_memory(model: Any, vector_db: Any, top_k: int = 3) -> RunnablePassthrough:

    SYSTEM_TEMPLATE = """
    Answer the user's questions based on the below context. 
    If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

    <context>
    {context}
    </context>
    """

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    def parse_retriever_input(params: Dict):
        return params["messages"][-1].content

    # Create a retriever from the vector database
    retriever = vector_db.as_retriever(search_kwargs={"k": top_k})

    # Document chain
    document_chain = create_stuff_documents_chain(model, question_answering_prompt)

    # Retrieval chain
    retrieval_chain = RunnablePassthrough.assign(
        context=parse_retriever_input | retriever,
    ).assign(
        answer=document_chain,
    )

    # add string output parser
    return retrieval_chain | StrOutputParser()
