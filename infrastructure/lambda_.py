import pulumi
import pulumi_aws as aws
import pulumi_command as command
import uuid

from . import iam


LAMBDA_DIR = "lambdas/lambda"
LAMBDA_BUILD = "lambdas/lambda"
lambda_package = command.local.run(
    command=f"{LAMBDA_DIR}/package.sh",
    archive_paths="dist/sidecar",
    environment={
        "LAMBDA_DIR": LAMBDA_DIR,
        "BUILD_DIR": LAMBDA_BUILD,
    },
)

SIDECAR_DIR = "lambdas/sidecar"
SIDECAR_BUILD = f"build/sidecar_{uuid.uuid4()}"
sidecar_package = command.local.run(
    command=f"{SIDECAR_DIR}/package.sh",
    archive_paths="dist/sidecar",
    environment={
        "LAMBDA_DIR": SIDECAR_DIR,
        "BUILD_DIR": SIDECAR_BUILD,
    },
)

lambda_function = aws.lambda_.Function(
    "test-lambda",
    aws.lambda_.FunctionArgs(
        runtime="python3.10",
        handler="handler.lambda_handler",
        role=iam.lambda_role,
        code=lambda_package,
        environment={
            "SIDECAR_PORT": "31566",
            # "OIDC_DOMAIN": oidc_domain,
            # "CLIENT_ID_PARAMETER": client_id_parameter,
            # "CLIENT_SECRET_PARAMETER": client_secret_parameter,
        },
    ),
)
