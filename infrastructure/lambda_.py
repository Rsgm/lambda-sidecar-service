import pulumi
import pulumi_aws as aws

from . import iam

# Create an AWS Lambda function
lambda_function = aws.lambda_.Function(
    "my-lambda-function",
    runtime="python3.8",
    handler="handler.lambda_handler",
    role=iam.lambda_role,  # Replace with your own IAM role ARN
    code=pulumi.FileArchive("dist/lambda.zip"),
)
