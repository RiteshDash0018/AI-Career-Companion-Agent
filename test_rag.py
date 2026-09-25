import json

from rag.job_documents import job_to_document
from rag.chunker import chunk_documents
from rag.vector_store import add_documents, search_jobs


# --------------------------------------------------
# 1. Load jobs
# --------------------------------------------------

with open(
    "data/jobs.json",
    "r",
    encoding="utf-8"
) as file:

    jobs = json.load(file)


print("Total jobs loaded:", len(jobs))


# --------------------------------------------------
# 2. Convert jobs into LangChain Documents
# --------------------------------------------------

documents = [
    job_to_document(job)
    for job in jobs
]

print("Documents created:", len(documents))


# --------------------------------------------------
# 3. Create text chunks
# --------------------------------------------------

chunks = chunk_documents(documents)

print("Chunks created:", len(chunks))


# --------------------------------------------------
# 4. Store chunks in ChromaDB
# --------------------------------------------------

add_documents(chunks)

print("Jobs successfully added to ChromaDB!")


# --------------------------------------------------
# 5. Test RAG retrieval
# --------------------------------------------------

query = (
    "Python machine learning internship "
    "for a B.Tech student"
)

print("\nSearch Query:")
print(query)

results = search_jobs(
    query,
    top_k=5
)


# --------------------------------------------------
# 6. Display results
# --------------------------------------------------

print("\nTop Relevant Jobs:")
print("------------------")

metadatas = results.get("metadatas", [[]])[0]

for index, metadata in enumerate(metadatas, start=1):

    print(
        f"{index}. "
        f"{metadata.get('title')} "
        f"- {metadata.get('company')}"
    )