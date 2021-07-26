# Q & A

Мне часто задают вопросы как решить ту или иную задачку и я решила
выкладывать эти вопросы и решения тут, на случай если кому-то это тоже пригодится.

При желании, описание вопроса можно использовать как задачку и решить ее самостоятельно,
а потом посмотреть вариант решения.

Варианты решения не являются каким-то идеальным варинтом, это просто тот вариант решения,
который написала я.

| QA | Description                                       | Topics/modules used in solution |
| ---|-------------------------------------------------- | ------------------------------- |
| 1  | [Split the interface configuration into two parts](https://github.com/natenka/q_and_a/tree/main/code/01_convert_interface_cfg) | regex, format, Jinja2           |
| 2  | [Network Topology Discovery Using CDP/LLDP](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map) | scrapli, regex, queue, Rich     |


## [Задача 1](https://github.com/natenka/q_and_a/tree/main/code/01_convert_interface_cfg)

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

## [Задача 2](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map)

> [English translation](https://github.com/natenka/q_and_a/blob/main/code/02_explore_network_map/README_ENG.md)

Надо обнаружить топологию сети через вывод CDP (считаем что CDP есть на всех устройствах).
Для старта должен быть известен IP-адрес одного устройства и параметры подключения
по SSH ко всем устройствам в сети.

Надо подключиться к первому устройству, дать команду ``sh cdp neighbors detail``, получить
всех соседей и их IP-адреса и подключаться к каждому соседу.
На каждом соседе опять дать команду ``sh cdp neighbors detail`` и получить соседей этого устройства.
Так надо пройтись по всей сети и собрать информацию об устройствах и топологии.


[Подробнее](https://github.com/natenka/q_and_a/tree/main/code/02_explore_network_map)
