## Надо разбить настройку интерфейса на две части

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

Все параметры берутся из исходной конфигурации, кроме MAC-адреса, который
вычисляется из IP-адреса. Часть `00:ff:` всегда одинакова, а остальные значения
это IP-адрес в шестнадцатеричном формате.

Картинка с обозначением цветом какая часть куда переходит:

![qa01](https://github.com/natenka/q_and_a/blob/main/code/01_convert_interface_cfg/qa_01.png?raw=true)

## Следующий шаг - конвертировать настройки нескольких интерфейсов

В файле cfg_data.txt находится настройка нескольких интерфейсов, которые нужно конвертировать
таким же образом как показано выше.


## Дополнительная особенность - строка mtu

В некоторых исходных интерфейсах есть строка с настройкой mtu

```
set interfaces ae0 unit 1001 description "EXAMPLE_1001"
set interfaces ae0 unit 1001 vlan-tags outer 18
set interfaces ae0 unit 1001 vlan-tags inner 10
set interfaces ae0 unit 1001 family inet mtu 1500
set interfaces ae0 unit 1001 family inet policer input P-IN-L2
set interfaces ae0 unit 1001 family inet policer output P-OUT-L2
set interfaces ae0 unit 1001 family inet address 60.1.1.1/30
```

Она может быть, а может не быть в интерфейсе.
Если строка есть, ее надо добавить в конвертированный вариант (в начало или в конец секции irb):

```
set interfaces irb unit 1001 family inet mtu 1500
set interfaces irb unit 1001 description "EXAMPLE_1001"
set interfaces irb unit 1001 family inet address 60.1.1.1/30
set interfaces irb unit 1001 mac 00:ff:3c:01:01:01
```

## Решение

В варианте решения задачи показан код, который обрабатывает несколько интерфейсов из файла и с учетом строки mtu.

Файлы:

* input_cfg_data.txt - это исходная конфигурация интерфейсов, которые надо конвертировать.
* output_cfg_results.txt - что надо получить в итоге
* solution_1.py - вариант решения с составлением итогового шаблона с помощью форматирования строк
* solution_2_jinja_template.py - вариант решения с шаблоном Jinja2
* interface_template.j2 - шаблон Jinja2 для второго варианта решения


