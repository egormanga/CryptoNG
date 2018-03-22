# CryptoNG
Безопасное хранение данных в `PNG`

Secure data storage in `PNG`

(Crypto Network Graphics)

# Зависимости / Requirements
* Crypto >= 2.6.1
* PIL >= 3.3.1

# Использование / Usage
`CryptoNG` можно использовать и как модуль, работая с любыми `bytes-like` объектами, и через интерфейс командной строки.

While you can use `CryptoNG` as a module, encrypting any `bytes-like` objects, there is a command-line interface.

Синтаксис / Syntax: `./CryptoNG.py <encrypt | decrypt> <file> <key>`

| Режим     | Описание                                         |
| --------- | ------------------------------------------------ |
| `encrypt` | Читать `stdin` до `<EOF>`, записывать в `PNG`.   |
| `decrypt` | Читать из `PNG`, выводить в `stdout`.            |

| Mode      | Description                                      |
| --------- | ----------------------------------------------   |
| `encrypt` | Read from `stdin` until `<EOF>`, write to `PNG`. |
| `decrypt` | Read from `PNG`, print to `stdout`.              |

Вся информация выводится в `stderr`, так что её можно легко перенаправить в `/dev/null`:

All info is printed to `stderr`, so it can be easily removed by redirecting to `/dev/null`:

`./CryptoNG.py <encrypt | decrypt> <file> <key> 2> /dev/null`

При перенаправлении в файл через `>` записываться будет только текст из `stdout`.

When redirected to a file using `>`, only text from `stdout` will be written.

# P.S.
Остальные беспотерьные форматы тоже должны работать, но я рекомендую `PNG` как самый распространённый.

Other loseless formats should also work, but I recommend `PNG` as most popular.
