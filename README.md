# Benchmark of YOGA Image

This repository contains images, scripts and data used to benchmark YOGA image.


## Requirements

The following softwares are required to run the benchmark:

* Python >= 3.8
* yoga >= 1.0.0
* imagemagick
* cwebp

To install requirements on Debian / Ubuntu, run the following command:

    sudo apt install build-essential python3-dev python3-pip imagemagick webp
    sudo pip3 install yoga


## Usage

* Put images to benchmark in the `images/` folder.
* Run `./list-images.py` to regenerate `images.list.csv`.
* Run `./benchmark.py` to run the benchmark. This will generate:
  * `result.size.csv` that contains the optimized file size (in Bytes),
  * `result.mem.csv` that contains the maximum amount of memory (in kB) used during the optimization,
  * `result.time.csv` that contains the optimization time (in seconds).

**WARNING:** With default images, this benchmark ran for about 4h on my machine and used up to 3.7 GB of memory.


## Links

* YOGA: https://github.com/wanadev/yoga
* YOGA Image Optimizer: https://github.com/flozz/yoga-image-optimizer
