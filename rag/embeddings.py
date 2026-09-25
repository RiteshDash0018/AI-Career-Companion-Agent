import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "openai/text-embedding-3-small"
)


def create_embedding(text):
    """
    Convert text into a numerical embedding vector.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts):
    """
    Convert multiple texts into embedding vectors.
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]