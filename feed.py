from datetime import datetime

from rfeed import *


def generate_feed(data, server):
    items = []
    servers = data.get('servers')
    server = servers[server]

    statString = f''

    items += [Item(
        title='Stats',
        link=f'https://{server}',
        pubDate=datetime.now(),
        description=f''
    )]
