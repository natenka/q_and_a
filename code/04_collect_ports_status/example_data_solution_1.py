port_info = {
    "192.168.100.1": {
        "loopback": {
            "administratively down": [],
            "down": [],
            "up": [
                "Loopback0",
                "Loopback11",
                "Loopback55",
                "Loopback77",
                "Loopback99",
                "Loopback100",
                "Loopback200",
            ],
        },
        "physical": {
            "administratively down": [],
            "down": [],
            "up": ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2", "Ethernet0/3"],
        },
        "tunnel": {
            "administratively down": [],
            "down": ["Tunnel0", "Tunnel1", "Tunnel9"],
            "up": [],
        },
    },
    "192.168.100.100": {
        "physical": {
            "administratively down": [],
            "down": [],
            "up": [
                "Ethernet0/0",
                "Ethernet0/1",
                "Ethernet0/2",
                "Ethernet0/3",
                "Ethernet1/0",
                "Ethernet1/1",
                "Ethernet1/2",
                "Ethernet1/3",
                "Ethernet2/0",
                "Ethernet2/1",
                "Ethernet2/2",
                "Ethernet2/3",
                "Ethernet3/0",
                "Ethernet3/1",
                "Ethernet3/2",
                "Ethernet3/3",
            ],
        },
        "vlan": {"administratively down": [], "down": [], "up": ["Vlan1"]},
    },
    "192.168.100.2": {
        "physical": {
            "administratively down": ["Ethernet0/2", "Ethernet0/3"],
            "down": [],
            "up": ["Ethernet0/0", "Ethernet0/1"],
        },
        "subinterface": {
            "administratively down": ["Ethernet0/3.100"],
            "down": [],
            "up": [],
        },
        "loopback": {
            "administratively down": [],
            "down": [],
            "up": ["Loopback0", "Loopback9", "Loopback19", "Loopback77", "Loopback100"],
        },
    },
    "192.168.100.3": {
        "loopback": {"administratively down": [], "down": [], "up": ["Loopback77"]},
        "physical": {
            "administratively down": ["Ethernet0/2", "Ethernet0/3"],
            "down": [],
            "up": ["Ethernet0/0", "Ethernet0/1"],
        },
    },
}
