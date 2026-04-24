"""
ChromaDB vector store for storing and retrieving business reviews.
Handles embedding storage, semantic search, and persistence.
"""

import chromadb
from chromadb.config import Settings
import os
import hashlib

from vectorstore.embeddings import get_embeddings, get_query_embedding

# Persistent storage directory for ChromaDB
CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")


def get_chroma_client():
    """Get a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_or_create_collection(client=None):
    """
    Get or create the 'business_reviews' collection in ChromaDB.

    Args:
        client: Optional ChromaDB client. Creates one if not provided.

    Returns:
        ChromaDB collection object.
    """
    if client is None:
        client = get_chroma_client()

    collection = client.get_or_create_collection(
        name="business_reviews",
        metadata={"description": "Business reviews for RAG-based analysis"},
    )
    return collection


def _generate_review_id(review: dict) -> str:
    """Generate a unique ID for a review based on its content."""
    content = f"{review.get('business_name', '')}-{review.get('author', '')}-{review.get('text', '')[:100]}"
    return hashlib.md5(content.encode()).hexdigest()


def add_reviews(business_name: str, reviews: list[dict]) -> int:
    """
    Embed and store reviews in ChromaDB.

    Args:
        business_name: Name of the business.
        reviews: List of review dicts with keys: text, rating, author, date.

    Returns:
        Number of reviews added (skips duplicates).
    """
    if not reviews:
        return 0

    collection = get_or_create_collection()

    # Prepare data for insertion
    texts = []
    ids = []
    metadatas = []

    for review in reviews:
        review_id = _generate_review_id(review)

        # Check if already exists
        existing = collection.get(ids=[review_id])
        if existing and existing["ids"]:
            continue

        review_text = review.get("text", "")
        texts.append(review_text)
        ids.append(review_id)
        metadatas.append({
            "business_name": review.get("business_name", business_name),
            "author": review.get("author", "Anonymous"),
            "rating": review.get("rating", 0),
            "date": review.get("date", "Unknown"),
        })

    if not texts:
        return 0

    # Generate embeddings
    embeddings = get_embeddings(texts)

    # Add to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

    return len(texts)


def search_reviews(query: str, business_name: str = None, top_k: int = 15) -> list[dict]:
    """
    Perform semantic similarity search on stored reviews.

    Args:
        query: Search query string.
        business_name: Optional filter by business name.
        top_k: Number of results to return.

    Returns:
        List of dicts with keys: text, rating, author, date, business_name, distance.
    """
    collection = get_or_create_collection()

    # Check if collection has any data
    if collection.count() == 0:
        return []

    # Generate query embedding
    query_embedding = get_query_embedding(query)

    # Build where filter if business_name is provided
    where_filter = None
    if business_name:
        where_filter = {"business_name": {"$eq": business_name}}

    # Perform search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    # Format results
    formatted = []
    if results and results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            formatted.append({
                "text": results["documents"][0][i],
                "rating": results["metadatas"][0][i].get("rating", 0),
                "author": results["metadatas"][0][i].get("author", "Anonymous"),
                "date": results["metadatas"][0][i].get("date", "Unknown"),
                "business_name": results["metadatas"][0][i].get("business_name", ""),
                "distance": results["distances"][0][i],
            })

    return formatted


def get_all_reviews_for_business(business_name: str) -> list[dict]:
    """
    Retrieve all stored reviews for a specific business.

    Args:
        business_name: Name of the business.

    Returns:
        List of review dicts.
    """
    collection = get_or_create_collection()

    if collection.count() == 0:
        return []

    results = collection.get(
        where={"business_name": {"$eq": business_name}},
        include=["documents", "metadatas"],
    )

    formatted = []
    if results and results["documents"]:
        for i in range(len(results["documents"])):
            formatted.append({
                "text": results["documents"][i],
                "rating": results["metadatas"][i].get("rating", 0),
                "author": results["metadatas"][i].get("author", "Anonymous"),
                "date": results["metadatas"][i].get("date", "Unknown"),
                "business_name": results["metadatas"][i].get("business_name", ""),
            })

    return formatted


def list_businesses() -> list[str]:
    """List all unique business names in the vector store."""
    collection = get_or_create_collection()

    if collection.count() == 0:
        return []

    results = collection.get(include=["metadatas"])
    businesses = set()
    if results and results["metadatas"]:
        for meta in results["metadatas"]:
            businesses.add(meta.get("business_name", "Unknown"))

    return sorted(list(businesses))
