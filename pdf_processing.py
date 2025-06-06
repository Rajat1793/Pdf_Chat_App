import tempfile
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def process_pdf(file_bytes, file_hash, file_name):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = Path(tmp_file.name)

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    # vector_db = QdrantVectorStore.from_documents(
    #     documents=split_docs,
    #     url="http://localhost:6333",
    #     collection_name="learning_ vectors",
    #     embedding=embedding_model,
    #     force_recreate=True
    # )
    
    # Use FAISS instead of Chroma and Qdrant
    vector_db = FAISS.from_documents(
        documents=split_docs,
        embedding=embedding_model
    )
    return vector_db