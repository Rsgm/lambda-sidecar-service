import pulumi
import pulumi_aws as aws
import pulumi_random as random

secret = random.RandomPassword(
    "random-secret",
    random.RandomPasswordArgs(
        length=32,
    ),
)

credentials_parameter = aws.ssm.Parameter(
    "credentials-parameter",
    aws.ssm.ParameterArgs(
        type="SecureString",
        value=secret.result,
    ),
)
