from rag.embeddings import create_embedding


text = "Machine Learning Intern requiring Python and model development"

embedding = create_embedding(text)

print("Embedding created successfully!")
print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])