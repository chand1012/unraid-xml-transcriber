import json
import os
from os.path import split

import requests


def get_api_stats(hostname, port="3005", https=False):
    http_mode = 'http://'
    if https:
        http_mode = 'https://'
    resp = requests.get(f'{http_mode}{hostname}:{port}/api/getServers')
    data = resp.json()
    resp.close()
    return data

# Calculations from https://rosettacode.org/wiki/Linux_CPU_utilization#Python
def get_hw_stats(path='/proc/'):
    cpu_file = open(os.path.join(path, 'stat'))
    limit = os.cpu_count()+1
    count = 0
    obj = {}
    for line in cpu_file:
        if count >= limit:
            break
        count += 1
        last_idle = last_total = 0
        split_lines = line.strip().split()
        fields = [float(column) for column in split_lines[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle, total - last_total
        obj[split_lines[0]] = 100.0 * (1.0 - idle_delta / total_delta)
    
    cpu_file.close()

    ram_file = open(os.path.join(path, 'meminfo'))
    count = 0
    limit = 3
    for line in ram_file:
        if count >= limit:
            break
        count += 1
        split_lines = line.strip().split()
        obj[split_lines[0].replace(':', '')] = int(split_lines[1])/1024

    obj['MemUsed'] = obj['MemTotal'] - obj['MemAvailable']
    obj['MemPercent'] = obj['MemUsed']/obj['MemTotal']

    ram_file.close()
    return obj

if __name__=='__main__':
    print(get_hw_stats())
