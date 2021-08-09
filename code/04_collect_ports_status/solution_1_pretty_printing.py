import re
import copy
import logging
from pprint import pprint

import yaml
from rich.console import Console
from rich.table import Table


def get_all_ports_stats(data):
    data_stats = copy.deepcopy(data)
    for device, ports in data.items():
        for port_type, details in ports.items():
            for status, port_numbers in details.items():
                data_stats[device][port_type][status] = len(port_numbers)
    return data_stats


def draw_pretty_tables_for_port_info(data, stats=False, full_data=True):
    columns = ["Device", "Port type", "Admin Down", "Down", "Up"]

    if stats:
        data_stats = get_all_ports_stats(data)
        draw_table(data_stats, columns)
    if full_data:
        draw_table(data, columns)


def draw_table(data, columns, ports_in_column=False):
    if ports_in_column:
        join_by = "\n"
    else:
        join_by = ", "

    table = Table()
    for name in columns:
        table.add_column(name, justify="left")

    for device, ports in data.items():
        for index, (port_type, details) in enumerate(ports.items()):
            if all(type(value) == int for value in details.values()):
                num_stats = [
                    f"[red]{num}" if num else f"[green]{num}"
                    for num in details.values()
                ]
                row = (device, port_type, *num_stats)
            else:
                row = (
                    device,
                    port_type,
                    *[join_by.join(port_numbers) for port_numbers in details.values()],
                )
            if index == 0:
                table.add_row(*row)
            else:
                table.add_row("", *row[1:])
        # Empty row for separation
        table.add_row()

    console = Console()
    console.print(table)

