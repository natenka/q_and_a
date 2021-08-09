from pprint import pprint
import re
import os
from datetime import datetime
import json

import yaml
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from solution_1_get_all_ports_info import collect_ports_info
from solution_2_physical_only_info import (
    filter_phy_ports,
    draw_pretty_tables_for_phy_ports,
    draw_table_phy_only,
)


def get_last_record_filename(path="collected_data"):
    files = [f for f in os.listdir(path) if not f.startswith(".")]
    if files:
        return os.path.join(path, max(files))
    else:
        return None


def get_diff_dict(old, new):
    """
    Сравнивает два словаря формата
    {'R1': {'down': ['Ethernet0/1', 'Ethernet0/2'],
            'up': ['Ethernet0/0', 'Ethernet0/3']},
     'R2': {'down': ['Ethernet0/2'],
            'up': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet0/3']},
     'R3': {'down': ['Ethernet0/2', 'Ethernet0/3'],
            'up': ['Ethernet0/0', 'Ethernet0/1']},
     'SW1': {'down': ['Ethernet2/0', 'Ethernet2/1'],
             'up': ['Ethernet0/0', 'Ethernet0/1', 'Ethernet3/3']}}
    Возвращает отличия в виде словаря
    {'R1': {'down->up': {'Ethernet0/1', 'Ethernet0/2'}, 'up->down': None},
     'R2': {'down->up': None, 'up->down': {'Ethernet0/3'}},
     'R3': {'down->up': None, 'up->down': None},
     'SW1': {'down->up': None, 'up->down': None}}
    """
    diff = {}
    changes = ["up->down", "down->up"]
    for device, ports in new.items():
        diff_dict = dict.fromkeys(changes)
        new_up = set(new[device]["up"])
        old_up = set(old[device]["up"])
        if new_up - old_up:
            diff_dict["down->up"] = new_up - old_up
        if old_up - new_up:
            diff_dict["up->down"] = old_up - new_up
        diff[device] = diff_dict
    return diff


def pretty_diff(data):
    # columns order as in changes list (get_diff)
    columns = ["Device", "Up -> Down", "Down -> Up"]
    draw_table_phy_only(data, columns, title="Difference")


def get_current_phy_ports_data(
    devices, save=True, path_template="collected_data/free_ports_{}.json"
):
    current_data = filter_phy_ports(collect_ports_info(devices))
    if save:
        filename_with_today_date = path_template.format(datetime.now().date())
        with open(filename_with_today_date, "w") as f:
            json.dump(current_data, f, indent=2)
    return current_data


def compare_current_port_status_with_last_status(
    current_data, last_saved_filename, pprint_data_tables=True
):
    with open(last_saved_filename) as f:
        last_recorded_data = json.load(f)
    if pprint_data_tables:
        draw_pretty_tables_for_phy_ports(
            last_recorded_data, table_title=last_saved_filename
        )
        draw_pretty_tables_for_phy_ports(
            current_data, table_title=f"Current Data {datetime.now().date()}"
        )

    diff_dict = get_diff_dict(last_recorded_data, current_data)
    pretty_diff(diff_dict)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    new_data = get_current_phy_ports_data(devices, save=False)
    last_saved_data_filename = get_last_record_filename()

    if not last_saved_data_filename:
        rprint("\n[red]No historical data!\n")
        draw_pretty_tables_for_phy_ports(new_data, table_title="Current Data")
    else:
        compare_current_port_status_with_last_status(new_data, last_saved_data_filename)
