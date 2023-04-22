import os

import httpx
import uvicorn
from fastapi import FastAPI
import boto3
from pydantic import BaseSettings

app = FastAPI()


class Settings(BaseSettings):
    proxy_port: int

    oidc_domain: str
    client_id_parameter: str
    client_secret_parameter: str


@app.get("/")
def proxy_request():
    r = httpx.get("https://example.com")
    r.raise_for_status()

    return r.content


if __name__ == "__main__":
    config = Settings
    uvicorn.run(app, port=config.proxy_port, log_level="info")
