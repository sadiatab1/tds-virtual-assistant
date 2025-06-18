# 🧠 TDS Virtual Assistant

A virtual teaching assistant for the *Tools for Data Science (TDS)* course that can answer students' questions based on course content and Discourse forum discussions.

## 🚀 Features

* 📁 Upload a `.pdf` or `.md` file containing course or forum content
* ❓ Ask any question related to the uploaded content
* 🤖 Returns the best-matching answer using embedding-based semantic search
* 🔗 Includes relevant links to forum discussions (if available)

## 🛠️ Tech Stack

* **Backend**: Flask
* **NLP**: OpenAI Embeddings
* **Data**: Markdown & PDF parsing, Discourse forum scraping
* **Deployment-ready**: Can be hosted anywhere with an exposed `/api` endpoint

## 📦 Folder Structure

```
.
├── app.py                   # Flask API endpoint
├── embeddings.py            # Handles embedding and matching logic
├── scrape_course_content.py # Scrapes course content
├── preprocess.py            # Converts scraped HTML to markdown
├── embeddings.json          # Pre-computed text embeddings
├── course_content.json      # Raw content from course page
├── requirements.txt         # Python dependencies
├── .gitignore
├── test_api.py              # Sample test script for the API
├── vercel.json              # Deployment config (Vercel)
└── render.yaml              # Deployment config (Render)
```

## 📱 API Endpoint

**POST** `/api`

### Request Body (JSON)

```json
{
  "question": "Should I use gpt-4o-mini or gpt-3.5 turbo?",
  "filename": "sample_thread.md",
  "file": "<base64-encoded file content>"
}
```

### Response (JSON)

```json
{
  "answer": "You must use gpt-3.5-turbo-0125...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/.../4",
      "text": "Use the model that’s mentioned in the question."
    }
  ],
  "score": 0.63
}
```

## 📝 How to Use

1. Clone the repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the API server:

   ```bash
   python app.py
   ```

3. Use `test_api.py` or `curl` to test the endpoint.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
