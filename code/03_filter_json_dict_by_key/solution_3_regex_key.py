import re
import json
from pprint import pprint

import click
from rich import print


def filter_data_by_name(data, search_key):
    if type(data) == dict:
        for key, value in data.items():
            # You can use search or fullmatch depending on what you need
            # if re.search(search_key, key):
            if re.fullmatch(search_key, key):
                yield {key: value}
            else:
                yield from filter_data_by_name(value, search_key)
    elif type(data) == list:
        for item in data:
            yield from filter_data_by_name(item, search_key)


def filter_by_keys(data, keys):
    if type(keys) == str:
        keys = [keys]
    for key in keys:
        result = filter_data_by_name(data, key)
        data = list(result)
    return data


@click.command()
@click.argument("json-file", type=click.File("r"))
@click.argument("keys", nargs=-1, required=True)
def cli(json_file, keys):
    """
    Filter data from JSON-FILE by key.

    Examples:

    \b
        python solution_3_regex_key.py json_files/cfg.json inter.*
        python solution_3_regex_key.py json_files/cfg.json .*off.*
        python solution_3_regex_key.py json_files/cfg.json vlan.*
        python solution_3_regex_key.py json_files/cfg.json .*address.*

    """
    data = json.load(json_file)
    result = filter_by_keys(data, keys)
    print(result)


if __name__ == "__main__":
    cli()
