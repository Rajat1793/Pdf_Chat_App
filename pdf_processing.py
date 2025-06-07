import tempfile
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.vectorstores import Chroma

embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def process_pdf(file_bytes, file_hash, file_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = Path(tmp_file.name)

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    # using chromaDB as streamlit cloud doest support Qdrant on docker 
    # vector_db = QdrantVectorStore.from_documents(
    #     documents=split_docs,
    #     url="http://localhost:6333",
    #     collection_name="learning_ vectors",
    #     embedding=embedding_model,
    #     force_recreate=True
    # )
    
    # Use a persistent directory for ChromaDB
    persist_directory = f"chroma_db_{file_hash}"
    vector_db = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    vector_db.persist()
    return vector_db