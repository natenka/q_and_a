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

![qa01]()
