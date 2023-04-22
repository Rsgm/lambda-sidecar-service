import httpx


def handle(event=None, context=None):
    r = httpx.get("http://localhost:31934")
    r.raise_for_status()
    print(r.content)
