import os
import time
from googletrans import Translator
from bs4 import BeautifulSoup

def translate_html_files():
    # Initialize the translator
    translator = Translator()
    
    # Get the catalog directory path
    catalog_dir = 'catalog'
    
    # Iterate through all HTML files in the catalog directory
    for filename in os.listdir(catalog_dir):
        translated_filename = f"{filename}.txt"
        # Check if translated file already exists
        translated_file_path = os.path.join(catalog_dir, translated_filename)
        if os.path.exists(translated_file_path):
            print(f"Skipping {filename} - translation already exists")
            continue

        # if filename.startswith('AIM') and filename.endswith('.html'):
        if filename.endswith('.html'):
            file_path = os.path.join(catalog_dir, filename)
            
            # Read the HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Parse HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all text elements
            text_elements = soup.find_all("div", {"class": "description"})
            
            # Translate each text element
            for element in text_elements:
                if element.parent.name not in ['script', 'style']:  # Skip script and style tags
                    # Get the text content
                    text = str(element.text)
                    if text:
                        try:
                            print("1")
                            # Translate the text to Korean
                            translated = translator.translate(text, dest='ko')
                            print("2")
                            print("translated : ", translated)
                            # Replace the original text with translated text
                            translated_text = translated.text
                            print("translated_text : ", translated_text)
                            # Wait for 3 seconds before next translation
                        except Exception as e:
                            print(f"Error translating text in {filename}: {str(e)}")
            
            # Save the translated HTML
            with open(os.path.join(catalog_dir, translated_filename), 'w', encoding='utf-8') as file:
                file.write(translated_text)
            
            print(f"Translated {filename} to {translated_filename}")
            time.sleep(3)
        

if __name__ == "__main__":
    translate_html_files()

