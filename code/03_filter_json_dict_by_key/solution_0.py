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


@click.command()
@click.argument("json-file", type=click.File("r"))
@click.argument("key")
def cli(json_file, key):
    """
    Filter data from JSON-FILE by key.

    Examples:

    \b
        python solution_0.py json_files/basic.json name

    """
    data = json.load(json_file)
    result = filter_data_by_name(data, key)
    print(result)


if __name__ == "__main__":
    cli()
