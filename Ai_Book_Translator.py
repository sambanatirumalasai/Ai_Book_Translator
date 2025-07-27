import re
import json
import google.generativeai as genai
import time
import getpass
import sys
import os

# --- Book Object Model (Single Class) ---
class Book:
    """
    Represents the entire book, managing chapters and paragraphs internally
    using a list of dictionaries.
    Each item in 'content' list is a chapter dictionary:
    {'title': 'Chapter Name', 'paragraphs': [{'original': '...', 'translated': '...'}]}
    """

    def __init__(self, title="Translated Book"):
        self.title = title
        self.content = []  # List to hold chapter dictionaries

    def add_chapter(self, title):
        """Adds a new chapter dictionary to the book's content."""
        chapter_dict = {'title': title, 'paragraphs': []}
        self.content.append(chapter_dict)
        return chapter_dict  # Return reference to the new chapter for direct paragraph addition

    def add_paragraph_to_last_chapter(self, original_text, translated_text):
        """
        Adds a paragraph to the last added chapter.
        Requires a chapter to have been added first.
        """
        if not self.content:
            raise ValueError("Cannot add paragraph: No chapter has been added to the book yet.")

        last_chapter = self.content[-1]
        paragraph_dict = {'original': original_text, 'translated': translated_text}
        last_chapter['paragraphs'].append(paragraph_dict)

    def __repr__(self):
        return f"Book(title='{self.title}', chapters_count={len(self.content)})"


# --- Original API & Utility Functions ---

def setup_gemini(api_key, target_language, tone):
    """
    Configures the Gemini API with the given API key and returns the model.
    Sets up system instructions for consistent translation tone and style.
    Exits if the model cannot be set up.
    """
    try:
        genai.configure(api_key=api_key)
        # Define the system instruction for the model
        system_instruction_prompt = f"""You are an AI specialized in translating books.
        Translate all text into {target_language}.
        Maintain a {tone} tone throughout the translation.
        Use words that are simple to understand with modern and formal diction (avoid slang or gen-z terms).
        Ensure readers are engaged.
        Crucially, only produce the translated text, without any additional commentary, introductions, or conclusions."""

        model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=system_instruction_prompt
        )
        return model
    except Exception as e:
        sys.exit(f"MODEL CAN NOT BE SET UP. Please check your API key or network connection. Error: {e}")


def translate_block(model, text):
    """
    Translates a single block of text using the Gemini model.
    The language and tone are set via system instructions.
    Raises ValueError if translation fails.
    """
    prompt = f"Translate the following paragraph. Text: {text}"
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        raise ValueError("Unable to translate block.")

def translate_heading(model, text):
    """
    Translates a single heading/index using the Gemini model.
    The language and tone are set via system instructions.
    Raises ValueError if translation fails.
    """
    prompt = f"Translate the following chapter title or section heading. Title/Heading: {text}"
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        print(f"❌ Error during heading translation: {e}")
        raise ValueError("Unable to translate heading.")


def check_api_key(api_key):
    """
    Validates the Gemini API key by making a test call.
    Returns True if the key is invalid, False otherwise.
    """
    try:
        genai.configure(api_key=api_key)
        # Use a minimal system instruction for the check
        test_model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction="Respond concisely.")
        response = test_model.generate_content("Hello Gemini")
        print("✅ API Key is valid.")
        print("🔹 Test Response:", response.text.strip())
        return False  # Key is valid
    except Exception as e:
        print("❌ Invalid API Key or another error occurred during validation.")
        print(f"🔍 Error: {e}")
        return True  # Key is invalid


def convert_txt_to_dict(txtfile):
    """
    Reads a text file, parses it into a dictionary where keys are chapter/summary headings
    and values are lists of original paragraphs. This function remains as in your original code.
    Exits if the text file format is not as expected.
    """
    try:
        with open(txtfile, "r", encoding="utf-8") as file:
            content = file.read().strip()
        paragraphs = content.split("\n\n")
        blocks = []
        for para in paragraphs:
            clean = para.strip()
            if clean:
                blocks.append(clean)
        chapter = {}
        # Default for initial blocks before any chapter number
        number = "summary"
        chapter["summary"] = []
        for block in blocks:
            if len(block) < 3:
                continue
            # Regex to match chapter numbers like "{-Chapter Name-}"
            match = re.match(r"^\{-(.+)-\}$", block)
            if match:
                number = match.group(1)
            else:
                chapter.setdefault(number, []).append(block)

        return chapter

    except FileNotFoundError:
        sys.exit(f"Error: Input text file '{txtfile}' not found. Please ensure it exists in the correct directory.")
    except Exception as e:
        sys.exit(f"Error parsing text file. Please arrange text file as specified in README. Error: {e}")


def save_dict_to_json(data, filename="book.json"):
    """
    Saves a dictionary (like the one returned by convert_txt_to_dict) to a JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving data to JSON: {e}")

def save_book_to_json(book_obj, filename="structured_book.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({'title': book_obj.title, 'content': book_obj.content}, f, ensure_ascii=False, indent=2)
        print(f"✅ Full Book JSON saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving full book JSON: {e}")

def main():
    # --- Interactive Input for Configuration ---
    input_txt_filename = input("Enter the path to the input text file (e.g., 'book.txt'): ").strip()
    if not os.path.exists(input_txt_filename):
        sys.exit(f"Error: Input file '{input_txt_filename}' not found. Please check the path and try again.")
    output_dir = os.path.dirname(os.path.abspath(input_txt_filename))
    if not output_dir: # Handle case where input_txt_filename is just "book.txt" in current directory
        output_dir = "."

    # Ensure output directory exists (important even if derived, as it might be a new directory if input path was new)
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        sys.exit(f"Error creating output directory '{output_dir}': {e}")

    print(f"Output files will be saved to: {os.path.abspath(output_dir)}")


    # Dynamically generate output filenames based on input file and output directory
    base_filename_without_ext = os.path.splitext(os.path.basename(input_txt_filename))[0]

    translated_output_text_filename = os.path.join(output_dir, f"{base_filename_without_ext}_translated.txt")
    full_output_text_filename = os.path.join(output_dir, f"{base_filename_without_ext}_full.txt")
    parsed_json_filename = os.path.join(output_dir, f"{base_filename_without_ext}_parsed.json")
    structured_book_json_filename = os.path.join(output_dir, f"{base_filename_without_ext}_structured_book.json")


    # --- API Key Validation ---
    api_check = True
    while api_check:
        secret_key = getpass.getpass("Enter your Gemini API key (hidden): ")
        api_check = check_api_key(secret_key)

    # --- User Input for Translation ---
    language = input("Please enter the target language to translate into (e.g., 'English', 'Hindi', 'Telugu'): ").strip()
    tone = input("How do you prefer the choice of words (e.g., 'simple', 'formal', 'conversational'): ").strip()
    print(f" Translation settings: Language = '{language}', Tone = '{tone}'")

    # --- Parse Input Text File into Original Dictionary Format ---
    print(f"\nProcessing '{input_txt_filename}' into dictionary format...")
    dictionary_format = convert_txt_to_dict(input_txt_filename)
    indexes = list(dictionary_format.keys())  # These are your chapter/section titles
    print(f"Found sections: {indexes}")
    save_dict_to_json(dictionary_format, parsed_json_filename)  # Save the original dictionary

    # --- Set Up Gemini Model (now with system instructions) ---
    model = setup_gemini(secret_key, language, tone)

    # --- Initialize the Book Object (Single Class) ---
    book_title = os.path.splitext(os.path.basename(input_txt_filename))[0].replace("_", " ").title()
    book_object = Book(title=f"Translated {book_title}") # Initial title is just based on original filename

    # --- Perform Translation, Write Files, and Populate Book Object ---
    print("\nStarting translation process...")
    try:
        # Open output files once before the loop for efficiency
        with open(translated_output_text_filename, "w", encoding="utf-8") as translated_file, \
                open(full_output_text_filename, "w", encoding="utf-8") as full_file:

            for index in indexes:
                # --- Translate the index (chapter/section title) ---
                translated_heading = ""
                retries = 0
                max_retries = 5
                print(f"\n  Translating heading: '{index}'...")
                while retries < max_retries:
                    try:
                        translated_heading = translate_heading(model, index)
                        break
                    except ValueError:
                        print(f"    Failed to translate heading '{index}'. Retrying ({retries + 1}/{max_retries})...")
                        retries += 1
                        time.sleep(2)
                else:
                    print(f"❌ Giving up on heading '{index}' after {max_retries} attempts.")
                    translated_heading = f"[Translation Failed for: {index}]"

                # Use the translated heading for display and file writing
                print(f"--- Original: '{index}' --- Translated: '{translated_heading}' ---")

                # Write headings to files
                translated_file.write(f"\n\n{translated_heading.upper()}\n\n\n") # Often headings are uppercase
                full_file.write(f"\n\n{index.upper()}\n\n\n") # Original heading
                full_file.write(f"{translated_heading.upper()}\n\n\n") # Translated heading

                # Add a new chapter to the book object with the translated title
                # IMPORTANT: Storing the translated title in the Book object for JSON export
                book_object.add_chapter(translated_heading)

                num = 0
                for block in dictionary_format[index]:
                    print(f"  Translating paragraph {num + 1} of '{index}'...")

                    translation = ""
                    retries = 0
                    while retries < max_retries:
                        try:
                            translation = translate_block(model, block)
                            break  # Break out of retry loop if successful
                        except ValueError:
                            print(
                                f"    Failed to translate paragraph {num + 1} of '{index}'. Retrying ({retries + 1}/{max_retries})...")
                            retries += 1
                            time.sleep(2)  # Longer sleep before retrying API call
                    else:  # This block executes if the while loop completes without a 'break'
                        print(f"❌ Giving up on paragraph {num + 1} of '{index}' after {max_retries} attempts.")
                        translation = "[Translation Failed]"  # Placeholder for failed translations

                    # Add the original and translated text to the book object
                    book_object.add_paragraph_to_last_chapter(original_text=block, translated_text=translation)

                    # Write to files as per original request
                    translated_file.write(f":\n{translation}\n") # Use translated heading
                    full_file.write(f"(Original):\n\n{block}\n\n\n")
                    full_file.write(f"(Translated):\n\n{translation}\n\n\n") # Use translated heading

                    num += 1
                    time.sleep(1.5)  # Pause between successful API calls to respect rate limits

        print(
            f"\n✅ Translation complete! Output saved to '{translated_output_text_filename}' and '{full_output_text_filename}'.")

    except Exception as e:
        print(f"An unexpected error occurred during the translation process: {e}")
        print("Please check your input file, network connection, or API key.")
        return None  # Return None if an error occurs
    save_book_to_json(book_object, structured_book_json_filename)
    return book_object  # Return the fully populated Book object at the end


if __name__ == "__main__":
    main()