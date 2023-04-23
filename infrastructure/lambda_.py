import pulumi
import pulumi_aws as aws
import pulumi_command as command
import uuid

from . import iam, ssm


LAMBDA_DIR = "lambdas/lambda"
LAMBDA_BUILD = f"build/lambda_{uuid.uuid4()}"
LAMBDA_ZIP = "dist/lambda.zip"
command.local.run(
    command=f"{LAMBDA_DIR}/package.sh",
    environment={
        "LAMBDA_DIR": LAMBDA_DIR,
        "OUTPUT_ZIP": LAMBDA_ZIP,
        "BUILD_DIR": LAMBDA_BUILD,
    },
)

SIDECAR_DIR = "lambdas/sidecar"
SIDECAR_BUILD = f"build/sidecar_{uuid.uuid4()}"
SIDECAR_ZIP = "dist/sidecar.zip"
command.local.run(
    command=f"{SIDECAR_DIR}/package.sh",
    environment={
        "LAMBDA_DIR": SIDECAR_DIR,
        "OUTPUT_ZIP": SIDECAR_ZIP,
        "BUILD_DIR": SIDECAR_BUILD,
    },
)

sidecar_layer = aws.lambda_.LayerVersion(
    "test-sidecar-layer",
    code=pulumi.FileArchive(SIDECAR_ZIP),
    layer_name="oidc_client_sidecar",
)

aws.lambda_.LayerVersionPermission(
    "test-sidecar-layer-permission",
    action="lambda:GetLayerVersion",
    layer_name=sidecar_layer.layer_name,
    principal=aws.get_caller_identity().account_id,
    statement_id="test-sidecar-layer-account-permission",
    version_number=1,
)

lambda_function = aws.lambda_.Function(
    "test-lambda",
    aws.lambda_.FunctionArgs(
        runtime="python3.9",
        handler="handler.lambda_handler",
        role=iam.lambda_role.arn,
        code=pulumi.FileArchive(LAMBDA_ZIP),
        reserved_concurrent_executions=2,
        layers=[sidecar_layer.arn],
        environment=aws.lambda_.FunctionEnvironmentArgs(
            variables={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/lambda_wrapper.sh",
                "SIDECAR_PORT": "31566",
                "OIDC_ISSUER": "example.com",
                "CLIENT_ID_PARAMETER": ssm.client_id_parameter.name,
                "CLIENT_SECRET_PARAMETER": ssm.client_secret_parameter.name,
            },
        ),
    ),
)
