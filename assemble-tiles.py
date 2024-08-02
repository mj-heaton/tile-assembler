import os
import re
import sys
import argparse
from PIL import Image


def assemble_tiles(folder_path: str) -> Image.Image:
    """
    Assembles JPEG tiles from the specified folder into a single image.

    Args:
        folder_path (str): The path to the folder containing the JPEG tiles.

    Returns:
        Image.Image: The assembled image.
    """
    # Regex to extract x and y coordinates from the filename
    tile_regex = re.compile(r'(\d+)_(\d+)\.jpg')

    # Dictionary to hold images with their coordinates as keys
    tiles: dict[tuple[int, int], Image.Image] = {}

    # Read through the folder and collect tile images
    for filename in os.listdir(folder_path):
        match = tile_regex.match(filename)
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            tiles[(x, y)] = Image.open(os.path.join(folder_path, filename))

    # Find the max coordinates to determine the size of the final image
    max_x = max(coord[0] for coord in tiles.keys())
    max_y = max(coord[1] for coord in tiles.keys())

    # Assuming all tiles are the same size, get the size of the first tile
    tile_width, tile_height = next(iter(tiles.values())).size

    # Create a new blank image with the appropriate size
    final_image = Image.new("RGB", ((max_x + 1) * tile_width, (max_y + 1) * tile_height))

    # Paste each tile into the final image
    for (x, y), tile in tiles.items():
        shift_x = 0
        shift_y = 0
        if x > 0:
            shift_x = -1
        if y > 0:
            shift_y = -1
        final_image.paste(tile, (x * tile_width + shift_x, y * tile_height + shift_y))

    # There is likely a solid black border at the bottom and right edges of the image - detect its location
    # and crop it
    border_color = (0, 0, 0)
    right_edge = final_image.width
    bottom_edge = final_image.height
    for x in range(final_image.width - 1, 0, -1):
        if final_image.getpixel((x, 0)) != border_color:
            right_edge = x
            break
    for y in range(final_image.height - 1, 0, -1):
        if final_image.getpixel((0, y)) != border_color:
            bottom_edge = y
            break

    amount_to_crop_vertically = final_image.height - bottom_edge
    amount_to_crop_horizontally = final_image.width - right_edge

    print(f"Amount to crop vertically: {amount_to_crop_vertically}")
    print(f"Amount to crop horizontally: {amount_to_crop_horizontally}")

    final_image = final_image.crop((0, 0, right_edge, bottom_edge))
    return final_image

def main() -> None:
    """
    Main function to parse command line arguments and assemble tiles.
    """
    parser = argparse.ArgumentParser(description="Assemble JPEG tiles from a folder into a single image.")
    parser.add_argument("folder_path", type=str, help="The path to the folder containing the JPEG tiles.")
    args = parser.parse_args()

    folder_path = args.folder_path
    output_image = f"{folder_path}.jpg"
    if os.path.exists(output_image):
        print(f"Image with name {output_image} already exists. Please delete it before running the script.")
        sys.exit(0)

    if not os.path.exists(folder_path):
        print(f"Folder with path {folder_path} does not exist.")
        sys.exit(1)

    assembled_image = assemble_tiles(folder_path)
    assembled_image.save(f"{folder_path}.jpg")
    print(f"Image saved as {folder_path}.jpg")

if __name__ == "__main__":
    main()

