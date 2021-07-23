from pprint import pprint

from rich import print
from rich.tree import Tree
from rich.live import Live
from rich.padding import Padding

from solution_2_ip_and_hostname import parse_cdp, connect_ssh


def generate_tree_from_schema(schema):
    tree = Tree("Topology")
    for s_dev, d_dev_params in schema.items():
        s_dev_tree = tree.add(s_dev)
        for d_dev, params in d_dev_params.items():
            s_dev_tree.add(d_dev)
    return Padding(tree, 4)


def generate_tree_from_schema_ports(schema):
    tree = Tree("Topology")
    for s_dev, d_dev_params in schema.items():
        s_dev_tree = tree.add(s_dev)
        for d_dev, params in d_dev_params.items():
            l_port = params["local_port"]
            r_port = params["remote_port"]
            s_dev_tree.add(l_port).add(r_port).add(d_dev)
    return Padding(tree, 4)


def explore_topology(start_device_ip, params, live):
    visited_hostnames = set()
    visited_ipadresses = set()
    topology = {}
    todo = []
    todo.append(start_device_ip)

    while len(todo) > 0:
        live.update(live_tree_function(topology))  # Rich
        current_ip = todo.pop(0)
        params["host"] = current_ip

        result = connect_ssh(params, "sh cdp neig det")
        if not result:
            continue
        current_host, sh_cdp_neighbors_output = result
        neighbors = parse_cdp(sh_cdp_neighbors_output)
        print("\nFound neighbors", neighbors)

        topology[current_host] = neighbors
        visited_ipadresses.add(current_ip)
        visited_hostnames.add(current_host)

        for neighbor, n_data in neighbors.items():
            neighbor_ip = n_data["ip"]
            if (
                neighbor not in visited_hostnames
                and neighbor_ip not in visited_ipadresses
                and neighbor_ip not in todo
            ):
                print("New neighbor", neighbor_ip)
                todo.append(neighbor_ip)
    return topology


if __name__ == "__main__":
    common_params = {
        "auth_password": "cisco",
        "auth_secondary": "cisco",
        "auth_strict_key": False,
        "auth_username": "cisco",
        "platform": "cisco_iosxe",
        "timeout_socket": 5,
        "timeout_transport": 10,
    }
    start = "192.168.100.1"
    live_tree_function = generate_tree_from_schema
    # live_tree_function = generate_tree_from_schema_ports
    with Live(live_tree_function({}), refresh_per_second=4) as live:  # Rich
        topology = explore_topology(start, common_params, live)
        print(topology)
