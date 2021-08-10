import re
import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from pprint import pprint

import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.logging import RichHandler

from solution_1_pretty_printing import draw_pretty_tables_for_port_info, draw_table


logging.getLogger("scrapli").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

logging.basicConfig(
    format="%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="[%X]",
    handlers=[RichHandler()],
)


def get_show_output(params, command):
    host = params.get("host")
    logging.info(f">>> Connecting to {host}")
    try:
        with Scrapli(**params) as ssh:
            response = ssh.send_command(command)
            output = response.result
            return output
    except ScrapliException as error:
        logging.critical(f"Error {error}. Host {host}")


def get_show_from_devices(devices, command, max_threads=10):
    host_output_dict = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(get_show_output, devices, repeat(command))
        for dev, output in zip(devices, results):
            host_output_dict[dev["host"]] = output
    return host_output_dict


def get_device_all_ports_info(output):
    regex = (
        r"(?P<port>\S+) +\S+ +\w+ \w+ +"
        r"(?P<admin_status>administratively down|up|down) +(?P<status>up|down)"
    )
    interface_type_regex = (
        r"(?P<loopback>Loopback\d+)"
        r"|(?P<tunnel>Tunnel\d+)"
        r"|(?P<subinterface>\S+\d\.\d+)"
        r"|(?P<vlan>Vlan\d+)|(?P<physical>\S+)"
    )
    status_keys = ["administratively down", "down", "up"]

    devices_stats = {}
    for m in re.finditer(regex, output):
        admin_status, status, port = m.group("admin_status", "status", "port")
        intf_type_m = re.search(interface_type_regex, port)
        intf_type = intf_type_m.lastgroup
        if admin_status == "administratively down":
            status = admin_status
        if intf_type not in devices_stats:
            devices_stats[intf_type] = {k: [] for k in status_keys}
        devices_stats[intf_type][status].append(port)
    return devices_stats


def collect_ports_info(devices, command="sh ip int br"):
    stats = {}
    host_output_dict = get_show_from_devices(devices, command)
    for host, output in host_output_dict.items():
        if output:
            stats[host] = get_device_all_ports_info(output)
    return stats


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    port_info = collect_ports_info(devices)
    pprint(port_info)
    # rprint(port_info) # Rich print
    draw_pretty_tables_for_port_info(port_info, stats=True)
