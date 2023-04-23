import pulumi
import pulumi_aws as aws
import pulumi_random as random

client_id = random.RandomPassword(
    "random-client-id",
    random.RandomPasswordArgs(
        length=16,
        special=False,
    ),
)
client_secret = random.RandomPassword(
    "random-client-secret",
    random.RandomPasswordArgs(
        length=32,
    ),
)

client_id_parameter = aws.ssm.Parameter(
    "oidc_client_id",
    aws.ssm.ParameterArgs(
        type="SecureString",
        value=client_id.result,
    ),
)
client_secret_parameter = aws.ssm.Parameter(
    "oidc_client_secret",
    aws.ssm.ParameterArgs(
        type="SecureString",
        value=client_secret.result,
    ),
)
