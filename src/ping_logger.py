import os


TRIES_NUMBER = 3
PING_TIMEOUT_MS = 500

def ping_log(hosts):
    reachable_hosts = set()
    unreachable_hosts = set()
    for host in hosts:
        tries = 1*TRIES_NUMBER
        while True:
            response = os.system(
                f'fping -c1 -t{PING_TIMEOUT_MS} {host} >/dev/null 2>&1')
            if response == 0:
                reachable_hosts.add(host)
                print (host, 'is up')
                break
            else:
                if tries <= 0:
                    unreachable_hosts.add(host)
                    break
                else:
                    tries -= 1
                    print (f'{host} is down, {tries} tries left')
    print("Reachable hosts: ", reachable_hosts)
    print("Unreacheable hosts: ", unreachable_hosts)
    return reachable_hosts, unreachable_hosts

if __name__ == "__main__":
    hosts = [
        '8.8.8.8',
        '31.13.89.35'
    ]
    with open('ips.txt', 'rt') as file:
        for line in file.readlines():
            hosts.append(line.strip())
        ping_log(hosts)
