import requests
import json

def get_stats(hostname, port="3005", https=False):
    http_mode = 'http://'
    if https:
        http_mode = 'https://'
    resp = requests.get(f'{http_mode}{hostname}:{port}/api/getServers')
    data = resp.json()
    resp.close()
    return data

if __name__=='__main__':
    data = get_stats('192.168.254.1')
    servers = data.get('servers')
    for server in servers:
        name = servers[server]['serverDetails'].get('title')
        with open(f'{name}.json', 'w') as f:
            f.write(json.dumps(servers[server], indent=4, sort_keys=True))