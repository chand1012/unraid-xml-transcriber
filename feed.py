import xml.etree.ElementTree as ElementTree
import re

def generate_feed(data, server, padding=5, hw=None):
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
    counter = 0
    for docker in server['docker']['details'].get('containers'):
        counter += 1
        container = server['docker']['details']['containers'].get(docker)
        docker_element = ElementTree.SubElement(dockers, 'container')
        
        for item in container:
            if item == 'imageUrl':
                continue
            element = ElementTree.SubElement(docker_element, item)
            element.text = container[item]

    if counter < padding:
        n = padding - counter
        placeholders = ['containerId', 'name', 'status', 'tag', 'uptoDate']
        for _ in range(n):
            element = ElementTree.SubElement(dockers, 'container')
            for item in placeholders:
                ElementTree.SubElement(element, item)

    vms = ElementTree.SubElement(main, 'vms')
    counter = 0 
    for vm_id in server['vm']['details']:
        counter += 1
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

    if counter < padding: # this is supposed to pad the 
        n = padding - counter
        placeholders = ['coreCount', 'id', 'name', 'primaryGPU', 'ramAllocation', 'status']
        for _ in range(n):
            vm_element = ElementTree.SubElement(vms, 'vm')
            for item in placeholders:
                ElementTree.SubElement(vm_element, item)
    if hw:
        usage = ElementTree.SubElement(main, 'usage')
        for item in hw:
            element = ElementTree.SubElement(usage, item)
            element.text = hw[item]
            
    output = ElementTree.tostring(main)
    prefix = '<?xml version="1.0" encoding="UTF-8"?>'
    return prefix+output.decode('utf-8')

if __name__ == '__main__':
    from unraid import get_api_stats
    data = get_api_stats('192.168.0.126')
    xml = generate_feed(data, '192.168.0.126')
    print(xml)