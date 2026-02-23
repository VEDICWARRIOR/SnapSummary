# SnapSummary 📄✨

A lightweight Flask-based REST API that summarizes long text using Hugging Face's **BART Large CNN** model. It preprocesses input text locally (cleaning, chunking) before sending it to the Hugging Face Inference API, making it suitable for summarizing articles, documents, and other long-form content.

---

## Features

- Cleans noisy text (removes citation markers, normalizes whitespace)
- Splits long text into manageable chunks using NLTK sentence tokenization
- Summarizes each chunk via the Hugging Face `facebook/bart-large-cnn` model
- Combines chunk summaries into a single coherent result
- CORS-enabled for easy frontend integration

---

## Project Structure

```
snap_summary/
├── snap_summary_code.py   # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md              # Project documentation
```

---

## Prerequisites

- Python 3.8+
- A [Hugging Face account](https://huggingface.co/) and API token

---

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/snap-summary.git
   cd snap-summary
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

5. **Set your Hugging Face API token**

   Replace the `HF_TOKEN` value in `snap_summary_code.py` with your own token, or set it as an environment variable:
   ```bash
   export HF_TOKEN="your_hf_token_here"
   ```
   > ⚠️ Never commit your API token to version control.

6. **Run the Flask app**
   ```bash
   python snap_summary_code.py
   ```

   The server will start at `http://localhost:5000`.

---

## API Usage

### `POST /summarize`

**Request**

```json
{
  "text": "Your long article or document text goes here..."
}
```

**Response**

```json
{
  "summary": "A concise summary of the provided text."
}
```

**Example with `curl`**

```bash
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Paste your long text here."}'
```

---

## Configuration

| Variable         | Description                              | Default                                      |
|------------------|------------------------------------------|----------------------------------------------|
| `API_URL`        | Hugging Face model inference endpoint    | `facebook/bart-large-cnn`                    |
| `HF_TOKEN`       | Your Hugging Face API bearer token       | Set in code or via environment variable      |
| `max_chunk_length` | Max character length per text chunk    | `800`                                        |

---

## License

This project is licensed under the [MIT License](LICENSE).
