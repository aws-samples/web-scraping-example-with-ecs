#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

set -e

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output text --query 'Account')
AWS_REGION=$(aws configure get region)

read -p "Enter the name of the bucket that will be created to store your output: "  S3_BUCKET_NAME

aws s3 mb s3://$S3_BUCKET_NAME

aws ecr create-repository \
    --repository-name demo/selenium-ecs


aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t demo/selenium-ecs .

docker tag demo/selenium-ecs:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/demo/selenium-ecs:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/demo/selenium-ecs:latest

echo Image URL: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/demo/selenium-ecs:latest
echo Bucket S3: $S3_BUCKET_NAME











