# 🔍 ReviewLens AI — Business Review Analyzer

An AI-powered application that fetches business reviews, analyzes them using RAG (Retrieval-Augmented Generation), and delivers a structured **Pros & Cons summary**.

## 🏗️ Architecture

```
User Query → Streamlit UI → Orchestrator Agent
                                    ↓
                            Review Fetcher (SerpApi / Sample Data)
                                    ↓
                            ChromaDB Vector Store (Embeddings)
                                    ↓
                            RAG Retriever (Semantic Search)
                                    ↓
                            Summarizer Agent (Gemini AI)
                                    ↓
                            Structured Pros & Cons Summary
```

## 🛠️ Technologies Used

| Technology | Role |
|---|---|
| **Google ADK** | Agent framework for orchestration |
| **RAG** | Retrieval-Augmented Generation pipeline |
| **ChromaDB** | Vector database for semantic search |
| **Gemini AI** | LLM for review analysis & summarization |
| **SerpApi** | Google Maps review fetching (optional) |
| **Streamlit** | Modern web frontend |
| **n8n** | Optional automation workflow |

## 📦 Setup & Installation

### 1. Clone the repository
```bash
cd "e:\Mini project -ai"
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
# Copy the example env file
copy .env.example .env
```

Edit `.env` and add your API keys:
- **GOOGLE_API_KEY** : Get from [Google AI Studio](https://aistudio.google.com/apikey)
- **SERPAPI_KEY** : Get from [SerpApi](https://serpapi.com). Leave blank to use sample data.

### 5. Run the application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🚀 Usage

1. Enter a business name (e.g., "Taj Palace Hotel Mumbai")
2. Click **Analyze**
3. The AI will:
   - Fetch reviews (from SerpApi or sample data)
   - Store them in ChromaDB with embeddings
   - Retrieve relevant reviews using RAG
   - Generate a Pros & Cons summary with Gemini

### Sample Businesses (works without API keys)
- 🏨 Taj Palace Hotel Mumbai
- 🍽️ Bombay Canteen
- ☕ Blue Tokai Coffee Roasters Koramangala

## 📂 Project Structure

```
├── app.py                      # Streamlit frontend
├── agents/
│   ├── orchestrator.py         # Main pipeline orchestration
│   └── summarizer.py           # Summarizer agent instructions
├── tools/
│   ├── review_fetcher.py       # SerpApi + sample data fetcher
│   └── rag_retriever.py        # ChromaDB semantic search
├── vectorstore/
│   ├── embeddings.py           # Gemini embedding generation
│   └── chroma_store.py         # ChromaDB operations
├── data/
│   └── sample_reviews.json     # Demo review data
├── n8n/
│   └── review_ingestion_workflow.json  # n8n automation
├── requirements.txt
├── .env.example
└── README.md
```

## 🔄 n8n Workflow (Optional)

An n8n workflow is included for automated review ingestion:

1. Import `n8n/review_ingestion_workflow.json` into your n8n instance
2. Configure the SerpApi credentials
3. The workflow runs daily to fetch new reviews and store them in ChromaDB

## 📝 License

This project is built for educational purposes as part of an AI Mini Project.
