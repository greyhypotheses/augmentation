#!/bin/bash
cd ~

# Import a required script file
aws s3 cp s3://engineering.infrastructure.definitions/projects/augmentation/infrastructure/datapipeline/scripts/model.sh .
aws s3 cp s3://engineering.infrastructure.definitions/projects/augmentation/infrastructure/datapipeline/scripts/synchronise.sh .
