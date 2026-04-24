"""
Embedding generation using Google's Gen AI SDK (google-genai).
Converts review text into vector embeddings for storage in ChromaDB.
"""

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Create the Gen AI client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

EMBEDDING_MODEL = "gemini-embedding-001"


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text strings using Gemini's embedding model.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (each a list of floats).
    """
    if not texts:
        return []

    # Process in batches of 100 (API limit)
    all_embeddings = []
    batch_size = 100

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
        )
        for embedding in response.embeddings:
            all_embeddings.append(embedding.values)

    return all_embeddings


def get_query_embedding(query: str) -> list[float]:
    """
    Generate an embedding for a search query.

    Args:
        query: The search query string.

    Returns:
        Embedding vector as a list of floats.
    """
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
    )
    return response.embeddings[0].values
