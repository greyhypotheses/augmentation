#!/bin/bash
cd ~

# Delivering the results files to Amazon S3
directory=$1.$1
aws s3 rm s3://deep.learning.images/$directory/ --recursive
aws s3 sync ~/images/zips/ s3://deep.learning.images/$directory/zips/
aws s3 cp ~/images/inventory.csv s3://deep.learning.images/$directory/
