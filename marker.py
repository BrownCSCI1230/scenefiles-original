# Script for marking expected outputs, recursively marks all files in
# <root_dir> and its subdirectories, when executed as
#       python marker.py <root_dir>

import os
import sys
from PIL import Image
from pathlib import Path
from collections import deque

def mark_folder(folder_path):
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    
    for image_file in folder_path.iterdir():
        if image_file.suffix.lower() in supported_extensions and image_file.stem.split('_')[0] != 'marked':
            with Image.open(image_file) as img:
                pixels = img.load()
                width, height = img.size

                if img.mode == 'RGB':
                    # top-left corner
                    r, g, b = pixels[0, 0]
                    r += 1 if r < 255 else -1
                    pixels[0, 0] = (r, g, b)

                img.save(os.path.join(folder_path, image_file.name))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        print("Please provide a folder path to recursively mark outputs within")
        sys.exit(1)

    q = deque([Path(folder_path)])
    
    while q:
        path = q.popleft()
        mark_folder(path)

        for item in Path(path).iterdir():
            if item.is_dir():
                q.append(item)
