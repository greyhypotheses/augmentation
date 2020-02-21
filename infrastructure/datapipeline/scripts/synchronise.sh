#!/bin/bash
cd ~

# Directory name based on square image dimensions.
directory=$1.$1

# Delivering the results files to Amazon S3.
aws s3 rm s3://deep.learning.images/$directory/ --recursive
aws s3 sync $HOME/images/zips/ s3://deep.learning.images/$directory/zips/
aws s3 cp $HOME/images/inventory.csv s3://deep.learning.images/$directory/
