## Network Topology Discovery Using CDP/LLDP

We need to discover the network topology through the CDP output (we assume that
all devices have CDP).
The IP address of the starting device and the parameters for connecting via SSH to all devices on the network are known.

> CDP or LLDP can be used.


You need to connect to the first device, run ``sh cdp neighbors detail`` command,
get all neighbors and their IP addresses, and connect to each neighbor.
For each neighbor, run the ``sh cdp neighbors detail`` command again to get
the neighbors information for that device. Thus, you need to traverse
the entire network and collect information about devices and topology.


For example, if the topology looks like this and the IP address of R1 is known:

```
.====.    .=====.    .====.
| R1 |----| SW1 |----| R2 |  
'===='    '====='    '===='
             |
             |
          .====.
          | R3 |
          '===='
```

The order of work can be something like this:

1. Connect to R1 and get CDP neighbors - only SW1
2. We connect to SW1 and get three neighbors R1, R2, R3 - we connect only to R2 and R3, since we have already connected to R1

Device IP addresses in the dictionary below:

* R1 192.168.100.1
* R2 192.168.100.2
* R3 192.168.100.3
* SW1 192.168.100.100

The final topology can look anything you like, for example, it can be a dictionary like this:

```python
{'192.168.100.1': {'192.168.100.100': {'local_port': 'Ethernet0/0',
                                       'remote_port': 'Ethernet0/1'}},
 '192.168.100.100': {'192.168.100.1': {'local_port': 'Ethernet0/1',
                                       'remote_port': 'Ethernet0/0'},
                     '192.168.100.2': {'local_port': 'Ethernet0/2',
                                       'remote_port': 'Ethernet0/0'},
                     '192.168.100.3': {'local_port': 'Ethernet0/3',
                                       'remote_port': 'Ethernet0/0'}},
 '192.168.100.2': {'192.168.100.100': {'local_port': 'Ethernet0/0',
                                       'remote_port': 'Ethernet0/2'}},
 '192.168.100.3': {'192.168.100.100': {'local_port': 'Ethernet0/0',
                                       'remote_port': 'Ethernet0/3'}}}
```

I chose this format because it was convenient for me to work with it,
but the final format for describing the topology itself is not important,
the main thing is to somehow describe how the equipment is interconnected.

## Topology loops

The next step is to verify that the code works for the topology that has loops.

```
.====.    .=====.    .====.
| R1 |----| SW1 |----| R2 |  
'===='    '====='    '===='
             |         |
             |         |
          .====.       |
          | R3 |-------|
          '===='
```

## Hostname

If in the previous versions the visited neighbor was marked by the IP address,
you need to make sure that it is marked by the hostname too, since, for example,
SW1 and R2 will see R3 through different IP addresses and R3 will be considered an unvisited neighbor.

An example of the final topology with hostname:

```python
{'R1': {'SW1': {'ip': '192.168.100.100',
                'local_port': 'Ethernet0/0',
                'remote_port': 'Ethernet0/1'}},
 'R2': {'R3': {'ip': '10.100.23.3',
               'local_port': 'Ethernet0/1',
               'remote_port': 'Ethernet0/1'},
        'SW1': {'ip': '192.168.100.100',
                'local_port': 'Ethernet0/0',
                'remote_port': 'Ethernet0/2'}},
 'R3': {'R2': {'ip': '10.100.23.2',
               'local_port': 'Ethernet0/1',
               'remote_port': 'Ethernet0/1'},
        'SW1': {'ip': '192.168.100.100',
                'local_port': 'Ethernet0/0',
                'remote_port': 'Ethernet0/3'}},
 'SW1': {'R1': {'ip': '192.168.100.1',
                'local_port': 'Ethernet0/1',
                'remote_port': 'Ethernet0/0'},
         'R2': {'ip': '192.168.100.2',
                'local_port': 'Ethernet0/2',
                'remote_port': 'Ethernet0/0'},
         'R3': {'ip': '192.168.100.3',
                'local_port': 'Ethernet0/3',
                'remote_port': 'Ethernet0/0'}}}
```

## Solution

* solution_1_ip_only.py - a version of the solution taking into account only IP addresses when determining whether a device has been visited
* solution_2_ip_and_hostname.py - a version of the solution taking into account IP addresses and hostname when determining whether the device was visited
* solution_3_ip_and_hostname_rich_live.py - second option, but with topology output using Rich
