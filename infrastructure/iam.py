import json

import pulumi
import pulumi_aws as aws

from infrastructure import ssm

lambda_role = aws.iam.Role(
    "test-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
    inline_policies=[
        aws.iam.RoleInlinePolicyArgs(
            name="policy",
            policy=pulumi.Output.all(
                parameters=[
                    ssm.client_id_parameter.arn,
                    ssm.client_secret_parameter.arn,
                ]
            ).apply(
                lambda args: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": [
                                    "logs:CreateLogGroup",
                                    "logs:CreateLogStream",
                                    "logs:PutLogEvents",
                                ],
                                "Resource": "arn:aws:logs:*:*:*",
                            },
                            {
                                "Effect": "Allow",
                                "Action": ["ssm:GetParameter"],
                                "Resource": args["parameters"],
                            },
                        ],
                    }
                )
            ),
        ),
    ],
)
