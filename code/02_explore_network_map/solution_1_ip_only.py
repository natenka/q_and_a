import re
from pprint import pprint
from queue import Queue

import click
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException


def connect_ssh(params, command, verbose=True):
    if verbose:
        print("Connect...", params["host"])
    try:
        with Scrapli(**params) as ssh:
            prompt = ssh.get_prompt()
            reply = ssh.send_command(command)
            output = reply.result
            return f"{prompt}\n{output}"
    except ScrapliException as error:
        print(error)


def parse_cdp(output):
    regex = (
        r"IP address: (?P<ip>\S+)\n"
        r".*?"
        r"Interface: (?P<local_port>\S+), +"
        r"Port ID \(outgoing port\): (?P<remote_port>\S+)"
    )
    result = {}

    match_iter = re.finditer(regex, output, re.DOTALL)
    for match in match_iter:
        groupdict = match.groupdict()
        ip = groupdict.pop("ip")
        result[ip] = groupdict
    return result


def explore_topology(start_device, params):
    visited_hosts = set()
    topology = {}
    todo = Queue()
    todo.put(start_device)

    while todo.qsize() > 0:
        current = todo.get()
        params["host"] = current
        if current in visited_hosts:
            continue
        output = connect_ssh(params, "sh cdp neig det")
        if not output:
            continue
        connections = parse_cdp(output)
        topology[current] = connections
        for neighbor, n_data in connections.items():
            if neighbor not in visited_hosts:
                todo.put(neighbor)
        visited_hosts.add(current)
    return topology


@click.command()
@click.argument("start")
def cli(start):
    """
    Run CDP network explorer. Enter START IP address.

    Example:

    \b
        python solution_1_ip_only.py 192.168.100.1
    """
    common_params = {
        "auth_password": "cisco",
        "auth_secondary": "cisco",
        "auth_strict_key": False,
        "auth_username": "cisco",
        "platform": "cisco_iosxe",
        "timeout_socket": 5,
        "timeout_transport": 10,
    }
    topology = explore_topology(start, params=common_params)
    pprint(topology)


if __name__ == "__main__":
    cli()
