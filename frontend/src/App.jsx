import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

const EXAMPLE_BUSINESSES = [
  "The Oberoi Udaivilas Udaipur",
  "Bukhara ITC Maurya Delhi",
  "Barbeque Nation Koramangala Bangalore",
  "Third Wave Coffee Indiranagar Bangalore",
  "Indian Accent New Delhi",
];

const STEPS = [
  { text: "🔍 Searching for business reviews...", time: 0 },
  { text: "📥 Fetching and processing reviews...", time: 1000 },
  { text: "📦 Storing reviews in ChromaDB vector database...", time: 2500 },
  { text: "🔗 Running RAG retrieval for relevant reviews...", time: 4000 },
  { text: "🤖 Gemini AI is analyzing and summarizing...", time: 5500 },
  { text: "✨ Generating pros & cons summary...", time: 7000 },
];

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [reviewsExpanded, setReviewsExpanded] = useState(false);

  const simulateLoadingSteps = () => {
    STEPS.forEach((step, index) => {
      setTimeout(() => {
        setLoadingStep(index);
      }, step.time);
    });
  };

  const handleAnalyze = async (searchQuery = query) => {
    if (!searchQuery) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    setReviewsExpanded(false);
    setLoadingStep(0);
    
    simulateLoadingSteps();

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ business_name: searchQuery }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "An error occurred during analysis.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSentiment = (reviews) => {
    if (!reviews || reviews.length === 0) return { text: "Unknown", emoji: "😐" };
    
    let positive = 0;
    let negative = 0;
    
    reviews.forEach(r => {
      const rating = parseInt(r.rating, 10);
      if (rating >= 4) positive++;
      else if (rating <= 2) negative++;
    });

    if (positive > negative) return { text: "Positive", emoji: "😊" };
    if (negative > positive) return { text: "Negative", emoji: "😔" };
    return { text: "Mixed", emoji: "😐" };
  };

  const getAvgRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, r) => acc + parseInt(r.rating, 10), 0);
    return (sum / reviews.length).toFixed(1);
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-section">
          <h3>📋 How It Works</h3>
          <ul className="sidebar-list">
            <li><strong>1. Enter</strong> a business or place name</li>
            <li><strong>2. Fetch</strong> — Live reviews pulled from Google Maps</li>
            <li><strong>3. Store</strong> — Reviews embedded in ChromaDB vector DB</li>
            <li><strong>4. RAG</strong> — Semantically relevant reviews retrieved</li>
            <li><strong>5. Analyze</strong> — Gemini 2.5 Flash generates pros & cons</li>
          </ul>
        </div>

        <div className="sidebar-section">
          <h3>💡 Try These Examples</h3>
          <ul className="sidebar-list">
            {EXAMPLE_BUSINESSES.map(biz => (
              <li key={biz} style={{ width: '100%' }}>
                <button 
                  className="example-btn"
                  onClick={() => {
                    setQuery(biz);
                    handleAnalyze(biz);
                  }}
                  disabled={loading}
                >
                  📍 {biz}
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="sidebar-section">
          <h3>🛠️ Tech Stack</h3>
          <div className="tech-stack">
            <div className="tech-item">🤖 Google ADK</div>
            <div className="tech-item">✨ Gemini 2.5 Flash</div>
            <div className="tech-item">📦 ChromaDB</div>
            <div className="tech-item">🌐 React Frontend</div>
            <div className="tech-item">⚡ FastAPI Backend</div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="hero">
          <h1>🔍 ReviewLens AI</h1>
          <p>AI-Powered Business Review Analysis with Pros & Cons Summary</p>
          <div className="badges">
            <span className="badge">🤖 Google ADK</span>
            <span className="badge">🔗 RAG Pipeline</span>
            <span className="badge">📦 ChromaDB</span>
            <span className="badge">✨ Gemini AI</span>
          </div>
        </div>

        <div className="search-container">
          <div className="search-input-wrapper">
            <span className="search-icon">🏢</span>
            <input
              type="text"
              className="search-input"
              placeholder="e.g., Taj Palace Hotel Mumbai, Bombay Canteen..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
              disabled={loading}
            />
          </div>
          <button 
            className="analyze-btn" 
            onClick={() => handleAnalyze()}
            disabled={loading || !query}
          >
            🚀 Analyze
          </button>
        </div>

        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <div className="loading-text">{STEPS[Math.min(loadingStep, STEPS.length - 1)].text}</div>
            <div className="loading-subtext">This usually takes about 10-15 seconds</div>
          </div>
        )}

        {!loading && !result && !error && (
          <div className="empty-state">
            <div className="empty-icon">🏢</div>
            <h2>Enter a business name to get started</h2>
            <p>
              ReviewLens AI will fetch reviews, analyze them using RAG and vector search,
              and deliver a comprehensive pros & cons summary powered by Gemini AI.
            </p>
          </div>
        )}

        {result && !loading && (
          <div className="results-container">
            <div className="source-badge">
              🟢 LIVE DATA — Fetched from Google Maps via {result.source === 'serpapi' ? 'SerpApi' : result.source.replace('_', ' ').toUpperCase()}
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-value">{result.review_count}</div>
                <div className="metric-label">Reviews Analyzed</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{getAvgRating(result.reviews)}</div>
                <div className="metric-label">Average Rating ⭐</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{getSentiment(result.reviews).emoji}</div>
                <div className="metric-label">Sentiment: {getSentiment(result.reviews).text}</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">{result.source === 'serpapi' ? '🔗' : '📁'}</div>
                <div className="metric-label">Source: {result.source === 'serpapi' ? 'SerpApi' : result.source.replace('_', ' ').toUpperCase()}</div>
              </div>
            </div>

            <div className="summary-container">
              <h2>🤖 AI Analysis Summary</h2>
              <div className="markdown-body">
                <ReactMarkdown>{result.summary}</ReactMarkdown>
              </div>
            </div>

            <div className="expander">
              <div 
                className="expander-header"
                onClick={() => setReviewsExpanded(!reviewsExpanded)}
              >
                <h3>📄 View All {result.reviews?.length || 0} Raw Reviews</h3>
                <span>{reviewsExpanded ? '▲' : '▼'}</span>
              </div>
              
              {reviewsExpanded && (
                <div className="expander-content">
                  {result.reviews?.map((review, i) => {
                    const rating = parseInt(review.rating, 10);
                    const stars = "⭐".repeat(rating);
                    const color = rating >= 4 ? "#34d399" : (rating === 3 ? "#fbbf24" : "#ef4444");

                    return (
                      <div key={i} className="review-item">
                        <div className="review-header">
                          <div className="review-rating" style={{ color }}>
                            {stars} ({rating}/5)
                          </div>
                          <div className="review-meta">
                            👤 {review.author || 'Anonymous'} · 📅 {review.date || 'Unknown'}
                          </div>
                        </div>
                        <div className="review-text">{review.text || 'No review text'}</div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
