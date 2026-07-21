"""
Project 01: The Glitch Art Generator

Hidden Gem: `pillow` + `numpy` — channel manipulation for glitch aesthetics.

What it does: Takes an image and applies corrupted color channels,
spatial warps, and datamosh-style effects to create modern glitch art.
"""
import os
import numpy as np
from PIL import Image


def glitch_image(image_path, output_path="output_glitch.png", intensity=10):
    img = Image.open(image_path)
    arr = np.array(img)

    # Channel shift — offset R, G, B channels independently
    for i in range(3):
        shift = np.random.randint(-intensity * 3, intensity * 3)
        arr[:, :, i] = np.roll(arr[:, :, i], shift, axis=1)

    # Random row corruption — swap blocks of rows
    for _ in range(intensity):
        start = np.random.randint(0, arr.shape[0] - intensity)
        end = start + np.random.randint(1, intensity)
        arr[start:end] = arr[start:end, ::-1]

    # Datamosh — duplicate random blocks
    for _ in range(intensity // 2):
        src_start = np.random.randint(0, arr.shape[0] - intensity * 2)
        dst_start = np.random.randint(0, arr.shape[0] - intensity * 2)
        length = np.random.randint(2, intensity)
        arr[dst_start:dst_start + length] = arr[src_start:src_start + length]

    result = Image.fromarray(arr)
    result.save(output_path)
    return output_path


def generate_synthetic_image(path="input_sample.png"):
    """Generate a test image if none exists."""
    arr = np.zeros((200, 300, 3), dtype=np.uint8)
    for y in range(200):
        for x in range(300):
            arr[y, x] = [(x * 255) // 300, (y * 255) // 200, ((x + y) * 255) // 500]
    Image.fromarray(arr).save(path)
    return path


def main():
    input_path = "input_sample.png"
    if not os.path.exists(input_path):
        print(f"No input image found. Generating synthetic test image: {input_path}")
        generate_synthetic_image(input_path)

    try:
        output = glitch_image(input_path, intensity=15)
        print(f"Glitch art generated: {output}")
        print("Open the file to see the result!")
    except Exception as e:
        print(f"Error generating glitch art: {e}")


if __name__ == "__main__":
    main()
