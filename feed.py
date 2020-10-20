from datetime import datetime
from xml.etree.ElementTree import ElementTree


def generate_feed(data, server):
    servers = data.get('servers')
    server = servers.get(server)
    