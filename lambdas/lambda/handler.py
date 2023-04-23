import os

import httpx

SIDECAR_PORT = os.environ["SIDECAR_PORT"]


def lambda_handler(event=None, context=None):
    r = httpx.get(f"http://localhost:{SIDECAR_PORT}")
    r.raise_for_status()
    print(r.content)