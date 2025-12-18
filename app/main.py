from renamer import rename_files
import os

def main():
    base_dir = os.path.dirname(__file__)
    folder = os.path.join(base_dir, "..", "examples", "test_files")
    folder = os.path.abspath(folder)

    rename_files(folder, prefix="doc", dry_run=True)
    
if __name__ == "__main__":
    main()
