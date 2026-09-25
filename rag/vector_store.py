import chromadb
from rag.embeddings import create_embeddings


# Create a local ChromaDB database
client = chromadb.PersistentClient(path="data/chroma_db")

# Create or open the jobs collection
collection = client.get_or_create_collection(
    name="internship_jobs"
)


def add_documents(documents):
    """
    Add job documents and their embeddings to ChromaDB.
    """

    if not documents:
        print("No documents found.")
        return

    texts = [doc.page_content for doc in documents]

    print(f"Generating embeddings for {len(texts)} chunks...")

    embeddings = create_embeddings(texts)

    ids = [
        f"{doc.metadata['job_id']}_{index}"
        for index, doc in enumerate(documents)
    ]

    metadatas = [doc.metadata for doc in documents]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Successfully added {len(documents)} chunks to ChromaDB.")


def search_jobs(query, top_k=5):
    """
    Search ChromaDB for jobs related to the query.
    """

    query_embedding = create_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


def get_collection_count():
    """
    Return the number of chunks currently stored in ChromaDB.
    """

    return collection.count()