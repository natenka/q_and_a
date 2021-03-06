## [English translation](https://github.com/natenka/q_and_a/blob/main/code/03_filter_json_dict_by_key/README_ENG.md)

## Фильтрация JSON по ключу

Задача отфильтровать данные из JSON файла по указанному ключу. Технически речь
об отборе данных из словаря/списка, так как после чтения данных в Python это уже будет
Python list/dict.
JSON упоминается потому что именно в этом формате часто очень большая вложенность.

Во всех этапах задачи надо написать код так, чтобы не было привязки к конкретному файлу JSON и конкретной структуре данных.

Возможно, для этой задачи есть готовое решение, но тут смысл именно в том чтобы попытаться решить это самостоятельно, без готовых модулей.

### Первый этап - отбор всех значений, которые соответствуют указанному ключу

Скрипт может работать как угодно в целом, главное отобрать нужные значения.
У меня варианты решения сделаны так, что как первый аргумент передается имя файла в формате JSON,
а вторым аргументом ключ по которому надо отфильтровать данные.

Пример данных из файла json_files/basic.json (JSON файл считан в словарь):

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

Вызов скрипта может выглядеть так:

```
$ python solution_1.py json_files/basic.json name
```

Результат в этом случае должен быть таким:
```python
$ python solution_1.py json_files/basic.json name
[
    'Python for network engineers',
    'Advanced Python for network engineers',
    'PyNEng Online Course Website',
    'Advanced PyNEng Online Course Website'
]
```

Отфильтрованные данные выводятся на stdout для удобства, но сам код должен не просто выводить данные,
а собирать их, например, в список и возвращать.

### Второй этап - добавить иерархию ключей

Часто ключи будут повторятся в совершенно разных секциях, поэтому было бы неплохо иметь возможность
указывать иерархию ключей. Например, такой вызов, с указанием только name, показывает все значения, которые соответствуют ключу name:

```python
$ python solution_2a.py json_files/basic.json name
[
    'Python for network engineers',
    'Advanced Python for network engineers',
    'PyNEng Online Course Website',
    'Advanced PyNEng Online Course Website'
]
```

А вызов с аргументами ``natenka name`` значит, что надо показывать значение ключа name только
если ключ name находится в значении ключа natenka (не важно в какой вложенности):
```python
$ python solution_2a.py json_files/basic.json natenka name
[
    'Python for network engineers',
    'Advanced Python for network engineers',
    'PyNEng Online Course Website',
    'Advanced PyNEng Online Course Website'
]
```

Пример вызова для другого файла:

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

### Третий этап - указывать ключ как регулярное выражение

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

## Решение

Во всех вариантах решения используется [рекурсия](https://runestone.academy/runestone/books/published/pythonds/Recursion/toctree.html) ([перевод](http://aliev.me/runestone/Recursion/Objectives.html)).

* solution_1.py - вариант решения только для первого этапа
* solution_2a.py - вариант решения для 1 и 2 этапа
* solution_2b_generators.py - вариант решения аналогичен solution_2a.py, но с генераторами
* solution_3_regex_key.py - вариант решения для 3го этапа: с указанием ключа в виде регулярного
  выражения. Результат выводится вместе с ключом, так как не всегда понятно какой именно ключ совпал
* json_files - каталог с примерами файлов в формате JSON

