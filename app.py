from flask import Flask, request, jsonify
import os
import base64
from PyPDF2 import PdfReader
from embeddings import embed_text, get_top_match, load_embeddings
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Cache embeddings globally (but lazy-loaded)
_embeddings_data = None
def get_embeddings():
    global _embeddings_data
    if _embeddings_data is None:
        _embeddings_data = load_embeddings()
    return _embeddings_data

@app.route("/api", methods=["POST"])
def handle_api():
    data = request.get_json()

    question = data.get("question")
    filename = data.get("filename")
    file_content_base64 = data.get("file")

    if not question or not filename or not file_content_base64:
        return jsonify({"error": "Missing required fields"}), 400

    # Reject unsupported file types
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return jsonify({"error": "Image inputs are not supported in this version"}), 400

    try:
        # Save uploaded file
        file_bytes = base64.b64decode(file_content_base64)
        save_path = os.path.join("uploaded", filename)
        os.makedirs("uploaded", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(file_bytes)

        # Extract text from file
        if filename.endswith(".md"):
            with open(save_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif filename.endswith(".pdf"):
            reader = PdfReader(save_path)
            content = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Embed & search
        query_embedding = embed_text(question)
        top_text, score, links = get_top_match(query_embedding, get_embeddings())

        return jsonify({
            "answer": top_text,
            "score": score,
            "links": links
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
