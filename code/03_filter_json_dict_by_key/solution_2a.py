import json
from pprint import pprint

import click
from rich import print


def filter_data_by_name(data, search_key):
    results = []
    if type(data) == dict:
        for key, value in data.items():
            if key == search_key:
                results.append(value)
            else:
                results.extend(filter_data_by_name(value, search_key))
    elif type(data) == list:
        for item in data:
            results.extend(filter_data_by_name(item, search_key))
    return results


def filter_by_keys(data, keys):
    if type(keys) == str:
        keys = [keys]
    for key in keys:
        data = filter_data_by_name(data, key)
    return data


@click.command()
@click.argument("json-file", type=click.File("r"))
@click.argument("keys", nargs=-1, required=True)
def cli(json_file, keys):
    """
    Filter data from JSON-FILE by key.

    Examples:

    \b
        python solution_2_without_generator.py json_files/repos.json owner id
        python solution_2_without_generator.py json_files/cfg.json name
        python solution_2_without_generator.py json_files/cfg.json interface name
        python solution_2_without_generator.py json_files/cfg.json address name
        python solution_2_without_generator.py json_files/cfg.json login name

    """
    data = json.load(json_file)
    result = filter_by_keys(data, keys)
    print(result)


if __name__ == "__main__":
    cli()
