#!/bin/bash
cd ~

# Import required bash script files
aws s3 cp s3://engineering.infrastructure.definitions/projects/augmentation/infrastructure/datapipeline/scripts/model.sh .
aws s3 cp s3://engineering.infrastructure.definitions/projects/augmentation/infrastructure/datapipeline/scripts/synchronise.sh .
