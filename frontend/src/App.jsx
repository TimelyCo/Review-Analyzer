import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

const STEPS = [
  { text: "Searching for business reviews...", time: 0 },
  { text: "Fetching and processing reviews...", time: 1000 },
  { text: "Storing reviews in vector database...", time: 2500 },
  { text: "Running retrieval for relevant reviews...", time: 4000 },
  { text: "AI is analyzing and summarizing...", time: 5500 },
  { text: "Generating summary...", time: 7000 },
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
    if (!reviews || reviews.length === 0) return { text: "Unknown" };

    let positive = 0;
    let negative = 0;

    reviews.forEach(r => {
      const rating = parseInt(r.rating, 10);
      if (rating >= 4) positive++;
      else if (rating <= 2) negative++;
    });

    if (positive > negative) return { text: "Positive" };
    if (negative > positive) return { text: "Negative" };
    return { text: "Mixed" };
  };

  const getAvgRating = (reviews) => {
    if (!reviews || reviews.length === 0) return 0;
    const sum = reviews.reduce((acc, r) => acc + parseInt(r.rating, 10), 0);
    return (sum / reviews.length).toFixed(1);
  };

  return (
    <div className="app-container">
      <main className="main-content">
        <div className="header">
          <h1>Review Analyzer</h1>
          <p>Business Review Analysis</p>
        </div>

        <div className="search-container">
          <input
            type="text"
            className="search-input"
            placeholder="Enter a business name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
            disabled={loading}
          />
          <button
            className="analyze-btn"
            onClick={() => handleAnalyze()}
            disabled={loading || !query}
          >
            Analyze
          </button>
        </div>

        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="loading-text">{STEPS[Math.min(loadingStep, STEPS.length - 1)].text}</div>
          </div>
        )}

        {!loading && !result && !error && (
          <div className="empty-state">
            <p>Enter a business name to get started.</p>
          </div>
        )}

        {result && !loading && (
          <div className="results-container">
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Reviews Analyzed</div>
                <div className="metric-value">{result.review_count}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Average Rating</div>
                <div className="metric-value">{getAvgRating(result.reviews)}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Sentiment</div>
                <div className="metric-value">{getSentiment(result.reviews).text}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Source</div>
                <div className="metric-value">{result.source === 'serpapi' ? 'SerpApi' : result.source.replace('_', ' ').toUpperCase()}</div>
              </div>
            </div>

            <div className="summary-container">
              <h2>Analysis Summary</h2>
              <div className="markdown-body">
                <ReactMarkdown>{result.summary}</ReactMarkdown>
              </div>
            </div>

            <div className="expander">
              <button
                className="expander-header"
                onClick={() => setReviewsExpanded(!reviewsExpanded)}
              >
                <span>View Raw Reviews ({result.reviews?.length || 0})</span>
                <span>{reviewsExpanded ? 'Hide' : 'Show'}</span>
              </button>

              {reviewsExpanded && (
                <div className="expander-content">
                  {result.reviews?.map((review, i) => {
                    const rating = parseInt(review.rating, 10);
                    return (
                      <div key={i} className="review-item">
                        <div className="review-header">
                          <span className="review-rating">Rating: {rating}/5</span>
                          <span className="review-meta">
                            {review.author || 'Anonymous'} - {review.date || 'Unknown'}
                          </span>
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