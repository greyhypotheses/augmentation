#!/bin/bash
cd ~

# Runs the augmentation package.  It requires one integer argument; image_length, i.e.,
# the required length of each prospective square image, such that
#
#   image_length >= augmentation.images.minimum_length
#
# and augmentation.images.minimum_length is declared in the global variables YAML
#
#   https://github.com/greyhypotheses/dictionaries/blob/develop/augmentation/variables.yml
#
sudo docker run -v ~/images:/app/images greyhypotheses/derma:augmentation src/main.py $1
