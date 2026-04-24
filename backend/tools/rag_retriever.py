"""
RAG Retriever Tool — Performs semantic search on stored reviews in ChromaDB.
Returns the most relevant reviews for a given query.
"""

from vectorstore.chroma_store import search_reviews, get_all_reviews_for_business


def retrieve_relevant_reviews(query: str, business_name: str = "", top_k: int = 15) -> str:
    """
    Retrieve the most relevant reviews from the vector database using semantic search.

    This function is designed to be used as an ADK tool. It searches ChromaDB
    for reviews that are semantically similar to the query.

    Args:
        query: The search query describing what aspects of the business to analyze
            (e.g., 'service quality and food at Taj Hotel').
        business_name: Optional business name to filter results
            (e.g., 'Taj Palace Hotel Mumbai').
        top_k: Maximum number of reviews to retrieve (default 15).

    Returns:
        A formatted string containing the retrieved reviews with their ratings,
        authors, and dates. Ready to be used as context for summarization.
    """
    # Perform semantic search
    results = search_reviews(
        query=query,
        business_name=business_name if business_name else None,
        top_k=top_k,
    )

    if not results:
        return f"No reviews found for '{business_name or query}' in the database. Please fetch reviews first using the review fetcher tool."

    # Format results as a readable context string for the LLM
    formatted_reviews = []
    for i, review in enumerate(results, 1):
        stars = "⭐" * int(review["rating"])
        formatted_reviews.append(
            f"Review #{i} | Rating: {review['rating']}/5 {stars} | "
            f"Author: {review['author']} | Date: {review['date']}\n"
            f"{review['text']}"
        )

    header = f"=== Retrieved {len(results)} reviews for '{results[0].get('business_name', business_name)}' ===\n"
    return header + "\n\n---\n\n".join(formatted_reviews)
