from datetime import datetime
from xml.etree.ElementTree import Element
from unraid import get_stats
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom
import re

def generate_feed(data, server):
    servers = data.get('servers')
    server = servers.get(server)
    main = ElementTree.Element('server')
    array_details = ElementTree.SubElement(main, 'details')
    for item in server.get('serverDetails'):
        info = server['serverDetails'].get(item)
        if type(info) is bool:
            if info:
                info = 'true'
            else:
                info = 'false'
        detail_tag = ElementTree.SubElement(array_details, item)
        detail_tag.text = re.sub(r"(?=\&)(.*?)(;)", '', info)
    dockers = ElementTree.SubElement(main, 'dockers')
    for docker in server['docker']['details'].get('containers'):
        container = server['docker']['details']['containers'].get(docker)
        docker_element = ElementTree.SubElement(dockers, 'container', attrib={'id': docker})
        status = ElementTree.SubElement(docker_element, 'status')
        status.text = container.get('status')
        name = ElementTree.SubElement(docker_element, 'name')
        name.text = container.get('name')
        update = ElementTree.SubElement(docker_element, 'upToDate')
        update.text = container.get('uptoDate')

    vms = ElementTree.SubElement(main, 'vms')
    for vm_id in server['vm']['details']:
        vm =  server['vm']['details'].get(vm_id)
        vm_element = ElementTree.SubElement(vms, 'vm')
        for key in vm:
            if type(vm[key]) is list or type(vm[key]) is dict:
                continue
            if key == 'icon' or key == 'xml':
                continue
            info = vm[key]
            detail_tag = ElementTree.SubElement(vm_element, key)
            detail_tag.text = re.sub(r"(?=\&)(.*?)(;)", '', info)

    output = ElementTree.tostring(main)
    prefix = '<?xml version="1.0" encoding="UTF-8"?>'
    return prefix+output.decode('utf-8')

if __name__ == '__main__':
    from unraid import get_stats
    data = get_stats('192.168.0.126')
    xml = generate_feed(data, '192.168.0.126')
    print(xml)