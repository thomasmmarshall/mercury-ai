import shutil

import chainlit as cl
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Mercury functions
from mercury.core.modules.document_store.loader import process_documents
from mercury.core.modules.llm.llms import chat_agent, rag_agent
from mercury.core.utils.misc import load_secrets

# Define the path to the secrets file
SECRETS_FILE_PATH = "./app/secrets.json"

# Define the deployment name of the language model
LLM_DEPLOYMENT = "gpt-4-turbo"
TEMPERATURE = 0.0

# Define the chunk size and overlap for the text splitter
MAX_DOCUMENTS = 100
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 3

# Define the path to the PDF storage directory
DOCUMENT_STORAGE_PATH = "./app/data/"


# ------------------------ ChainLit Init Start ------------------------ #
def init(RAG=False):
    """
    This function is called when a user logs in.

    It performs the initial setup, defines the language model, initializes the vector store and retriever,
    and creates a LangChain runnable object for the agent.

    Returns:
        None
    """
    # Load the secrets
    load_secrets(SECRETS_FILE_PATH)

    if RAG:
        # Do initial setup here
        print("Setting up models and vector stores...")
        embedder = OpenAIEmbeddings()

        # Initialise vector store and retriever
        vector_db = process_documents(
            data_directory=DOCUMENT_STORAGE_PATH,
            chunk_overlap=CHUNK_OVERLAP,
            chunk_size=CHUNK_SIZE,
            embeddings=embedder,
        )

        # Define the language model
        llm = ChatOpenAI(
            model_name=LLM_DEPLOYMENT, temperature=TEMPERATURE, streaming=True
        )

        return llm, vector_db

    else:
        print("Setting up models only...")

        # Define the language model
        llm = ChatOpenAI(
            model_name=LLM_DEPLOYMENT, temperature=TEMPERATURE, streaming=True
        )

        return llm


async def assistant_chat():
    """
    This function is called when the user selects the assistant chat profile.

    Returns:
        None
    """
    # Initialise the language model and vector store
    llm = init(RAG=False)

    # Create a LangChain runnable object for the agent
    runnable = await chat_agent(llm)

    # Save the runnable object to the user session
    cl.user_session.set("runnable", runnable)

    msg = cl.Message(
        content="Hello! What can I help you with?",
        disable_feedback=False,
    )
    await msg.send()


async def document_chat():
    """
    This function is called when the user selects the document chat profile.

    Returns:
        None
    """
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload PDF files to begin!",
            accept=["pdf"],
            max_size_mb=20,
            timeout=180,
            max_files=MAX_DOCUMENTS,
        ).send()

    # Send a message to the user re document processing
    msg = cl.Message(
        content=f"""Processing and saving `{len(files)}` files...\n """,
        disable_feedback=True,
    )
    await msg.send()

    # Save files to local directory
    for file in files:
        print(f"Processing file: {file.name}")

        # Copy file from file.path to DOCUMENT_STORAGE_PATH
        shutil.copy(file.path, DOCUMENT_STORAGE_PATH + file.name)

        # Send a message to the user re file processing
        msg.content += f"- `{file.name}`\n"
        await msg.update()

    # Initialise the language model and vector store
    llm, vector_db = init(RAG=True)

    # Create a LangChain runnable object for the agent
    runnable = await rag_agent(llm, vector_db, TOP_K)

    # Save the runnable object to the user session
    cl.user_session.set("runnable", runnable)

    msg = cl.Message(
        content="Hello! What questions do you have about the uploaded documents?",
        disable_feedback=False,
    )
    await msg.send()
