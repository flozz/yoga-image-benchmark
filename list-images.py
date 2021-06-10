#!/usr/bin/env python3

"""
List images and images dimentions.

Requirements:

* Pillow
"""

import pathlib
import csv

from PIL import Image


IMAGES = sorted(pathlib.Path("./images").glob("*"))


def main():
    result = [
        ["image", "width", "height"]
    ]

    # run benchmarks
    for input_image in IMAGES:
        img = Image.open(input_image)
        result.append([input_image.name, img.width, img.height])

    with open("images.list.csv", "w") as csvfile:
        csv_ = csv.writer(csvfile)
        csv_.writerows(result)


if __name__ == "__main__":
    main()
