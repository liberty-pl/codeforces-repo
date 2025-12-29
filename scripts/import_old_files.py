import os
import shutil
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT_DIR, 'cf')
ARCHIVE_DIR = os.path.join(ROOT_DIR, 'Archive')
MISC_DIR = os.path.join(ARCHIVE_DIR, 'Misc')

if not os.path.exists(MISC_DIR):
    os.makedirs(MISC_DIR)

# Extensions to keep
SOURCE_EXTS = {'.cpp', '.cc', '.c', '.py', '.java', '.rs', '.go', '.js', '.ts'}

def is_contest_id(name):
    return name.isdigit()

def get_contest_id_from_filename(filename):
    # Match patterns like 1234A.cpp, 1234B2.cpp
    match = re.match(r'^(\d+)[A-Z]', filename)
    if match:
        return match.group(1)
    return None

def main():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory {SOURCE_DIR} does not exist.")
        return

    print(f"Importing files from {SOURCE_DIR} to {ARCHIVE_DIR}...")

    for item in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, item)
        
        # Skip system files
        if item in ['.DS_Store', '.git', '.vscode', '.cph']:
            continue

        if os.path.isdir(src_path):
            # It's a folder
            if is_contest_id(item):
                dest_path = os.path.join(ARCHIVE_DIR, item)
                if os.path.exists(dest_path):
                    print(f"Warning: {item} already exists in Archive. Merging/Overwriting...")
                    # If exists, we need to move contents individually to avoid errors
                    for sub_item in os.listdir(src_path):
                        shutil.move(os.path.join(src_path, sub_item), os.path.join(dest_path, sub_item))
                    shutil.rmtree(src_path) # Remove empty dir
                else:
                    shutil.move(src_path, dest_path)
                print(f"Archived Folder: {item}")
            else:
                print(f"Skipping non-contest folder: {item}")
        
        elif os.path.isfile(src_path):
            # It's a file
            _, ext = os.path.splitext(item)
            if ext in SOURCE_EXTS:
                contest_id = get_contest_id_from_filename(item)
                if contest_id:
                    # Move to Archive/ID/
                    target_dir = os.path.join(ARCHIVE_DIR, contest_id)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    shutil.move(src_path, os.path.join(target_dir, item))
                    print(f"Archived File: {item} -> {contest_id}/")
                else:
                    # Move to Misc
                    shutil.move(src_path, os.path.join(MISC_DIR, item))
                    print(f"Moved to Misc: {item}")
            else:
                # Ignore binaries/others
                pass

    # Clean up
    # shutil.rmtree(SOURCE_DIR) # Optional: keep empty dir or delete? User might want to keep it.
    print("Import complete.")

if __name__ == "__main__":
    main()
