import os
import json
import sys
import shutil
import subprocess
import datetime

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
    Iterates through .cph/ config files and updates 'srcPath' to match the current machine's absolute path.
    """
    print("--- Fixing CPH Paths ---")
    if not os.path.exists(CPH_DIR):
        print(f"No .cph directory found at {CPH_DIR}. Skipping.")
        return

    count = 0
    for filename in os.listdir(CPH_DIR):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(CPH_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if srcPath exists
            if 'srcPath' in data:
                old_path = data['srcPath']
                # Extract the filename from the old path
                src_filename = os.path.basename(old_path)
                
                # Construct the new correct absolute path on this machine
                # We assume the source file is directly in 'Current/'
                new_path = os.path.join(CURRENT_DIR, src_filename)
                
                # Normalize paths for comparison (handle slashes)
                if os.path.normpath(old_path) != os.path.normpath(new_path):
                    print(f"Updating {src_filename}:")
                    print(f"  Old: {old_path}")
                    print(f"  New: {new_path}")
                    data['srcPath'] = new_path
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    count += 1
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    print(f"Fixed paths in {count} files.")

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
    Removes binaries and .cph folder from Current directory.
    """
    print("--- Cleaning Current Directory ---")
    
    # 1. Remove binaries
    files_cleaned = 0
    for filename in os.listdir(CURRENT_DIR):
        file_path = os.path.join(CURRENT_DIR, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext in CLEAN_EXTENSIONS:
                os.remove(file_path)
                print(f"Deleted binary: {filename}")
                files_cleaned += 1
    
    # 2. Remove .cph folder
    if os.path.exists(CPH_DIR):
        shutil.rmtree(CPH_DIR)
        print("Removed .cph directory")
    
    print(f"Cleaned {files_cleaned} files.")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manager.py fix       - Fix CPH paths for current OS")
        print("  python manager.py sync      - Git sync (add, commit, pull, fix, push)")
        print("  python manager.py archive <ID> - Archive current contest and sync")
        print("  python manager.py clean     - Clean binaries and .cph from Current")
        return

    command = sys.argv[1].lower()

    if command == 'fix':
        fix_cph_paths()
    elif command == 'sync':
        git_sync()
    elif command == 'clean':
        clean_current()
    elif command == 'archive':
        if len(sys.argv) < 3:
            print("Error: Please provide a contest ID (e.g., python manager.py archive 1950)")
            return
        archive_contest(sys.argv[2])
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
