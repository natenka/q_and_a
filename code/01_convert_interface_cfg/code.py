import re
from pprint import pprint
import ipaddress


def get_mac_from_ip(ip):
    mac = "00:ff:"
    ip = int(ipaddress.ip_address(ip.split("/")[0]))
    hex_ip = f"{ip:08x}"
    hex_ip_str = ":".join([hex_ip[i : i + 2] for i in range(0, len(hex_ip), 2)])
    final_mac = f"{mac}{hex_ip_str}"
    return final_mac


def convert_intf_cfg(source_cfg, dest_cfg):
    intf_cfg_finish_template = (
        'set interfaces ae9 unit {unit} description "{description}"\n'
        'set interfaces ae9 unit {unit} encapsulation vlan-bridge\n'
        'set interfaces ae9 unit {unit} vlan-tags outer {vlan_outer}\n'
        'set interfaces ae9 unit {unit} vlan-tags inner {vlan_inner}\n'
        'set interfaces ae9 unit {unit} family bridge policer input {policer_input}\n'
        'set interfaces ae9 unit {unit} family bridge policer output {policer_output}\n'
        'set interfaces irb unit {unit} description "{description}"\n'
        'set interfaces irb unit {unit} family inet address {address}\n'
        'set interfaces irb unit {unit} mac {hex_address}\n'
    )
    mtu_line = 'set interfaces irb unit {unit} family inet mtu {mtu}\n'
    regex = re.compile(
        r'set interfaces ae0 unit (?P<unit>\d+) description "(?P<description>.+)"\s'
        r"set interfaces ae0 unit (?P=unit) vlan-tags outer (?P<vlan_outer>\d+)\s"
        r"set interfaces ae0 unit (?P=unit) vlan-tags inner (?P<vlan_inner>\d+)\s"
        r"set interfaces ae0 unit (?P=unit) accounting-profile \S+\s"
        r"(set interfaces ae0 unit (?P=unit) family inet mtu (?P<mtu>\d+)\s)?"
        r"set interfaces ae0 unit (?P=unit) family inet policer input (?P<policer_input>\S+)\s"
        r"set interfaces ae0 unit (?P=unit) family inet policer output (?P<policer_output>\S+)\s"
        r"set interfaces ae0 unit (?P=unit) family inet address (?P<address>\S+)"
    )

    with open(source_cfg) as f:
        all_cfg = f.read()
    match_all = regex.finditer(all_cfg)
    with open(dest_cfg, "w") as dst:
        for interface_match in match_all:
            data = interface_match.groupdict()
            data["hex_address"] = get_mac_from_ip(data["address"])
            if data.get("mtu"):
                intf_cfg_template_mtu = intf_cfg_finish_template + mtu_line
                dst.write(intf_cfg_template_mtu.format(**data))
            else:
                dst.write(intf_cfg_finish_template.format(**data))
            dst.write("\n\n")


if __name__ == "__main__":
    convert_intf_cfg("cfg_data.txt", "results.txt")
