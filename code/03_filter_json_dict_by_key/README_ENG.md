## Filter JSON by Key

The task is to filter data from a JSON file by the specified key. Technically,
we are talking about selecting data from a dictionary/list, since after reading
JSON data in Python, it will already be Python list/dict. JSON is mentioned
because this format is often very nested.

> Perhaps there is a ready-made solution for this task, but the point here is to try to solve it on your own, without ready-made modules.

### The first step is to select all values that match the specified key

The code can work as you like in general, the main thing is to select the necessary
values. My solutions are made in such a way that the name of the file in JSON format
is passed as the first argument, and the key by which the data must be filtered as the second argument.


Sample data from json_files/basic.json file (JSON file read into dictionary):

```python
{'users': {'natenka': {'projects': {'advpyneng': {'name': 'Advanced Python for network engineers',
                                                  'url': 'https://advpyneng.readthedocs.io/ru/latest/'},
                                    'pyneng': {'name': 'Python for network engineers',
                                               'url': 'https://natenka.github.io/pyneng/'}},
                       'twitter': 'https://twitter.com/natenka_says'},
           'pyneng': {'projects': {'advpyneng.github.io': {'name': 'Advanced PyNEng Online Course Website',
                                                           'url': 'https://advpyneng.github.io/'},
                                   'pyneng.github.io': {'name': 'PyNEng Online Course Website',
                                                        'url': 'https://pyneng.github.io/'}},
                      'twitter': None}}}
```

The script call might look like this:

```
$ python solution_1.py json_files/basic.json name
```

The result in this case should be like this:

```
$ python solution_1.py json_files/basic.json name
[
    'Python for network engineers',
    'Advanced Python for network engineers',
    'PyNEng Online Course Website',
    'Advanced PyNEng Online Course Website'
]
```

The filtered data is printed to stdout for convenience, but the code itself
should not just print the data, but collect it, for example, into a list and return it.

### The second step is to add a hierarchy of keys

Often, keys will be repeated in completely different sections,
so it would be userful to be able to specify a key hierarchy. For example, such a call,
specifying only name, shows all values that match the key name:

```
$ python solution_2a.py json_files/basic.json name
[
    'Python for network engineers',
    'Advanced Python for network engineers',
    'PyNEng Online Course Website',
    'Advanced PyNEng Online Course Website'
]
```

A call with natenka name arguments means that you need to show the value
of the name key only if the name key is in the value of the natenka key (no matter how nested it is):

```
$ python solution_2a.py json_files/basic.json natenka name
['Python for network engineers', 'Advanced Python for network engineers']
```

An example of a call for another file:

```python
$ python solution_2a.py json_files/cfg.json name
[
    'ae1.185',
    'v185',
    'ae47.128',
    'v128',
    'ae1.139',
    'v139',
    'ae1.140',
    'v140',
    'User1',
    'User2',
    'User3',
    'ge-0/0/0',
    '192.168.1.1/29',
    11,
    '10.1.1.1/29',
    'ge-0/0/1',
    '192.168.199.1/30'
]

$ python solution_2a.py json_files/cfg.json user
[
    [
        {
            'authentication': {'encrypted-password': 'password'},
            'class': 'super-user',
            'name': 'User1',
            'uid': 1000
        },
        {
            'authentication': {'encrypted-password': 'password'},
            'class': 'super-user',
            'name': 'User2',
            'uid': 2001
        },
        {
            'authentication': {'encrypted-password': 'password'},
            'class': 'super-user',
            'name': 'User3',
            'uid': 2002
        }
    ]
]

$ python solution_2a.py json_files/cfg.json user name
['User1', 'User2', 'User3']
```

### The third step is to specify the key as a regular expression

```python
$ python solution_3_regex_key.py json_files/cfg.json vlan.*
[{'vlan-id': 185}, {'vlan-id': 128}, {'vlan-id': 139}, {'vlan-id': 140}, {'vlan-id': 11}]

$ python solution_3_regex_key.py json_files/cfg.json inter.*
[
    {'interface': [{'name': 'ae1.185'}]},
    {'interface': [{'name': 'ae47.128'}]},
    {'interface': [{'name': 'ae1.139'}]},
    {'interface': [{'name': 'ae1.140'}]},
    {'interface-name': 'ge-0/0/1.1'},
    {'interface-name': 'ge-0/0/1.4'},
    {
        'interfaces': {
            'interface': [
                {
                    'description': 'To CORE gi-1/0/5',
                    'encapsulation': 'flexible-ethernet-services',
                    'flexible-vlan-tagging': [None],
                    'hierarchical-scheduler': [None],
                    'name': 'ge-0/0/0',
                    'unit': [
                        {
                            'description': 'L3-management',
                            'family': {'inet': {'address': [{'name': '192.168.1.1/29'}]}},
                            'name': 11,
                            'vlan-id': 11
                        },
                        {
                            'description': 'Server',
                            'family': {'inet': {'address': [{'name': '10.1.1.1/29'}]}}
                        }
                    ]
                },
                {
                    'description': 'ISP1',
                    'name': 'ge-0/0/1',
                    'unit': [{'family': {'inet': {'address': [{'name': '192.168.199.1/30'}]}}}]
                }
            ]
        }
    }
]

```

## Solution

All solutions use [recursion](https://runestone.academy/runestone/books/published/pythonds/Recursion/toctree.html).

* solution_1.py - solution only for the first step
* solution_2a.py - solution for steps 1 and 2
* solution_2b_generators.py - solution is similar to solution_2a.py, but with generators
* solution_3_regex_key.py - solution for the 3rd step: specifying the key
  in the form of a regular expression. The result is displayed along with the key,
  since it is not always clear which key matched.
* json_files - directory with sample JSON files

  * basic.json
  * cfg.json
  * cmd_output.json
  * repos.json
