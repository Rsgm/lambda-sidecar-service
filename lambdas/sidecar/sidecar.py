import boto3
import httpx
import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings

app = FastAPI()


class Settings(BaseSettings):
    sidecar_port: int
    credentials_parameter: str

    @property
    def credentials(self):
        client = boto3.client("ssm")

        response = client.get_parameter(
            Name=self.credentials_parameter,
            WithDecryption=True,
        )
        return response["Parameter"]["Value"]


@app.get("/")
def get_token():
    r = httpx.get("https://example.com")
    r.raise_for_status()
    return r.content


if __name__ == "__main__":
    config = Settings()
    uvicorn.run(app, port=config.sidecar_port, log_level="info")
