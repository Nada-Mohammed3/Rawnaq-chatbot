# Perfume Recommendation Chatbot

An AI system that takes a customer's question about perfumes (in any language), recommends the best-matching product from a real product catalog, and generates a personalized explanation of why it fits and when to wear it.

---

## AI Stack

| Technology | Role |
|---|---|
| **Sentence Transformers** (`paraphrase-multilingual-mpnet-base-v2`) | Converts text into embeddings for semantic search; supports Arabic, English, and other languages |
| **ChromaDB** | Local vector database storing and searching product embeddings |
| **RAG (Retrieval-Augmented Generation)** | Overall architecture: retrieve relevant real data first, then generate text grounded only in that data |
| **Google Gemini API** (`gemini-3.6-flash`) | Generates the final advice text in Arabic, based strictly on the retrieved product(s), with no invented information |
| **FastAPI** | Exposes everything above as a single API the frontend can call |

---

## Project Structure

```
final project/
├── data/
│   ├── كتالوج_بيع_البرفانات_والمسكات.xlsx   # Original source file
│   └── catalog_clean.xlsx                      # Cleaned data (auto-generated)
├── chroma_db/                                   # Vector database (auto-generated)
├── prepare_data.py          # Cleans and merges the raw data
├── build_embeddings.py      # Converts data into embeddings and stores them
├── search.py                # Semantic search function + season detection/filtering
├── generate_advice.py       # Generates advice text via Gemini
├── main.py                  # FastAPI server (the production API)
├── try_it.py                 # Interactive terminal tool for quick testing
├── requirements.txt          # Required Python packages
├── .env                       # Gemini API key (never committed to version control)
├── API_Documentation.md      # API reference for the frontend developer
└── README_EN.md              # This file
```

---

## Setup From Scratch

### 1) Environment setup

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 2) Gemini API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in and click **Create API Key** (free)
3. Create a `.env` file in the project root containing:
```
GEMINI_API_KEY=your_key_here
```
(no quotes, no spaces around the `=`)

> ⚠️ The `.env` file and the API key are personal — never share them or commit them to GitHub.

### 3) Prepare the data (one-time, or whenever the source file changes)

```powershell
python prepare_data.py
python build_embeddings.py
```

### 4) Run the server

```powershell
uvicorn main:app --reload
```

The server runs at:
```
http://127.0.0.1:8000
```

### 5) Try it out

- **From the browser (recommended):** open `http://127.0.0.1:8000/docs` and test the `/ask` endpoint directly
- **From the terminal:** in a separate terminal (with the venv activated there too):
```powershell
python try_it.py
```

---

## How It Works

1. **Cleaning (`prepare_data.py`):** merges the Excel sheets and replaces incomplete values with column-appropriate general defaults, without dropping any product
2. **Embedding (`build_embeddings.py`):** converts each product's description (type, season, scent family, notes, sweetness) into a vector and stores it in ChromaDB
3. **Search (`search.py`):** converts the customer's question into a vector and compares it against product vectors to find the closest matches. Also detects the season mentioned in the question (in any language) and filters results accordingly when relevant
4. **Generation (`generate_advice.py`):** sends the matched product to the Gemini API with strict instructions not to invent any information not present in the data
5. **API (`main.py`):** ties everything together in a single `/ask` endpoint, returning one recommended product plus advice, with backup alternatives and support for excluding previously shown products

Full request/response details are in [`API_Documentation.md`](./API_Documentation.md).

---

## Next Step: Deployment

The server currently runs locally only (`127.0.0.1`) and is reachable only on the development machine. To make it available to the live website, it needs to be deployed to a hosting service (e.g. Render or Railway) — a step not yet completed.
