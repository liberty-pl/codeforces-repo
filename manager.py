import os
import json
import sys
import shutil
import subprocess
import datetime

import hashlib

# --- Configuration ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR = os.path.join(ROOT_DIR, 'Current')
ARCHIVE_DIR = os.path.join(ROOT_DIR, 'Archive')
CPH_DIR = os.path.join(CURRENT_DIR, '.cph')

# File extensions to archive (source code)
SOURCE_EXTENSIONS = {'.cpp', '.cc', '.c', '.py', '.java', '.rs', '.go', '.js', '.ts'}
# File extensions/names to clean (binaries, etc.)
CLEAN_EXTENSIONS = {'.exe', '.out', '.o', '.app', '.dSYM', '.class'}

def run_command(cmd, cwd=None):
    """Run a shell command."""
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd or ROOT_DIR)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        # We don't exit here because sometimes git pull might fail if no upstream, etc.
        # But for critical errors, it might be better to handle them.

def fix_cph_paths():
    """
    Function A: Fix CPH Paths
    Iterates through .cph/ config files and:
    1. Updates 'srcPath' to match the current machine's absolute path.
    2. Renames the .prob file to match the hash of the new path (required by CPH).
    """
    print("--- Fixing CPH Paths ---")
    if not os.path.exists(CPH_DIR):
        print(f"No .cph directory found at {CPH_DIR}. Skipping.")
        return

    count = 0
    # List files first to avoid issues if we rename them while iterating
    files = [f for f in os.listdir(CPH_DIR) if f.endswith('.json') or f.endswith('.prob')]
    
    for filename in files:
        file_path = os.path.join(CPH_DIR, filename)
        # Skip if file was already renamed/moved in this loop
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if srcPath exists
            if 'srcPath' in data:
                old_path = data['srcPath']
                src_filename = os.path.basename(old_path)
                
                # Construct the new correct absolute path on this machine
                new_path = os.path.join(CURRENT_DIR, src_filename)
                
                # 1. Update content if path changed
                path_changed = os.path.normpath(old_path) != os.path.normpath(new_path)
                if path_changed:
                    print(f"Updating content for {src_filename}")
                    data['srcPath'] = new_path
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                
                # 2. Check and Fix Filename (Hash)
                # CPH uses md5(absolute_path) in the filename. 
                # If we moved the file, we MUST rename the config file too.
                new_path_hash = hashlib.md5(new_path.encode('utf-8')).hexdigest()
                new_config_filename = f".{src_filename}_{new_path_hash}.prob"
                new_config_path = os.path.join(CPH_DIR, new_config_filename)

                if filename != new_config_filename:
                    print(f"Renaming config file:")
                    print(f"  From: {filename}")
                    print(f"  To:   {new_config_filename}")
                    shutil.move(file_path, new_config_path)
                    count += 1
                elif path_changed:
                    count += 1

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    print(f"Fixed paths and filenames for {count} files.")

def git_sync():
    """
    Function B: Git Sync
    add -> commit -> pull -> fix_paths -> push
    """
    print("--- Starting Git Sync ---")
    
    # 1. Add and Commit
    run_command("git add .")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Only commit if there are changes
    try:
        subprocess.run("git diff-index --quiet HEAD --", shell=True, cwd=ROOT_DIR, check=True)
        print("No changes to commit.")
    except subprocess.CalledProcessError:
        run_command(f'git commit -m "Sync: {timestamp}"')

    # 2. Pull
    print("Pulling from remote...")
    try:
        run_command("git pull")
    except Exception:
        print("Git pull failed (maybe merge conflict or no upstream). Continuing to fix paths...")

    # 3. Fix Paths (Crucial step after pulling)
    fix_cph_paths()

    # 4. Push
    print("Pushing to remote...")
    run_command("git push")
    print("Sync complete.")

def archive_contest(contest_id):
    """
    Function C: Archive
    Moves code from Current to Archive/<contest_id>, cleans up, and syncs.
    """
    print(f"--- Archiving Contest {contest_id} ---")
    
    target_dir = os.path.join(ARCHIVE_DIR, contest_id)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created archive directory: {target_dir}")

    # 1. Move Source Files
    files_moved = 0
    for filename in os.listdir(CURRENT_DIR):
        file_path = os.path.join(CURRENT_DIR, filename)
        
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext in SOURCE_EXTENSIONS:
                shutil.move(file_path, os.path.join(target_dir, filename))
                print(f"Moved: {filename}")
                files_moved += 1
            elif ext in CLEAN_EXTENSIONS:
                os.remove(file_path)
                print(f"Deleted binary: {filename}")
    
    # 2. Clean .cph folder
    if os.path.exists(CPH_DIR):
        print("Cleaning .cph directory...")
        shutil.rmtree(CPH_DIR)
        # Recreate empty .cph dir if needed, or just leave it deleted until next run
        # Usually CPH plugin recreates it.
    
    # 3. Clean any other binaries in Current (if missed by loop above)
    # (The loop above covers files in Current root)

    print(f"Archived {files_moved} source files to {target_dir}")

    # 4. Sync
    git_sync()

def clean_current():
    """
    Function D: Clean
    Removes ALL source files, binaries and .cph folder from Current directory.
    """
    print("--- Cleaning Current Directory ---")
    
    # 1. Remove files
    files_cleaned = 0
    for filename in os.listdir(CURRENT_DIR):
        file_path = os.path.join(CURRENT_DIR, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            # Remove both binaries AND source files
            if ext in CLEAN_EXTENSIONS or ext in SOURCE_EXTENSIONS:
                os.remove(file_path)
                print(f"Deleted: {filename}")
                files_cleaned += 1
    
    # 2. Remove .cph folder
    if os.path.exists(CPH_DIR):
        shutil.rmtree(CPH_DIR)
        print("Removed .cph directory")
    
    print(f"Cleaned {files_cleaned} files.")

def move_files_to_current():
    """
    Function: Move Files
    Moves loose source files from Root to Current.
    Also moves .cph folder if it exists in Root.
    """
    print("--- Moving Source Files to Current ---")
    files_moved = 0
    for filename in os.listdir(ROOT_DIR):
        file_path = os.path.join(ROOT_DIR, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext in SOURCE_EXTENSIONS:
                # Don't move the manager script itself
                if filename == 'manager.py':
                    continue
                
                target_path = os.path.join(CURRENT_DIR, filename)
                # Move file
                shutil.move(file_path, target_path)
                print(f"Moved: {filename}")
                files_moved += 1
                
    print(f"Moved {files_moved} files to Current/.")

    # Move .cph folder from Root to Current if it exists
    root_cph = os.path.join(ROOT_DIR, '.cph')
    if os.path.exists(root_cph):
        if os.path.exists(CPH_DIR):
            print(f"Removing existing {CPH_DIR} to replace with root .cph")
            shutil.rmtree(CPH_DIR)
        
        shutil.move(root_cph, CPH_DIR)
        print(f"Moved .cph folder to {CPH_DIR}")
        
        # Fix paths immediately after moving
        fix_cph_paths()

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manager.py fix       - Fix CPH paths for current OS")
        print("  python manager.py sync      - Git sync (add, commit, pull, fix, push)")
        print("  python manager.py archive <ID> - Archive current contest and sync")
        print("  python manager.py clean     - Clean binaries and .cph from Current")
        print("  python manager.py move      - Move loose source files to Current")
        return

    command = sys.argv[1].lower()

    if command == 'fix':
        fix_cph_paths()
    elif command == 'sync':
        git_sync()
    elif command == 'clean':
        clean_current()
    elif command == 'move':
        move_files_to_current()
    elif command == 'archive':
        if len(sys.argv) < 3:
            print("Error: Please provide a contest ID (e.g., python manager.py archive 1950)")
            return
        archive_contest(sys.argv[2])
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
