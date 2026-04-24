"""
Orchestrator Agent — Main ADK agent that coordinates review fetching, RAG retrieval,
and summarization. This is the entry point for processing user queries.
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

from tools.review_fetcher import fetch_reviews
from tools.rag_retriever import retrieve_relevant_reviews
from agents.summarizer import SUMMARIZER_INSTRUCTION


def analyze_business(business_name: str, location: str = "") -> dict:
    """
    Full pipeline: Fetch reviews → Store in ChromaDB → RAG retrieve → Summarize.

    This is the main orchestration function that coordinates all components.

    Args:
        business_name: Name of the business to analyze.
        location: Optional location for more specific search.

    Returns:
        Dictionary with keys:
        - status: 'success' or 'error'
        - business_name: The matched business name
        - summary: The AI-generated pros/cons summary (markdown)
        - review_count: Number of reviews analyzed
        - source: Where reviews came from
        - reviews: Raw review data
    """
    try:
        # Create Gen AI client
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        # Step 1: Fetch reviews (SerpApi or sample data)
        fetch_result = fetch_reviews(business_name, location)

        if fetch_result["review_count"] == 0:
            return {
                "status": "error",
                "business_name": business_name,
                "summary": "No reviews found for this business. Please try a different search term.",
                "review_count": 0,
                "source": fetch_result["source"],
                "reviews": [],
            }

        matched_business = fetch_result["business_name"]

        # Step 2: RAG retrieval — get the most relevant reviews
        query = f"Complete analysis of {matched_business} covering service, quality, value, ambiance, and overall experience"
        retrieved_context = retrieve_relevant_reviews(
            query=query,
            business_name=matched_business,
            top_k=20,
        )

        # Step 3: Summarize using Gemini with the summarizer agent instruction
        prompt = f"""Analyze the following reviews for **{matched_business}** and generate a 
comprehensive pros and cons summary.

{retrieved_context}

Now produce the structured summary following the exact format in your instructions."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SUMMARIZER_INSTRUCTION,
                temperature=0.7,
            ),
        )

        return {
            "status": "success",
            "business_name": matched_business,
            "summary": response.text,
            "review_count": fetch_result["review_count"],
            "source": fetch_result["source"],
            "reviews": fetch_result["reviews"],
        }

    except Exception as e:
        return {
            "status": "error",
            "business_name": business_name,
            "summary": f"An error occurred during analysis: {str(e)}",
            "review_count": 0,
            "source": "error",
            "reviews": [],
        }
