from pprint import pprint
import re
import os
from datetime import datetime
import json
import copy

import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from rich.console import Console
from rich.table import Table

from solution_1_get_all_ports_info import collect_ports_info


def get_device_phy_ports_info(all_ports_info):
    phy_only = all_ports_info["physical"]
    phy_ports_info = {
        "down": sorted(phy_only["down"] + phy_only["administratively down"]),
        "up": phy_only["up"],
    }
    return phy_ports_info


def get_phy_port_stats(data):
    data_stats = copy.deepcopy(data)
    for device, ports in data.items():
        for status, port_numbers in ports.items():
            data_stats[device][status] = len(port_numbers)
    return data_stats


def filter_phy_ports(all_ports_dict):
    phy_ports_info = {}
    for host, data in all_ports_dict.items():
        phy_ports_info[host] = get_device_phy_ports_info(data)
    return phy_ports_info


def draw_pretty_tables_for_phy_ports(
    data, *, stats=False, full_data=True, table_title=None
):
    columns = ["Device", "Down", "Up"]

    if stats:
        data_stats = get_phy_port_stats(data)
        draw_table_phy_only(data_stats, columns, table_title)
    if full_data:
        draw_table_phy_only(data, columns, table_title)


def draw_table_phy_only(data, columns, title, ports_in_column=False):
    if ports_in_column:
        join_by = "\n"
    else:
        join_by = ", "

    table = Table(title=title)
    for name in columns:
        table.add_column(name, justify="left")

    for device, ports in data.items():
        if all(type(value) == int for value in ports.values()):
            num_stats = [
                f"[red]{num}" if num else f"[green]{num}"
                for num in ports.values()
            ]
            row = (device, *num_stats)
        else:
            row = (
                device,
                *[
                    join_by.join(port_numbers if port_numbers else "")
                    for port_numbers in ports.values()
                ],
            )
        table.add_row(*row)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    all_ports_info = collect_ports_info(devices)
    phy_port_info = filter_phy_ports(all_ports_info)
    pprint(phy_port_info)
    draw_pretty_tables_for_phy_ports(phy_port_info, stats=True)
