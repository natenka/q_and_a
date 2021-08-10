# Q & A

Мне часто задают вопросы как решить ту или иную задачку и я решила
выкладывать эти вопросы и решения тут, на случай если кому-то это тоже пригодится.

При желании, описание вопроса можно использовать как задачку и решить ее самостоятельно,
а потом посмотреть вариант решения.

Варианты решения не являются каким-то идеальным варинтом, это просто тот вариант решения,
который написала я.

| QA | Description                                       | Topics/modules used in solutions |
|:--:|-------------------------------------------------- | -------------------------------- |
| 1  | [Split the interface configuration into two parts](https://github.com/natenka/q_and_a/tree/main/code/01_convert_interface_cfg) | regex, format, jinja2           |
| 2  | [Network Topology Discovery Using CDP/LLDP](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map) | scrapli, regex, queue, click, rich     |
| 3  | [Filter JSON data by key](https://github.com/natenka/q_and_a/tree/main/code/03_filter_json_dict_by_key) | recursion, generator, regex, click |
| 4  | [Collect Port Status Information](https://github.com/natenka/q_and_a/tree/main/code/04_collect_ports_status) | scrapli, concurrent.futures, regex, rich |


## [Q&A 1](https://github.com/natenka/q_and_a/tree/main/code/01_convert_interface_cfg)

> [English translation](https://github.com/natenka/q_and_a/blob/main/code/01_convert_interface_cfg/README_ENG.md)

Надо разбить настройку интерфейса на две части.
Есть конфигурация интерфейса такого вида:

```
set interfaces ae0 unit 1001 description "EXAMPLE_1001"
set interfaces ae0 unit 1001 vlan-tags outer 18
set interfaces ae0 unit 1001 vlan-tags inner 10
set interfaces ae0 unit 1001 family inet policer input P-IN-L2
set interfaces ae0 unit 1001 family inet policer output P-OUT-L2
set interfaces ae0 unit 1001 family inet address 60.1.1.1/30
```

Эту конфигурацию надо разбить на две части:

```
set interfaces ae9 unit 1001 description "EXAMPLE_1001"
set interfaces ae9 unit 1001 encapsulation vlan-bridge
set interfaces ae9 unit 1001 vlan-tags outer 18
set interfaces ae9 unit 1001 vlan-tags inner 10
set interfaces ae9 unit 1001 family bridge policer input P-IN-L2
set interfaces ae9 unit 1001 family bridge policer output P-OUT-L2
```

и
```
set interfaces irb unit 1001 description "EXAMPLE_1001"
set interfaces irb unit 1001 family inet address 60.1.1.1/30
set interfaces irb unit 1001 mac 00:ff:3c:01:01:01
```

[Подробнее](https://github.com/natenka/q_and_a/tree/main/code/01_convert_interface_cfg)

## [Q&A 2](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map)

> [English translation](https://github.com/natenka/q_and_a/blob/main/code/02_explore_network_map/README_ENG.md)

Надо обнаружить топологию сети через вывод CDP (считаем что CDP есть на всех устройствах).
Для старта должен быть известен IP-адрес одного устройства и параметры подключения
по SSH ко всем устройствам в сети.

Надо подключиться к первому устройству, дать команду ``sh cdp neighbors detail``, получить
всех соседей и их IP-адреса и подключаться к каждому соседу.
На каждом соседе опять дать команду ``sh cdp neighbors detail`` и получить соседей этого устройства.
Так надо пройтись по всей сети и собрать информацию об устройствах и топологии.


[Подробнее](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map)


## [Q&A 3](https://github.com/natenka/q_and_a/tree/main/code/03_filter_json_dict_by_key)

> [English translation](https://github.com/natenka/q_and_a/blob/main/code/03_filter_json_dict_by_key/README_ENG.md)

Задача отфильтровать данные из JSON файла по указанному ключу. Технически речь
об отборе данных из словаря/списка, так как после чтения данных в Python это уже будет
Python list/dict.
JSON упоминается потому что именно в этом формате часто очень большая вложенность.

```
$ python solution_2a.py json_files/cfg.json name
['ae1.185', 'v185', 'ae47.128', 'v128', 'ae1.139', 'v139', 'ae1.140', 'v140', 'User1', 'User2', 'User3', 'ge-0/0/0', '192.168.1.1/29', 11, '10.1.1.1/29', 'ge-0/0/1', '192.168.199.1/30']

$ python solution_2a.py json_files/cfg.json user
[
    [
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User1', 'uid': 1000},
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User2', 'uid': 2001},
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User3', 'uid': 2002}
    ]
]

$ python solution_2a.py json_files/cfg.json user name
['User1', 'User2', 'User3']
```


## [Q&A 4](https://github.com/natenka/q_and_a/tree/main/code/04_collect_ports_status)

> [English translation](https://github.com/natenka/q_and_a/blob/main/code/04_collect_ports_status/README_ENG.md)

Задача собрать информацию о статусе портов на оборудовании (up/down/admin down для Cisco IOS).
На первом этапе собирается информация о всех портах (Loopback/физические/Tunnel/...) и их статусе.
На втором этапе из собраной информации надо отобрать только физические порты. И на третьем сохранять
информацию о статусе портов и добавить возможность сравнивать изменения
в статусе портов (текущий статус с последним записанным).

![solution_1_stats](https://github.com/natenka/q_and_a/blob/main/images/qa_04_1_table_stats.png?raw=true)

