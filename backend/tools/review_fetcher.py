"""
Review Fetcher Tool — Fetches Google Maps reviews for a business using SerpApi.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _fetch_from_serpapi(business_name: str, location: str = "") -> list[dict]:
    """
    Fetch reviews from SerpApi's Google Maps Reviews endpoint.

    Args:
        business_name: Name of the business to search for.
        location: Optional location to narrow the search.

    Returns:
        List of review dicts.
    """
    from serpapi import GoogleSearch

    api_key = os.getenv("SERPAPI_KEY", "")
    if not api_key or api_key == "your_serpapi_key_here":
        raise ValueError("SERPAPI_KEY not configured in .env file.")

    # Step 1: Search for the business on Google Maps to get the place data_id
    search_query = f"{business_name} {location}".strip()
    search = GoogleSearch({
        "engine": "google_maps",
        "q": search_query,
        "api_key": api_key,
    })
    results = search.get_dict()

    data_id = ""
    place_name = business_name

    if "place_results" in results:
        data_id = results["place_results"].get("data_id", "")
        place_name = results["place_results"].get("title", business_name)
    elif "local_results" in results and results["local_results"]:
        data_id = results["local_results"][0].get("data_id", "")
        place_name = results["local_results"][0].get("title", business_name)

    if not data_id:
        return []

    # Step 2: Fetch reviews for this place
    reviews_search = GoogleSearch({
        "engine": "google_maps_reviews",
        "data_id": data_id,
        "api_key": api_key,
    })
    reviews_results = reviews_search.get_dict()

    reviews = []
    for review in reviews_results.get("reviews", []):
        reviews.append({
            "business_name": place_name,
            "author": review.get("user", {}).get("name", "Anonymous"),
            "rating": review.get("rating", 0),
            "date": review.get("date", "Unknown"),
            "text": review.get("snippet", review.get("text", "")),
        })

    return reviews


def fetch_reviews(business_name: str, location: str = "") -> dict:
    """
    Fetch live reviews for a business from Google Maps via SerpApi.

    This function is designed to be used as an ADK tool.

    Args:
        business_name: The name of the business or place to search for
            (e.g., 'Taj Palace Hotel Mumbai').
        location: Optional location to narrow the search (e.g., 'Mumbai, India').

    Returns:
        A dictionary containing:
        - source: 'serpapi' (live Google Maps data)
        - business_name: The matched business name
        - review_count: Number of reviews fetched
        - reviews: List of review objects with text, rating, author, date
    """
    from vectorstore.chroma_store import add_reviews

    # Fetch live reviews from SerpApi
    reviews = _fetch_from_serpapi(business_name, location)

    # Store reviews in ChromaDB for RAG retrieval
    if reviews:
        matched_business = reviews[0].get("business_name", business_name)
        count_added = add_reviews(matched_business, reviews)

        return {
            "source": "serpapi",
            "business_name": matched_business,
            "review_count": len(reviews),
            "new_reviews_stored": count_added,
            "reviews": reviews,
        }

    return {
        "source": "serpapi",
        "business_name": business_name,
        "review_count": 0,
        "new_reviews_stored": 0,
        "reviews": [],
    }
