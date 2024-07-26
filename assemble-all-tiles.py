import os


def main() -> None:
    """
    Main function to parse command line arguments and assemble tiles.
    """
    # List all folders in the current directory
    folders = [name for name in os.listdir() if os.path.isdir(name)]
    ignore_folders = ["__pycache__", ".git", ".idea", "venv", ".", ".."]
    print(folders)
    for folder in folders:
        if folder in ignore_folders:
            continue

        os.system(f'python assemble-tiles.py "{folder}"')


if __name__ == "__main__":
    main()
