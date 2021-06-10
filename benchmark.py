#!/usr/bin/env python3

"""
Benchmark yoga image optimizations.

Requirements:

* yoga >= 1.0.0
* imagemagick
* cwebp
"""

import time
import pathlib
import subprocess
import csv


ENCODERS = {
    # JPEG
    "libjpeg8-q95": {
        "cmd": "convert -quality 95 {INPUT} {OUTPUT}",
        "ext": ".jpg",
    },
    "yoga-jpeg-q95": {
        "cmd": "yoga image --output-format=jpeg --jpeg-quality=95 {INPUT} {OUTPUT}",
        "ext": ".jpg",
    },
    # PNG
    "libpng16": {
        "cmd": "convert {INPUT} {OUTPUT}",
        "ext": ".png",
    },
    "yoga-png": {
        "cmd": "yoga image --output-format=png {INPUT} {OUTPUT}",
        "ext": ".png",
    },
    "yoga-png-slow": {
        "cmd": "yoga image --output-format=png --png-slow-optimization {INPUT} {OUTPUT}",
        "ext": ".png",
    },
    # WebP (lossy)
    "cwebp-q95": {
        "cmd": "cwebp -quiet -q 95 -alpha_q 95 {INPUT} -o {OUTPUT}",
        "ext": ".webp",
    },
    "yoga-webp-q95": {
        "cmd": "yoga image --output-format=webp --webp-quality=95 {INPUT} {OUTPUT}",
        "ext": ".webp",
    },
    # WebP (lossless)
    "cwebp-lossless": {
        "cmd": "cwebp -quiet -lossless {INPUT} -o {OUTPUT}",
        "ext": ".webp",
    },
    "yoga-webp-lossless": {
        "cmd": "yoga image --output-format=webpl {INPUT} {OUTPUT}",
        "ext": ".webp",
    },
}

IMAGES = sorted(pathlib.Path("./images").glob("*"))
OUTPUT_DIR = pathlib.Path("./output")
COMMAND_PREFIX = "/usr/bin/time --format %M "


def main():
    results_size = [["image", *ENCODERS.keys()]]
    results_time = [["image", *ENCODERS.keys()]]
    results_mem = [["image", *ENCODERS.keys()]]

    # run benchmarks
    for input_image in IMAGES:
        size_line = [input_image.name]
        time_line = [input_image.name]
        mem_line = [input_image.name]
        print("* Benchmarking %s" % input_image.name)
        for encoder in ENCODERS:
            output_image = (
                OUTPUT_DIR
                / input_image.with_suffix(
                    ".%s%s" % (encoder, ENCODERS[encoder]["ext"])
                ).name
            )
            print("  * %s -> %s" % (encoder, output_image.name))

            start_time = time.perf_counter()
            proc = subprocess.Popen(
                COMMAND_PREFIX + ENCODERS[encoder]["cmd"].format(
                    INPUT=input_image.as_posix(),
                    OUTPUT=output_image.as_posix(),
                ),
                shell=True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
            )
            stdout, stderr = proc.communicate()
            end_time = time.perf_counter()

            size_line.append(output_image.stat().st_size)
            time_line.append(end_time - start_time)
            mem_line.append(int(stderr.strip()))

        results_size.append(size_line)
        results_time.append(time_line)
        results_mem.append(mem_line)

    # Write result in csv files
    with open("results.size.csv", "w") as benchfile:
        csvbench = csv.writer(benchfile)
        csvbench.writerows(results_size)
    with open("results.time.csv", "w") as benchfile:
        csvbench = csv.writer(benchfile)
        csvbench.writerows(results_time)
    with open("results.mem.csv", "w") as benchfile:
        csvbench = csv.writer(benchfile)
        csvbench.writerows(results_mem)


if __name__ == "__main__":
    main()
