import json

from rag.job_documents import job_to_document
from rag.chunker import chunk_documents
from rag.vector_store import add_documents, search_jobs


# --------------------------------------------------
# 1. Load internship dataset
# --------------------------------------------------

def load_jobs():
    """
    Load internship/job postings from jobs.json.
    """

    with open(
        "data/jobs.json",
        "r",
        encoding="utf-8"
    ) as file:
        jobs = json.load(file)

    return jobs


# --------------------------------------------------
# 2. Build the RAG knowledge base
# --------------------------------------------------

def build_knowledge_base():
    """
    Convert job postings into documents,
    split them into chunks, generate embeddings,
    and store them in ChromaDB.
    """

    jobs = load_jobs()

    print("Total jobs loaded:", len(jobs))

    documents = [
        job_to_document(job)
        for job in jobs
    ]

    print("Documents created:", len(documents))

    chunks = chunk_documents(documents)

    print("Chunks created:", len(chunks))

    add_documents(chunks)

    print("Jobs successfully added to ChromaDB!")

    return len(jobs), len(documents), len(chunks)


# --------------------------------------------------
# 3. Test semantic search
# --------------------------------------------------

def test_semantic_search():
    """
    Test semantic search using multiple natural-language queries.
    """

    test_queries = [
        "Python machine learning internship for a B.Tech computer science student",

        "Frontend development internship using React JavaScript and HTML",

        "Cybersecurity internship involving network security and ethical hacking",

        "Cloud DevOps internship using AWS Docker and Kubernetes"
    ]

    for test_number, query in enumerate(test_queries, start=1):

        print("\n" + "=" * 60)
        print(f"SEMANTIC SEARCH TEST {test_number}")
        print("=" * 60)

        print("\nSearch Query:")
        print(query)

        results = search_jobs(
            query,
            top_k=5
        )

        print("\nTop 5 Relevant Jobs:")
        print("--------------------")

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        for index, metadata in enumerate(
            metadatas,
            start=1
        ):
            print(
                f"{index}. "
                f"{metadata.get('title')} "
                f"- {metadata.get('company')} "
                f"- {metadata.get('location')}"
            )


# --------------------------------------------------
# 4. Run knowledge-base creation and testing
# --------------------------------------------------

if __name__ == "__main__":

    test_semantic_search()