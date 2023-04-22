import json

import pulumi
import pulumi_aws as aws

lambda_role = aws.iam.Role(
    "test-role",
    inline_policies=[
        aws.iam.RoleInlinePolicyArgs(
            name="policy",
            policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": [
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            "Resource": "arn:aws:logs:*:*:*",
                            "Effect": "Allow",
                        }
                    ],
                }
            ),
        ),
    ],
)
