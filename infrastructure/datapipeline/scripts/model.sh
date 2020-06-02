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
# The second argument is optional, it's for previewing images.  Usage: --preview 96
#
sudo docker run -v $HOME/images:/app/images greyhypotheses/derma:augmentation src/main.py $1 $2
