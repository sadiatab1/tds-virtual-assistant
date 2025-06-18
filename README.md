# 🤖 TDS Virtual Assistant

A FastAPI-based virtual assistant that leverages local knowledge from PDFs, web scraping, and the OpenAI API to answer questions based on the **Tools in Data Science** course.

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers (Only Once)

```bash
playwright install
```

### 3. Run the FastAPI Server

```bash
uvicorn app:app --reload
```


---

## 🧠 Knowledge Base

The app uses a local SQLite database `knowledge_base.db` for storing vector embeddings of the course material.  
If it's not already present, you can create it using the provided scripts.

---

## 🛠 Tech Stack

- FastAPI 🚀
- SQLite (for knowledge base)
- OpenAI API (for GPT-based Q&A)
- Playwright (for scraping course content)
- HTML2Text + BeautifulSoup4
- Sentence Transformers for embeddings




---

## 📄 License

MIT License. Feel free to fork, modify, and build something awesome.
