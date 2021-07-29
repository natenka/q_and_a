## [English translation]()

## Фильтрация JSON по ключу

Задача отфильтровать данные из JSON файла по указанному ключу. Технически речь
об отборе данных из словаря/списка, так как после чтения данных в Python это уже будет
Python list/dict.
JSON упоминается потому что именно в этом формате часто очень большая вложенность.

### Первый этап - отбор всех значений, которые соответствуют указанному ключу

Скрипт может работать как угодно в целом, главное отобрать нужные значения.
У меня варианты решения сделаны так, что как первый аргумент передается имя файла в формате JSON,
а вторым аргументом ключ по которому надо отфильтровать данные.

Например данных из файла json_files/basic.json (JSON файл считан в словарь):

```python
{'users': {'natenka': {'projects': {'advpyneng': {'name': 'Advanced Python для сетевых инженеров',
                                                  'url': 'https://advpyneng.readthedocs.io/ru/latest/'},
                                    'pyneng': {'name': 'Python для сетевых инженеров',
                                               'url': 'https://natenka.github.io/pyneng/'}},
                       'twitter': 'https://twitter.com/natenka_says'},
           'pyneng': {'projects': {'advpyneng.github.io': {'name': 'Сайт курса Advanced PyNEng Online',
                                                           'url': 'https://advpyneng.github.io/'},
                                   'pyneng.github.io': {'name': 'Сайт курса PyNEng Online',
                                                        'url': 'https://pyneng.github.io/'}},
                      'twitter': None}}}
```

Вызов скрипта может выглядеть так:

```
$ python solution_0.py json_files/basic.json name
```

Результат в этом случае должен быть таким:
```
$ python solution_0.py json_files/basic.json name
['Python для сетевых инженеров', 'Advanced Python для сетевых инженеров', 'Сайт курса PyNEng Online', 'Сайт курса Advanced PyNEng Online']
```

Отфильтрованные данные выводятся на stdout для удобства, но сам код должен не просто выводить данные,
а собирать их, например, в список и возвращать.

### Второй этап - добавить иерархию ключей

Часто ключи будут повторятся в совершенно разных секциях, поэтому было бы неплохо иметь возможность
указывать иерархию ключей. Например, такой вызов, с указанием только name, показывает все значения, которые соответствуют ключу name:

```
$ python solution_0.py json_files/basic.json name
['Python для сетевых инженеров', 'Advanced Python для сетевых инженеров', 'Сайт курса PyNEng Online', 'Сайт курса Advanced PyNEng Online']
```

А вызов с аргументами ``natenka name`` значит, что надо показывать значение ключа name только
если ключ name находится в значении ключа natenka (не важно в какой вложенности):
```
$ python solution_1.py json_files/basic.json natenka name
['Python для сетевых инженеров', 'Advanced Python для сетевых инженеров']
```

Пример вызова для другого файла:

```
$ python solution_1.py json_files/cfg.json name
['ae1.185', 'v185', 'ae47.128', 'v128', 'ae1.139', 'v139', 'ae1.140', 'v140', 'User1', 'User2', 'User3', 'ge-0/0/0', '192.168.1.1/29', 11, '10.1.1.1/29', 'ge-0/0/1', '192.168.199.1/30']

$ python solution_1.py json_files/cfg.json user
[
    [
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User1', 'uid': 1000},
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User2', 'uid': 2001},
        {'authentication': {'encrypted-password': 'password'}, 'class': 'super-user', 'name': 'User3', 'uid': 2002}
    ]
]

$ python solution_1.py json_files/cfg.json user name
['User1', 'User2', 'User3']
```

### Третий этап - указывать ключ как регулярное выражение

## Решение

Во всех вариантах решения используется рекурсия.

* solution_0.py - вариант решения только для первого этапа
* solution_1.py - вариант решения для 1 и 2 этапа
* solution_2_generators.py - вариант решения аналогичен 2му, но с генераторами
* solution_3_regex_key.py - вариант решения с указанием ключа в виде регулярного
  выражения. Результат выводится вместе с ключом, так как не всегда понятно какой именно ключ совпал
* json_files - каталог с примерами файлов в формате JSON

  * cfg.json
  * cmd_output.json
  * repos.json

Полезные ссылки:

* [recursion](https://runestone.academy/runestone/books/published/pythonds/Recursion/toctree.html), [перевод](http://aliev.me/runestone/Recursion/Objectives.html)
