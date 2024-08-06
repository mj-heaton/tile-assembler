import os
import requests
import argparse
import sys
import hashlib
import re


def download_jpegs(
    base_url: str,
    download_dir: str,
    extension: str = ".jpg",
    max_row_col_count: int = 60
) -> None:
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    hashes: set[str] = set()

    x = 0
    while True:
        y = 0
        while True:
            url = f"{base_url}{x}_{y}{extension}"
            print(f"Downloading {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error downloading {url}. Status code: {response.status_code}")

                if y == 0 and y == 0 and extension == ".jpg":
                    download_jpegs(base_url, download_dir, ".jpeg", max_row_col_count)

                break  # Exit the loop if the URL returns an error code

            file_extension = ".jpg" if extension == ".jpeg" else extension
            file_path = os.path.join(download_dir, f"{x}_{y}{file_extension}")
            with open(file_path, 'wb') as file:
                file.write(response.content)

            # Get the SHA256 hash of the downloaded file
            with open(file_path, 'rb') as file:
                file_hash = hashlib.sha256(file.read()).hexdigest()
                print(f"SHA256 hash of {file_path}: {file_hash}")
                # Check if the hash has already been seen
                if file_hash in hashes:
                    print(f"Warning: Duplicate file detected")
                    # Remove the duplicate file
                    os.remove(file_path)
                    break

                hashes.add(file_hash)

            print(f"Downloaded {file_path}")
            y += 1

            if y >= max_row_col_count:
                print(f"Warning, max_row_col_count ({max_row_col_count}) reached for x={x} y={y}. This is likely an error. Terminating.")
                sys.exit(1)
        if y == 0:
            break  # Exit the loop if no files were downloaded for the current value of x
        x += 1
        if x >= max_row_col_count:
            print(f"Warning, max_row_col_count ({max_row_col_count}) reached for x={x} y={y}. This is likely an error. Terminating.")
            sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description='Download JPEG images from a URL pattern.')
    parser.add_argument('base_url', type=str, help='The base URL pattern (e.g., "https://example.com/images/image_").')
    parser.add_argument('download_dir', type=str, help='The directory to save the downloaded images.')
    args = parser.parse_args()

    # Define the regex pattern to match the final {integer}_{integer}.jpg or .jpeg part
    pattern = r'\d+_\d+\.(jpg|jpeg)$'
    # Use re.sub to replace the matched pattern with an empty string
    base_url = re.sub(pattern, '', args.base_url)

    # If there are no spaces in the download_dir, replace - with spaces and capitalize the first letter of each word
    if ' ' not in args.download_dir:
        args.download_dir = ' '.join(args.download_dir.split('-')).title()

    download_jpegs(base_url, args.download_dir)

if __name__ == '__main__':
    main()
