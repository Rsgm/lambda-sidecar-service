import os

import httpx
import uvicorn
from fastapi import FastAPI
import boto3
from pydantic import BaseSettings

app = FastAPI()


class Settings(BaseSettings):
    sidecar_port: int

    # oidc_issuer: str
    # client_id_parameter: str
    # client_secret_parameter: str

    @property
    def client_id(self):
        # client = boto3.client("ssm")
        # client.get
        return


@app.get("/")
def get_token():
    r = httpx.get("https://example.com")
    r.raise_for_status()

    return r.content


if __name__ == "__main__":
    config = Settings()
    uvicorn.run(app, port=config.sidecar_port, log_level="info")
