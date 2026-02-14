import os
from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_store = Chroma(
    collection_name="research_docs",
    embedding_function=embeddings,
    persist_directory=os.getenv("CHROMA_DIR", "./chroma_db"),
)

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20,
        length_function = len,
        separators = ['\n\n', '\n', ' ', '']
    )

# add text into the DB  ( add Raw Text)
def add_document(text: str):
    chunks = text_splitter.split_text(text)
    vector_store.add_texts(chunks)

# # this function for add PDF files. (add data manually)
def add_pdf(file_path: str):
    try:
        reader = PdfReader(file_path)

        full_text = ""
        for page in reader.pages:
            if page.extract_text():
                full_text += page.extract_text() + "\n"

        chunks = text_splitter.split_text(full_text)

        vector_store.add_texts(chunks)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

file_path = os.getenv("pdf_file_path")
add_pdf(file_path)

# semantic search
def semantic_search(query: str, k: int = 3):
    docs = vector_store.similarity_search(query, k=k)
    return "\n".join(d.page_content for d in docs)