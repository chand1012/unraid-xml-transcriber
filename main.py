import os

from fastapi import FastAPI
from starlette.responses import RedirectResponse, Response

from feed import generate_feed
from unraid import get_api_stats, get_hw_stats

app = FastAPI()

@app.get("/")
async def index():
    """
    Redirects to the servers.
    """
    return RedirectResponse(url="/servers")

@app.get("/servers")
async def logs(server: str = '', padding: int = 5, hw: bool = False):
    """
    Gets the servers as an XML RSS feed.
    """
    if server == '':
        server = os.environ.get('LOCAL_IP') or os.environ.get('API_HOST')

    logs = get_api_stats(os.environ.get('API_HOST'))
    hardware = None
    if hw:
        hardware = get_hw_stats()
    feed = generate_feed(logs, server=server, padding=padding, hw=hardware)

    return Response(content=feed, media_type='application/xml')

@app.get('/hwinfo')
async def hwinfo_json():
    return get_hw_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
