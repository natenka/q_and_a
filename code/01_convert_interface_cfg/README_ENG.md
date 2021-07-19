## Split the interface configuration into two parts

Split this interface configuration into two parts:

```
set interfaces ae0 unit 1001 description "EXAMPLE_1001"
set interfaces ae0 unit 1001 vlan-tags outer 18
set interfaces ae0 unit 1001 vlan-tags inner 10
set interfaces ae0 unit 1001 family inet policer input P-IN-L2
set interfaces ae0 unit 1001 family inet policer output P-OUT-L2
set interfaces ae0 unit 1001 family inet address 60.1.1.1/30
```

part 1:

```
set interfaces ae9 unit 1001 description "EXAMPLE_1001"
set interfaces ae9 unit 1001 encapsulation vlan-bridge
set interfaces ae9 unit 1001 vlan-tags outer 18
set interfaces ae9 unit 1001 vlan-tags inner 10
set interfaces ae9 unit 1001 family bridge policer input P-IN-L2
set interfaces ae9 unit 1001 family bridge policer output P-OUT-L2
```

part 2:

```
set interfaces irb unit 1001 description "EXAMPLE_1001"
set interfaces irb unit 1001 family inet address 60.1.1.1/30
set interfaces irb unit 1001 mac 00:ff:3c:01:01:01
```

All parameters must be taken from the initial configuration, except for the MAC address,
which is calculated from the IP address. The ``00:ff:`` part is always the same,
and the rest of the values are the IP address in hexadecimal.

A picture with a color designation which part goes where:

![qa01](https://github.com/natenka/q_and_a/blob/main/code/01_convert_interface_cfg/qa_01.png?raw=true)

## The next step is to convert the settings of multiple interfaces

The cfg_data.txt file contains the configuration of several interfaces that need to be converted
in the same way as shown above.


## Additional feature - mtu string

Some interfaces have a line with the mtu setting:

```
set interfaces ae0 unit 1001 description "EXAMPLE_1001"
set interfaces ae0 unit 1001 vlan-tags outer 18
set interfaces ae0 unit 1001 vlan-tags inner 10
set interfaces ae0 unit 1001 family inet mtu 1500
set interfaces ae0 unit 1001 family inet policer input P-IN-L2
set interfaces ae0 unit 1001 family inet policer output P-OUT-L2
set interfaces ae0 unit 1001 family inet address 60.1.1.1/30
```

The mtu line may or may not be present in the configuration. If there is a line,
it must be added to the converted version (at the beginning or at the end of the irb section):

```
set interfaces irb unit 1001 family inet mtu 1500
set interfaces irb unit 1001 description "EXAMPLE_1001"
set interfaces irb unit 1001 family inet address 60.1.1.1/30
set interfaces irb unit 1001 mac 00:ff:3c:01:01:01
```

## Solution

* input_cfg_data.txt - is the initial configuration of the interfaces to be converted
* output_cfg_results.txt - what you need to get in the end
* solution_1.py - a version of the solution with the compilation of the final template using string formatting
* solution_2_jinja_template.py - solution with Jinja2 template
* interface_template.j2 - Jinja2 template for the second solution
