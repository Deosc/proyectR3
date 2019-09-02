import subprocess
import xml.etree.ElementTree as ET
import os
import ping_logger
import re

IP_ROUTE_COMMANDS = ["ip", "route"]
OUTPUT_SCAN_FILEPATH = '/tmp/namp_scan.xml'
NMAP_SCAN_COMMANDS = ['nmap', '-sn', '-oX', OUTPUT_SCAN_FILEPATH, '--min-parallelism', '100']
SNMP_GET_ROUTABLE_CMD = ['snmpwalk', '-v', '2c', '-c', 'public', '%s', '.1.3.6.1.2.1.4.24.4.1.16']


def scan_networks(networks):
    hosts = []
    for net in networks:
        commands = NMAP_SCAN_COMMANDS[:]
        commands.append(net)
        res_code = subprocess.call(commands, stdout=open(os.devnull, 'wb'))
        if res_code == 0:
            scan_tree = read_xml(OUTPUT_SCAN_FILEPATH)
            for host_node in scan_tree.findall('host'):
                address = host_node.find('address').attrib['addr']
                hosts.append(address)
        else:
            print(' '.join(commands) + ' error')  
    return hosts


def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def get_networks(snmp_host):
    SNMP_GET_ROUTABLE_CMD[5] = snmp_host
    output = subprocess.check_output(SNMP_GET_ROUTABLE_CMD).decode('UTF-8')
    networks = []
    for line in output.split('\n'):
        line = line.strip()
        if len(line) != 0:
            match = re.match(r"iso\.3\.6\.1\.2\.1\.4\.24\.4\.1\.16\.(.+)", line)
            if match:
                ip_row = match.groups()[0]
                matches = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.?)", ip_row)
                ip = matches[0][:-1]
                if (ip != '0.0.0.0'):
                    netmask_bits = netmask_to_cidr(matches[1][:-1])
                    networks.append(f"{ip}/{netmask_bits}")
    return networks


def read_xml(path):
    with open(path) as file:
        tree = ET.parse(path)
    return tree
        

if __name__ == '__main__':
    snmp_host = "10.0.25.2"
    networks = get_networks(snmp_host)
    print(networks)
    hosts = scan_networks(networks)
    print(hosts)
    ping_logger.ping_log(hosts)
