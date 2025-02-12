"""
Read.me
What is this? 
When you have many Xbox codes that you want to redeem, using the Xbox PC application is a reliable way to do so.
pyautogui is simply pushing the individual buttons needed in the Xbox app at the right coordinates, copies the
codes out of a word document in a *.docx format. I have a different program that I run to strip out the correct
codes from a larger document and place the codes into the document.
Learn more about pyautogui here https://www.youtube.com/watch?v=lfk_T6VKhTE
ChatGPT o3-mini was used in the creation of this code
You MUST modify the coordinates_first_run and clone some of the coordinates for coordinates_subsequent to make it 
work on your PC.
"""
import time
import pyautogui
import pyperclip
from docx import Document
import os
import re

# Full coordinate sequence for the *first* code redemption
coordinates_first_run = [
    (116, 52),    # "Xbox Face"
    (125, 300),   # "Xbox Settings"
    (1102, 1262), # "Xbox Redeem"
    (751, 780),   # "Xbox Code" (where we paste the code)
    (782, 772),   # "Xbox NEXT"
    (759, 1435),  # "Confirm"
    (759, 1435),  # "Close"
    (1255, 1425)  # "Cancel"
]

# Partial coordinate sequence for *subsequent* redemptions
coordinates_subsequent = [
    (1102, 1262), # "Xbox Redeem"
    (751, 780),   # "Xbox Code"
    (782, 772),   # "Xbox NEXT"
    (759, 1435),  # "Confirm"
    (759, 1435),  # "Close"
    (1255, 1425)  # "Cancel"
]

def read_all_codes_from_docx(docx_path):
    """
    Searches the DOCX file for codes matching the pattern 'XXXXX-XXXXX-XXXXX-XXXXX-XXXXX'
    using a regex. This function scans both paragraphs and tables.
    Returns a list of code strings.
    """
    document = Document(docx_path)
    codes = []
    # Define a regex pattern: 5 alphanumeric characters, repeated 5 times with dashes in between.
    pattern = re.compile(r'\b[A-Za-z0-9]{5}(?:-[A-Za-z0-9]{5}){4}\b')
    
    # Search in paragraphs
    for paragraph in document.paragraphs:
        found = pattern.findall(paragraph.text)
        if found:
            codes.extend(found)
    
    # Search in tables (if any)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                found = pattern.findall(cell.text)
                if found:
                    codes.extend(found)
                    
    # Remove duplicates while preserving order
    seen = set()
    unique_codes = []
    for code in codes:
        if code not in seen:
            unique_codes.append(code)
            seen.add(code)
    
    return unique_codes

def redeem_code(code, coordinates):
    """
    Goes through the given coordinate list, clicking each coordinate.
    Immediately after clicking (751, 780), it pastes the given code.
    """
    for (x, y) in coordinates:
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()

        # Right after clicking (751, 780), paste the code
        if (x, y) == (751, 780):
            pyperclip.copy(code)
            pyautogui.hotkey("ctrl", "v")

        # Wait 7 seconds before moving to the next coordinate
        time.sleep(7)

def get_docx_path():
    """
    Prompt the user to input the DOCX file path.
    Continues to prompt until a valid file path is provided.
    Provides an example to guide the user.
    """
    example_path = r"D:\OneDrive\xbox\Codes\Automation\Code.docx"
    prompt_message = (
        f"Please enter the full path to your DOCX file (e.g., {example_path}): "
    )
    while True:
        docx_path = input(prompt_message).strip()
        if os.path.isfile(docx_path) and docx_path.lower().endswith('.docx'):
            return docx_path
        else:
            print("Invalid file path or file is not a DOCX. Please try again.\n")

def main():
    # Get a valid DOCX file path from the user
    docx_path = get_docx_path()
    
    codes = read_all_codes_from_docx(docx_path)
    if not codes:
        print("No valid codes found in the DOCX file.")
        return
    
    print(f"Found {len(codes)} code(s):")
    for c in codes:
        print(" -", c)
    
    # New message added as per your request
    print(f"\nThe total codes found in the file are: {len(codes)}")
    
    print("\nPlease make sure the Xbox app is open and visible. You have 5 seconds...")
    time.sleep(5)
    
    # Redeem the first code with the full coordinate sequence
    print(f"\nRedeeming first code: {codes[0]}")
    redeem_code(codes[0], coordinates_first_run)
    
    # Redeem subsequent codes (if any) using the partial sequence
    for code in codes[1:]:
        print(f"\nRedeeming next code: {code}")
        redeem_code(code, coordinates_subsequent)
        # Optional: wait a few extra seconds between codes
        time.sleep(5)

    print("\nAll codes processed.")

if __name__ == "__main__":
    main()
