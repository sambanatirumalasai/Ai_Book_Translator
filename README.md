📚 AI_Book_Translator: Translate Books Using Gemini AI
AI_Book_Translator is a Python-based CLI tool that allows you to translate entire books into your chosen language and tone using Google's Gemini 1.5 Flash model. Built for my CS50P Final Project, this marks my first complete and structured GitHub project! 🎉

✨ Features
🔄 Translates full books, not just single lines or paragraphs

🧠 Uses Gemini 1.5 Flash with system instructions for better tone and context

🌍 Supports any target language (Hindi, Tamil, Spanish, etc.)

💬 Customize the tone: simple, formal, conversational, and more

📁 Outputs clean translated text, side-by-side full text, and structured JSON

🔐 Securely uses your own Gemini API key

📊 Built with clean, testable Python code structure

🗂️ Project Structure
bash
Copy
Edit
AI_Book_Translator/
├── project.py                 # Main CLI app
├── test_project.py            # Tests for functions
├── requirements.txt           # Required libraries
├── book.txt                   # Your input file (example)
├── *_translated.txt           # Translated output
├── *_full.txt                 # Original + translated output
├── *_parsed.json              # Parsed raw book content
├── *_structured_book.json     # Fully structured book JSON
└── README.md                  # This file
🔧 How to Set It Up
Clone the project

bash
Copy
Edit
git clone https://github.com/<your-username>/AI_Book_Translator.git
cd AI_Book_Translator
(Optional) Set up a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate        # On Mac/Linux
venv\Scripts\activate           # On Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Get your Gemini API key

Go to Google AI Studio

Copy your API key

Run the translator

bash
Copy
Edit
python project.py
You’ll be prompted for:

Your Gemini API key (secure input)

Target language

Tone (e.g., simple, formal)

📘 Input Format
Your book.txt file should follow this format:

txt
Copy
Edit
{-Introduction-}
This is the first paragraph.

This is the second paragraph.

{-Chapter 1-}
The story begins here.

Another line in chapter 1.
Paragraphs are separated by blank lines

Headings are wrapped like {–Chapter Name–}

📤 Output Files
File Name	Description
*_translated.txt	Clean, translated text
*_full.txt	Original + translated text side-by-side
*_parsed.json	Raw parsed book as dictionary
*_structured_book.json	Fully structured JSON with chapters

🧪 Running Tests
Run tests using pytest:

bash
Copy
Edit
pytest
Ensure your test_project.py contains unit tests for at least 3 functions in project.py.

📦 Requirements
All dependencies are listed in requirements.txt. Install them with:

bash
Copy
Edit
pip install -r requirements.txt
🪪 License
This project is released under the MIT License.

🙏 Acknowledgments
CS50's Introduction to Programming with Python

Google AI Studio

OpenAI and Gemini API documentation

Let me know if you’d like to include badges (e.g., build passing, python version) or a banner logo. I can help you generate one!
