from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from playbook_product_review.data_converter import dataconverter

from dotenv import load_dotenv

import os


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ASTRA_DB_API_ENDPOINT = os.getenv("ASTREA_DB_API_ENDPOINT")

ASTRA_DB_APPLICATION_TOKEN = os.getenv(
    "ASTREA_DB_APPICATION_TOKEN"
)

ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")


# =========================================================
# HuggingFace Embeddings
# =========================================================

embeddings = HuggingFaceEndpointEmbeddings(
    huggingfacehub_api_token=HUGGINGFACE_TOKEN,
    model="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# Data Ingestion Function
# =========================================================

def data_ingestion(status):

    # Create AstraDB Vector Store
    vstore = AstraDBVectorStore(

        embedding=embeddings,

        collection_name="playbook_product_review",

        api_endpoint=ASTRA_DB_API_ENDPOINT,

        token=ASTRA_DB_APPLICATION_TOKEN,

        namespace=ASTRA_DB_KEYSPACE
    )

    # =====================================================
    # Insert Documents
    # =====================================================

    if status == "none":

        docs = dataconverter()

        insert_ids = vstore.add_documents(docs)

        return vstore, insert_ids

    else:

        return vstore


# =========================================================
# Main Execution
# =========================================================

if __name__ == "__main__":

    vstore, insert_ids = data_ingestion("none")

    print(f"\n[SUCCESS] Inserted {len(insert_ids)} documents")

    # Similarity Search
    result = vstore.similarity_search(
        "can you tell me the low budget sound basshead set?",
        k=3
    )

    # Print Results
    for res in result:

        print(f"\n{res.page_content}")

        print(f"\nMetadata: {res.metadata}")