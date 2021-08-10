## Collect Port Status Information

The task is to collect information about the status of ports on the devices
(up/down/admin down for Cisco IOS). At the first step, information is collected
about all ports (Loopback/physical/Tunnel/...) and their status. At the second
step, only physical ports should be selected from the collected information.
And on the third, you need to save information about the status of ports on
a specific day in files and add the ability to compare changes in the status
of ports (the current status with the last recorded one).

### The first step is to collect information about the status of ports

The task is to collect information about the status of ports on the devices
(up/down/admin down for Cisco IOS). Information about all ports
(Loopback/physical/Tunnel/...) and their status is collected.

An example
of a summary dictionary (full output in example_data_solution_1.py):

```python
{
    "192.168.100.1": {
        "loopback": {
            "administratively down": [],
            "down": [],
            "up": ["Loopback0", "Loopback11"],
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
}
```

It is convenient to work with information in the form of a dictionary further,
but it is not very convenient to perceive it visually, therefore, it is also
necessary to display information about the status of ports in a tabular form,
for example (it may just be output in columns):

![solution_1](https://github.com/natenka/q_and_a/blob/main/images/qa_04_1_table_all_info.png?raw=true)

Additionally, you can add a summary of the number of ports without listing specific ports, for example:

![solution_1_stats](https://github.com/natenka/q_and_a/blob/main/images/qa_04_1_table_stats.png?raw=true)

### The second step is to filter out only physical ports from the collected information

The second step is to filter out only physical ports from the collected
information and simplify the port statuses. Now there is no need to distinguish
between the statuses of administratively down and down, both statuses
should be recorded as down.


If at the previous step the dictionary with all ports was like this:

```python
{
    "loopback": {"administratively down": [], "down": [], "up": ["Loopback77"]},
    "physical": {
        "administratively down": ["Ethernet0/2"],
        "down": ["Ethernet0/3"],
        "up": ["Ethernet0/0", "Ethernet0/1"],
    },
    "subinterface": {
        "administratively down": ["Ethernet0/3.100"],
        "down": [],
        "up": [],
    },
}
```

After filtering, you should get the following dictionary (full dictionary in the file example_data_solution_2.py):
)
```python
{
    "down": ["Ethernet0/2", "Ethernet0/3"],
    "up": ["Ethernet0/0", "Ethernet0/1"],
}
```

As with the first step, you need to display information on ports in the form of a table:

![solution_2](https://github.com/natenka/q_and_a/blob/main/images/qa_04_2_table_all_info.png?raw=true)

And add a summary of the number of ports, without listing specific ports:

![solution_2_stats](https://github.com/natenka/q_and_a/blob/main/images/qa_04_2_table_stats_info.png?raw=true)

### The third step is tracking changes in the status of ports

After the second step, there is information about the status of the physical ports.
Now you need to write this information (dictionary) in JSON format to files
and add the recording date to the file name (example in collected_data/free_ports_2021-07-28.json).

Now imagine that several days have passed and we need to compare the current
status of ports with the last record and show which ports have changed
from up to down status and vice versa.

For example, there is such data (old_data data that was previously written to a file, new_data data read from the network):

```python
old_data = {
    "192.168.100.1": {
        "down": ["Ethernet0/1", "Ethernet0/2"],
        "up": ["Ethernet0/0", "Ethernet0/3"],
    },
    "192.168.100.100": {
        "down": ["Ethernet0/0", "Ethernet0/1"],
        "up": ["Ethernet0/2", "Ethernet0/3"],
    },
    "192.168.100.2": {
        "down": ["Ethernet0/2"],
        "up": ["Ethernet0/0", "Ethernet0/1", "Ethernet0/3"],
    },
    "192.168.100.3": {
        "down": ["Ethernet0/2", "Ethernet0/3"],
        "up": ["Ethernet0/0", "Ethernet0/1"],
    },
}

new_data = {
    "192.168.100.1": {
        "down": [],
        "up": ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2", "Ethernet0/3"],
    },
    "192.168.100.100": {
        "down": [],
        "up": ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2", "Ethernet0/3"],
    },
    "192.168.100.2": {
        "down": ["Ethernet0/2", "Ethernet0/3"],
        "up": ["Ethernet0/0", "Ethernet0/1"],
    },
    "192.168.100.3": {
        "down": ["Ethernet0/2", "Ethernet0/3"],
        "up": ["Ethernet0/0", "Ethernet0/1"],
    },
}
```

The resulting dictionary with changes in port status should be like this:

```python
diff_dict = {
    "192.168.100.1": {"down->up": {"Ethernet0/2", "Ethernet0/1"}, "up->down": None},
    "192.168.100.100": {"down->up": {"Ethernet2/0", "Ethernet2/1"}, "up->down": None},
    "192.168.100.2": {"down->up": None, "up->down": {"Ethernet0/3"}},
    "192.168.100.3": {"down->up": None, "up->down": None},
}
```

The same output as a table

![solution3](https://github.com/natenka/q_and_a/blob/main/images/qa_04_3_table.png?raw=true)

## Solution

* solution_1_get_all_ports_info.py - solution only for the first step
* solution_1_pretty_printing.py - tabular output for the first step
* solution_2_physical_only_info.py - solution for the 2nd step with tabular output
* solution_3_network_changes.py - solution for the 3rd step with tabular output

Other files:

* devices.yaml - connection params
* example_data_solution_X.py - an example of the final dictionary for the X step
* example_sh_ip_int_br_output.txt - example sh ip int br output
* collected_data/free_ports_2021-07-28.json - example of saved data for step 3

