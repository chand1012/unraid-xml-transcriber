import os

from fastapi import FastAPI
from starlette.responses import RedirectResponse, Response

from feed import generate_feed
from unraid import get_stats

app = FastAPI()

@app.get("/")
async def index():
    """
    Redirects to the servers.
    """
    return RedirectResponse(url="/servers")

@app.get("/servers")
async def logs(server: str = ''):
    """
    Gets the servers as an XML RSS feed.
    """
    if server is '':
        server = os.environ.get('API_HOST')

    logs = get_stats(os.environ.get('API_HOST'))
    feed = generate_feed(logs, server=server)

    return Response(content=feed, media_type='application/xml')
