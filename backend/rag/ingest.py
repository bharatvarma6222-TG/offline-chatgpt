from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


def ingest_pdf(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    # Embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # Create vector database
    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    # Save locally
    vectorstore.save_local("faiss_index")

    return "PDF processed successfully"
