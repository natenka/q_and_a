## [English translation]()

## Сбор информации о статусе портов, изменения в статусе

Задача собрать информацию о статусе портов на оборудовании (up/down/admin down для Cisco IOS).
На первом этапе собирается информация о всех портах (Loopback/физические/Tunnel/...) и их статусе.
На втором этапе из собраной информации надо отобрать только физические порты. И на третьем сохранять
информацию о статусе портов в определенный день в файлы и добавить возможность сравнивать изменения
в статусе портов (текущий статус с последним записанным).


### Первый этап - собрать информацию о статусе портов на оборудовании

Задача собрать информацию о статусе портов на оборудовании (up/down/admin down для Cisco IOS).
Собирается информация о всех портах (Loopback/физические/Tunnel/...) и их статусе.
Пример итогового словаря (полный вывод в example_data_solution_1.py):

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

С информацией в виде словаря удобно работать дальше, но ее не очень удобно воспринимать визуально, поэтому
надо также вывести информацию о статусе портов в табличном виде, например (может быть просто вывод столбцами):

![solution_1](https://github.com/natenka/q_and_a/blob/main/images/qa_04_1_table_all_info.png?raw=true)

Дополнительно можно добавить сводку по количеству портов, без перечисления конкретных портов, например:

![solution_1_stats](https://github.com/natenka/q_and_a/blob/main/images/qa_04_1_table_stats_info_color.png?raw=true)

### Второй этап - отфильтровать из собраной информации только физические порты

На втором этапе надо отфильтровать из собраной информации только физические порты и упростить статусы портов.
Теперь не надо делать различие между статусами ``administratively down`` и ``down``, оба статуса должны быть записаны как down.

Если на предыдущем этапе словарь со всеми портами был таким:

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

После фильтрации должен получиться такой словарь (полный словарь в файле example_data_solution_2.py):

```python
{
    "down": ["Ethernet0/2", "Ethernet0/3"],
    "up": ["Ethernet0/0", "Ethernet0/1"],
}
```

Так же как и с первым этапом, надо вывести информацию по портам в виде таблицы:

![solution_2](https://github.com/natenka/q_and_a/blob/main/images/qa_04_2_table_all_info.png?raw=true)

И добавить сводку по количеству портов, без перечисления конкретных портов:

![solution_2_stats](https://github.com/natenka/q_and_a/blob/main/images/qa_04_2_table_stats_info.png?raw=true)

### Третий этап - отслеживание изменений в статусе портов

После второго этапа есть информация о статусе физических портов. Теперь надо записывать эту
информацию (словарь) в формате JSON в файлы с указанием даты получения информации
(пример в collected_data/free_ports_2021-07-28.json).

Теперь представляем, что прошло несколько дней и надо сравнить текущий статус портов
с последней записью и показать какие порты перешли из статуса up в down и наоборот.

Например есть такие данные (old_data данные которые были ранее записаны в файл, new_data данные считанные из сети):
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

Итоговый словарь для таких данных должен быть таким:
```python
diff_dict = {
    "192.168.100.1": {"down->up": {"Ethernet0/2", "Ethernet0/1"}, "up->down": None},
    "192.168.100.100": {"down->up": {"Ethernet2/0", "Ethernet2/1"}, "up->down": None},
    "192.168.100.2": {"down->up": None, "up->down": {"Ethernet0/3"}},
    "192.168.100.3": {"down->up": None, "up->down": None},
}
```

И тот же вывод таблицей

![solution3](https://github.com/natenka/q_and_a/blob/main/images/qa_04_3_table.png?raw=true)

## Решение

* solution_1_get_all_ports_info.py - вариант решения только для первого этапа
* solution_1_pretty_printing.py - вывод таблиц по первому этапу
* solution_2_physical_only_info.py - вариант решения только для 2го этапа с выводом таблиц
* solution_3_network_changes.py - вариант решения только для 3го этапа с выводом таблиц

Вспомогательные файлы:

* devices.yaml - параметры подключения к оборудованию
* example_data_solution_1.py - пример итогового словаря для 1го этапа
* example_data_solution_2.py - пример итогового словаря для 2го этапа
* example_data_solution_3.py - пример итогового словаря для 3го этапа
* example_sh_ip_int_br_output.txt - пример вывода sh ip int br
* collected_data/free_ports_2021-07-28.json - пример сохраненных данных для 3го этапа

