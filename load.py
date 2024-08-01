import os
import shutil
import time
import random
import hashlib
from openai import RateLimitError
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import Document
from langchain_chroma import Chroma

os.environ['OPENAI_API_KEY'] = 'e05202e4665242a9aa5f75ff4e1ca082'

CHROMA_PATH = "chroma"
DATA_PATH = "masterDB"
CHUNK_SIZE = 2048
BATCH_SIZE = 10

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = create_chunks(documents)
    print_documents(chunks)
    save_to_chroma(chunks)

def load_documents():
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith('.txt') or filename.endswith('.md'):
            file_path = os.path.join(DATA_PATH, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    doc = Document(page_content=content, metadata={"source": file_path})
                    documents.append(doc)
            except Exception as e:
                print(f"Error loading file {file_path}: {str(e)}")
    print(f"Loaded {len(documents)} documents.")
    return documents

def create_chunks(documents):
    chunks = []
    for doc in documents:
        text = doc.page_content
        metadata = doc.metadata
        doc_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        metadata["hash"] = doc_hash
        for i in range(0, len(text), CHUNK_SIZE):
            chunk_text = text[i:i + CHUNK_SIZE]
            chunk = Document(page_content=chunk_text, metadata=metadata)
            chunks.append(chunk)
    print(f"Created {len(chunks)} chunks.")
    return chunks

def print_documents(documents):
    print(f"Loaded {len(documents)} document(s).")
    for i, doc in enumerate(documents):
        print(f"Document {i + 1} structure: {type(doc)}")
        preview = doc.page_content[:100]
        print(f"Document {i + 1} content preview: {preview}...")

def save_to_chroma(documents):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    embeddings = AzureOpenAIEmbeddings(
        openai_api_key=openai_api_key,
        api_version="2024-03-01-preview",
        base_url="https://flexapimanager.flex.com/openai/v2",
        default_headers={"Ocp-Apim-Subscription-Key": openai_api_key},
        model="embedding"
    )

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    existing_docs = db.get()
    existing_hashes = {doc.metadata["hash"] for doc in existing_docs['documents']} if 'documents' in existing_docs else set()

    new_documents = [doc for doc in documents if doc.metadata["hash"] not in existing_hashes]

    for i in range(0, len(new_documents), BATCH_SIZE):
        batch = new_documents[i:i + BATCH_SIZE]
        retry_with_exponential_backoff(db.add_documents, batch)

    print(f"Saved {len(new_documents)} new document(s) to {CHROMA_PATH}.")

def retry_with_exponential_backoff(func, *args, **kwargs):
    max_retries = 5
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            sleep_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limit exceeded. Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()

# Example code to check the contents of the Chroma database
CHROMA_PATH = "chroma"

openai_api_key = os.environ.get('OPENAI_API_KEY')
embeddings = AzureOpenAIEmbeddings(
    openai_api_key=openai_api_key,
    api_version="2024-03-01-preview",
    base_url="https://flexapimanager.flex.com/openai/v2",
    default_headers={"Ocp-Apim-Subscription-Key": openai_api_key},
    model="embedding"
)
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

all_docs = db.get()
print(f"Total documents in the database: {len(all_docs['documents'])}")

if 'documents' in all_docs:
    for i, doc in enumerate(all_docs['documents']):
        print(f"Document {i + 1} structure: {type(doc)}")
        if isinstance(doc, str):
            print(f"Document {i + 1} content: {doc[:100]}...")
        else:
            print(f"Document {i + 1} is not a string.")
else:
    print("No documents found in the database.")