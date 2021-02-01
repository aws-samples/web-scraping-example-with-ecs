# Web Scraping Example

This repository contains hands on content that will guide you through building a simple application to perform web scraping using AWS in two ways. One of them we have been using a FaaS approach (AWS Lambda) and the other one a Container approach (ECS).

# Prerequisites

- AWS Account
- AWS CLI installed and pre configured AWS Credentials
- [Docker](https://docs.docker.com/get-docker/)
- Pre configured VPC with minimum of 2 public subnets

**THIS WORKSHOP WAS TESTED IN US-EAST-1 REGION**

# Overview of Hands on Labs

In the demonstration we are going to build a stack to navigate on a web page and extract content from a URL and store the output in a S3 Bucket.

# Getting Started Running Web Scraping using Amazon ECS

The purpose of this demo is to build a stack that uses Amazon ECS, Selenium, Requests and BeautifulSoup in order to extract content from a given URL. We are using an Amazon ECS, Python3.6 and Selenium to navigate on a page and use the Requests lib to get the HTML file, then we use BeautifulSoup to extract some elements like the all texts and URL's from the page, then we save the output as .txt file in a S3 Bucket.

**This demo was tested in us-east-1**

# Setup instructions

First of all we need to setup the foundation for our solution, that consists of create the bucket to store our output and the ECR to store our scraping worker docker image.

A script was developed to help in that task, simple run:

```bash
    ./setup.sh
```

## CloudFormation
```bash
    aws cloudformation create-stack \
        --stack-name ecs-demo-scraping \
        --template-body file://cloudformation/ecs-stack.yaml \
        --parameters ParameterKey=ClusterName,ParameterValue=ecs-cluster-demo \
        ParameterKey=ServiceName,ParameterValue=scraping-worker \
        ParameterKey=ImageUrl,ParameterValue=<IMAGE_URL> \
        ParameterKey=BucketName,ParameterValue=<S3_BUCKET> \
        ParameterKey=VpcId,ParameterValue=<VPC_ID> \
        ParameterKey=VpcCidr,ParameterValue=<VPC_CIDR> \
        ParameterKey=PubSubnet1Id,ParameterValue=<PUB_SUBNET_1_ID> \
        ParameterKey=PubSubnet2Id,ParameterValue=<PUB_SUBNET_2_ID> \
        --capabilities CAPABILITY_IAM
```

**Values to be replaced:**

**<IMAGE_URL>** - The URI of ECR the image uploaded in the script **setup.sh** (ImageUrl).

**<BUCKET_NAME>** - Our created bucket for output files.

**<VPC_ID>** - VPC that we will use to provision ECS cluster.

**<VPC_CIDR>** - VPC CIDR that we will use to provision ECS cluster.

**<PUB_SUBNET_1_ID>** - First public Subnet ID that we will use to provision ECS cluster.

**<PUB_SUBNET_2_ID>** - Second public Subnet ID that we will use to provision ECS cluster.


# Testing the solution

Check your S3 Bucket for the output file. You will see our solutions is looking for "I love Python" in Python official website because these were my parameters in our code, but you can change the way that we are doing this, this was just for a demonstration. 
    
**Our ECS cluster will run several web scraping tasks since we set the desired running tasks to 1, so when it finishes a scraping task it will start a new task in order to perform web scraping. Don't forget to clean up all of our provisioned stack because this may apply some additional costs**

# Cleaning up:

```bash
    aws cloudformation delete-stack \
        --stack-name ecs-demo-scraping
```

- Delete all the files inside of the provisioned S3 bucket.

```bash
    aws s3 rm s3://<BUCKET-NAME> --recursive
```

- Delete the provisioned S3 bucket.

```bash
    aws s3 rb s3://<BUCKET-NAME> --force
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
