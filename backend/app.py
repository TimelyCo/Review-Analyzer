"""
Business Review Analyzer — Streamlit Frontend
A beautiful, modern UI for analyzing business reviews using AI.
"""

import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ReviewLens AI — Business Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS for Premium Dark Theme ────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hero header */
    .hero-container {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a0aec0;
        font-weight: 300;
        letter-spacing: 0.3px;
    }

    /* Tech badges */
    .tech-badges {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    .tech-badge {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 0.35rem 0.9rem;
        border-radius: 50px;
        font-size: 0.78rem;
        color: #c4b5fd;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }

    /* Result cards */
    .pros-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.04) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .cons-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(220, 38, 38, 0.04) 100%);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(79, 70, 229, 0.04) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Metric cards */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        flex: 1;
        min-width: 140px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.4);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Review item */
    .review-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s ease;
    }
    .review-item:hover {
        border-color: rgba(139, 92, 246, 0.3);
    }
    .review-rating {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .review-text {
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    .review-meta {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.5rem;
    }

    /* Source badge */
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .source-live {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .source-sample {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🔍 ReviewLens AI</div>
    <div class="hero-subtitle">AI-Powered Business Review Analysis with Pros & Cons Summary</div>
    <div class="tech-badges">
        <span class="tech-badge">🤖 Google ADK</span>
        <span class="tech-badge">🔗 RAG Pipeline</span>
        <span class="tech-badge">📦 ChromaDB</span>
        <span class="tech-badge">✨ Gemini AI</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 How It Works")
    st.markdown("""
    1. **Enter** a business or place name
    2. **Fetch** — Live reviews pulled from Google Maps
    3. **Store** — Reviews embedded in ChromaDB vector DB
    4. **RAG** — Semantically relevant reviews retrieved
    5. **Analyze** — Gemini 2.5 Flash generates pros & cons
    """)

    st.markdown("---")
    st.markdown("### 💡 Try These Examples")
    example_businesses = [
        "The Oberoi Udaivilas Udaipur",
        "Bukhara ITC Maurya Delhi",
        "Barbeque Nation Koramangala Bangalore",
        "Third Wave Coffee Indiranagar Bangalore",
        "Indian Accent New Delhi",
    ]
    for biz in example_businesses:
        if st.button(f"📍 {biz}", key=f"example_{biz}", use_container_width=True):
            st.session_state["search_query"] = biz

    st.markdown("---")
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - **Agent**: Google ADK
    - **LLM**: Gemini 2.5 Flash
    - **Vector DB**: ChromaDB
    - **Reviews**: SerpApi (Google Maps)
    - **RAG**: Semantic retrieval pipeline
    """)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#64748b; font-size:0.8rem;'>"
        "Built with ❤️ using ADK + RAG + ChromaDB"
        "</div>",
        unsafe_allow_html=True,
    )


# ─── Main Search Area ────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])

with col1:
    search_query = st.text_input(
        "🏢 Enter Business Name",
        value=st.session_state.get("search_query", ""),
        placeholder="e.g., Taj Palace Hotel Mumbai, Bombay Canteen...",
        label_visibility="collapsed",
    )

with col2:
    analyze_clicked = st.button("🚀 Analyze", use_container_width=True)


# ─── Analysis Logic ──────────────────────────────────────────────────────────
if analyze_clicked and search_query:
    if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your_gemini_api_key_here":
        st.error("⚠️ GOOGLE_API_KEY not found. Please add it to your .env file.")
        st.stop()

    # Progress animation
    progress_container = st.empty()
    status_container = st.empty()

    steps = [
        ("🔍 Searching for business reviews...", 0.15),
        ("📥 Fetching and processing reviews...", 0.30),
        ("📦 Storing reviews in ChromaDB vector database...", 0.50),
        ("🔗 Running RAG retrieval for relevant reviews...", 0.70),
        ("🤖 Gemini AI is analyzing and summarizing...", 0.85),
        ("✨ Generating pros & cons summary...", 0.95),
    ]

    progress_bar = progress_container.progress(0)
    for step_text, step_progress in steps:
        status_container.info(step_text)
        progress_bar.progress(step_progress)
        time.sleep(0.4)

    # Run the actual analysis
    from agents.orchestrator import analyze_business

    result = analyze_business(search_query)

    # Clear progress indicators
    progress_container.empty()
    status_container.empty()

    if result["status"] == "error":
        st.error(f"❌ {result['summary']}")
    else:
        # ── Source Badge ──
        st.markdown(
            '<span class="source-badge source-live">🟢 LIVE DATA — Fetched from Google Maps via SerpApi</span>',
            unsafe_allow_html=True,
        )

        # ── Metrics Row ──
        reviews = result["reviews"]
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
        rating_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for r in reviews:
            rating = int(r.get("rating", 0))
            if rating in rating_counts:
                rating_counts[rating] += 1

        positive = rating_counts[5] + rating_counts[4]
        negative = rating_counts[1] + rating_counts[2]
        sentiment = "Positive" if positive > negative else ("Negative" if negative > positive else "Mixed")
        sentiment_emoji = "😊" if sentiment == "Positive" else ("😔" if sentiment == "Negative" else "😐")

        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-value">{result['review_count']}</div>
                <div class="metric-label">Reviews Analyzed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_rating:.1f}</div>
                <div class="metric-label">Average Rating ⭐</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{sentiment_emoji}</div>
                <div class="metric-label">Sentiment: {sentiment}</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{"🔗" if result['source'] == 'serpapi' else "📁"}</div>
                <div class="metric-label">Source: {result['source'].replace('_', ' ').title()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── AI Summary ──
        st.markdown("---")
        st.markdown(result["summary"])

        # ── Raw Reviews (Expandable) ──
        st.markdown("---")
        with st.expander(f"📄 View All {len(reviews)} Raw Reviews", expanded=False):
            for review in reviews:
                rating = int(review.get("rating", 0))
                stars = "⭐" * rating
                color = "#34d399" if rating >= 4 else ("#fbbf24" if rating == 3 else "#ef4444")

                st.markdown(f"""
                <div class="review-item">
                    <div class="review-rating" style="color: {color};">
                        {stars} ({rating}/5)
                    </div>
                    <div class="review-text">{review.get('text', 'No review text')}</div>
                    <div class="review-meta">
                        👤 {review.get('author', 'Anonymous')} · 📅 {review.get('date', 'Unknown')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Store result in session state
        st.session_state["last_result"] = result

elif not search_query and analyze_clicked:
    st.warning("Please enter a business name to analyze.")

# ─── Empty State ──────────────────────────────────────────────────────────────
if "last_result" not in st.session_state and not analyze_clicked:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #64748b;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🏢</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">
            Enter a business name to get started
        </div>
        <div style="font-size: 0.95rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
            ReviewLens AI will fetch reviews, analyze them using RAG and vector search,
            and deliver a comprehensive pros & cons summary powered by Gemini AI.
        </div>
    </div>
    """, unsafe_allow_html=True)
