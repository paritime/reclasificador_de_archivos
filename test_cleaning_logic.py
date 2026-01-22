import os
import renamer
import shutil

TEST_DIR = "test_clean_folder"

def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    
    # Create test files
    files = [
        "1. Alpha.txt",
        "02 - Beta.docx",
        "3 Gamma.pdf",
        "NoNum.txt",
        "10.1. Delta.xls"
    ]
    for f in files:
        with open(os.path.join(TEST_DIR, f), 'w') as fh:
            fh.write("content")

def test_auto_pattern():
    print("Testing Auto Pattern...")
    prev = renamer.get_cleaning_preview(TEST_DIR, 'auto_pattern')
    for item in prev['mapping']:
        print(f"  {item['Original']} -> {item['Nuevo Nombre']}")
    
    # Assertions roughly
    mapping = {i['Original']: i['Nuevo Nombre'] for i in prev['mapping']}
    assert mapping["1. Alpha.txt"] == "Alpha.txt"
    assert mapping["02 - Beta.docx"] == "Beta.docx"
    assert mapping["3 Gamma.pdf"] == "Gamma.pdf"
    assert mapping["NoNum.txt"] == "NoNum.txt"
    # "10.1. Delta.xls" -> "Delta.xls" or "1. Delta.xls" depending on regex greediness
    # Regex was ^[\d\s\.\-_]+
    # So 10.1. contains all matching chars, should strip all.
    print("  10.1. check:", mapping["10.1. Delta.xls"])
    
def test_remove_n():
    print("\nTesting Remove N (n=3)...")
    prev = renamer.get_cleaning_preview(TEST_DIR, 'remove_n', {'n': 3})
    for item in prev['mapping']:
        print(f"  {item['Original']} -> {item['Nuevo Nombre']}")

if __name__ == "__main__":
    setup()
    test_auto_pattern()
    test_remove_n()
    print("\nTests Finished.")
