from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import os
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# -------------------------------------------
# 🔹 Configuration for Hugging Face BART API
# -------------------------------------------
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = os.environ.get("HF_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("HF_TOKEN is not set. Please add it to your .env file.")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# -------------------------------------------
# 🔹 Function to call Hugging Face API
# -------------------------------------------
def summarize_via_huggingface(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print("Error:", response.text)
        return "Error during summarization"

    data = response.json()
    if isinstance(data, list) and len(data) > 0 and "summary_text" in data[0]:
        return data[0]["summary_text"]
    else:
        return "No summary generated."

# -------------------------------------------
# 🔹 Local preprocessing: clean & chunk text
# -------------------------------------------
def clean_text(text):
    """Remove extra spaces, references, and unwanted characters."""
    text = re.sub(r"\[\d+\]", "", text)  # remove [1], [2], etc.
    text = re.sub(r"\s+", " ", text)     # normalize whitespace
    return text.strip()

def chunk_text(text, max_chunk_length=800):
    """Split long text into smaller chunks for summarization."""
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# -------------------------------------------
# 🔹 Flask API endpoint
# -------------------------------------------
@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"summary": "No text provided."})

    # Local preprocessing
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    # Remote summarization
    summaries = []
    for chunk in chunks:
        summary = summarize_via_huggingface(chunk)
        summaries.append(summary)

    # Combine chunk summaries
    final_summary = " ".join(summaries).strip()
    return jsonify({"summary": final_summary})

# -------------------------------------------
# 🔹 Run Flask App
# -------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
