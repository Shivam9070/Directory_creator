import os
import pyperclip
import re

def clean_line(line):
    # Remove tree structure characters and icons
    line = re.sub(r'[│├└─📁📄]', '', line)
    return line.strip()

def create_structure_from_text(structure_text, base_dir='.'):
    lines = structure_text.strip().split('\n')
    stack = [base_dir]

    for line in lines:
        cleaned = clean_line(line)
        if not cleaned:
            continue

        # Calculate depth based on indentation (tabs or spaces)
        depth = len(line) - len(line.lstrip(' \t│├└─📁📄'))
        name = cleaned.rstrip('/')

        # Adjust stack depth
        while len(stack) > (depth // 4) + 1:
            stack.pop()

        path = os.path.join(stack[-1], name)

        if '.' in os.path.basename(name):  # treat as file
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                open(path, 'w').close()
                print(f"📄 Created file: {path}")
            else:
                print(f"⚠️ Skipped existing file: {path}")
        else:  # treat as folder
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"📂 Created folder: {path}")
            else:
                print(f"📂 Skipped existing folder: {path}")
            stack.append(path)

if __name__ == "__main__":
    print("📋 Reading structure from clipboard...")
    structure = pyperclip.paste()
    if not structure.strip():
        print("❌ Clipboard is empty. Please copy your folder structure first.")
    else:
        base_directory = input("Enter base directory (default: current folder): ").strip() or "."
        create_structure_from_text(structure, base_directory)
        print("✅ Structure creation complete!")
