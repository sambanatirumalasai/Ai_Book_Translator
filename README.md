# AI_Book_Translator

A Python tool for translating structured books and documents using [Google Gemini AI](https://aistudio.google.com/). Maintains original formatting and style for high-quality results.

---

## ✨ Features

- **End-to-End Translation:** Translates both section headings and paragraphs.
- **AI-Powered:** Uses Google Gemini for accurate, natural translations.
- **Customizable Output:**
  - Select your target language (e.g., Hindi, French, Japanese)
  - Choose tone (e.g., simple, formal, conversational)
- **Resilient & Efficient:** Handles network errors and API rate limits gracefully.
- **Secure:** Prompts for your Gemini API key at runtime (never hardcoded).
- **Organized Output Files:**
  - Pure translated text
  - Side-by-side (original + translation)
  - Structured JSON for programmatic use
- **Automated File Management:** All outputs saved in your input file’s directory.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An active internet connection
- A [Google Gemini API key](https://aistudio.google.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sambanatirumalasai/Ai_Book_Translator.git
   cd Ai_Book_Translator
   ```
2. **Install required libraries:**
   ```bash
   pip install -r requirements.txt
   ```
3. *(Optional)* Install pytest for testing:
   ```bash
   pip install pytest
   ```

---

## 📖 Usage

1. **Prepare your input file (e.g., `book.txt`):**
   - Section headings: `{ - ... - }`
   - Paragraphs: Separated by two newlines (`\n\n`)
   - Example:
     ```
     {-Introduction-}

     This is the first paragraph.

     This is the second paragraph.

     {-Chapter 1: The Journey Begins-}

     The hero embarks on his journey.
     ```

2. **Run the translator:**
   ```bash
   python project.py
   ```
   - Follow prompts for file path, API key, target language, and preferred style.

---

## 📦 Output Files

- `[input]_parsed.json` — Structured original content
- `[input]_translated.txt` — Translated text only
- `[input]_full.txt` — Original and translated content side-by-side
- `[input]_structured_book.json` — Structured translated book for further use

---

## ✅ Testing

Run unit tests (if available):
```bash
pytest
```

---

## 🛠 Troubleshooting

- **File not found:** Check your filename and path.
- **API key error:** Verify your Gemini API key and network connection.
- **Formatting error:** Make sure your input matches the specified structure.
- **Translation failed:** The script retries automatically; persistent failures may need more time between calls or checking Gemini’s status.

---

## 📬 Contributing

Pull requests and suggestions are welcome! Open an issue or submit a PR.

---

## 📄 License

This project is released under the [Unlicense](LICENSE).

---

**Made with ❤️ by [sambanatirumalasai](https://github.com/sambanatirumalasai)**
