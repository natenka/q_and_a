import re
from pprint import pprint
import ipaddress

from jinja2 import Environment, FileSystemLoader


def get_mac_from_ip(ip):
    mac = "00:ff:"
    ip = int(ipaddress.ip_address(ip.split("/")[0]))
    hex_ip = f"{ip:08x}"
    hex_ip_str = ":".join([hex_ip[i : i + 2] for i in range(0, len(hex_ip), 2)])
    final_mac = f"{mac}{hex_ip_str}"
    return final_mac


def convert_intf_cfg(source_cfg, dest_cfg):
    regex = re.compile(
        r'set interfaces ae0 unit (?P<unit>\d+) description "(?P<description>.+)"\s'
        r"set interfaces ae0 unit (?P=unit) vlan-tags outer (?P<vlan_outer>\d+)\s"
        r"set interfaces ae0 unit (?P=unit) vlan-tags inner (?P<vlan_inner>\d+)\s"
        r"(set interfaces ae0 unit (?P=unit) family inet mtu (?P<mtu>\d+)\s)?"
        r"set interfaces ae0 unit (?P=unit) family inet policer input (?P<policer_input>\S+)\s"
        r"set interfaces ae0 unit (?P=unit) family inet policer output (?P<policer_output>\S+)\s"
        r"set interfaces ae0 unit (?P=unit) family inet address (?P<address>\S+)"
    )
    env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("interface_template.j2")

    with open(source_cfg) as f:
        all_cfg = f.read()
    match_all = regex.finditer(all_cfg)
    with open(dest_cfg, "w") as dst:
        for interface_match in match_all:
            data = interface_match.groupdict()
            data["hex_address"] = get_mac_from_ip(data["address"])
            dst.write(template.render(data))
            dst.write("\n\n")


if __name__ == "__main__":
    convert_intf_cfg("cfg_data.txt", "results.txt")
