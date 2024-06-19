from pathlib import Path
from typing import Any, List

from langchain.indexes import SQLRecordManager, index
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma


def process_documents(
    data_directory: str, chunk_size=1024, chunk_overlap=50, embeddings: Any = None
) -> Chroma:
    """
    Process the uploaded files by saving them to disk, loading the data, splitting it into chunks,
    creating a vector store, indexing the documents, and returning the vector index.

    Parameters:
    - uploaded_files (List[Any]): The list of uploaded files.
    - chunk_size (int): The size of each chunk for splitting the text into chunks for embedding. Default is 1024.
    - chunk_overlap (int): The overlap between consecutive chunks. Default is 50.

    Returns:
    - vector_index (Chroma): The vector index created from the processed documents.
    """

    # Load the data from the saved files
    loaded_documents = load_documents(data_directory)

    # Split text into chunks for embedding
    chunked_docs = split_chunks(loaded_documents, chunk_size, chunk_overlap)

    # Create a vector store and index the documents
    vector_index = Chroma.from_documents(chunked_docs, embeddings)

    # Create a record manager
    namespace = "chromadb/my_documents"
    record_manager: SQLRecordManager = SQLRecordManager(
        namespace, db_url="sqlite:///record_manager_cache.sql"
    )
    record_manager.create_schema()

    # Index the documents
    index_result = index(
        chunked_docs,
        record_manager,
        vector_index,
        cleanup="incremental",
        source_id_key="source",
    )

    print(f"Indexing stats: {index_result}")

    return vector_index


def load_documents(data_directory: str) -> List[Any]:
    """
    Loads documents from the specified file paths.

    Parameters:
    - file_paths (List[str]): The list of file paths to load the documents from.

    Returns:
    - List[Any]: The list of loaded documents.
    """

    # loader = DirectoryLoader(
    #     data_directory, show_progress=True, use_multithreading=True
    # )
    # loaded_documents = loader.load()

    # return loaded_documents

    pdf_directory = Path(data_directory)
    docs = []  # type: List[Document]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for pdf_path in pdf_directory.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
        docs += text_splitter.split_documents(documents)

    return docs


def split_chunks(
    concatenated_content: str, chunk_size=2500, chunk_overlap=0
) -> List[str]:
    """
    Splits the given `concatenated_content` into chunks of specified size.

    Args:
        concatenated_content (str): The content to be split into chunks.
        chunk_size (int, optional): The size of each chunk. Defaults to 1000.
        chunk_overlap (int, optional): The amount of overlap between adjacent chunks. Defaults to 0.

    Returns:
        List[str]: A list of strings, where each string represents a chunk of the `concatenated_content`.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Notice that you can .split_documents(), or .split_text()
    document_leafs = text_splitter.split_documents(concatenated_content)

    return document_leafs


def format_docs(docs: List[Document]) -> str:
    """
    Formats the page content of a list of documents.

    Args:
        docs (List[Document]): A list of documents.

    Returns:
        str: The formatted page content of the documents, separated by two newlines.
    """
    return "\n\n".join([d.page_content for d in docs])
