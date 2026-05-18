from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


def retrieve_context(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = vectorstore.similarity_search(
        query,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context
