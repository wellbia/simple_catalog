# Simple Catalog

Register information with the catalog server to facilitate the integrity checks of built files in the build system.

## Installation

install the latest stable version using `pip`

```shell
pip install simple-catalog
```

## Usage

```python
import simple_catalog

client = simple_catalog.Client(
    host="localhost",
    user="user",
    password="passwd",
    database="db",
    salt="abcd1234",
    product="product",
    revision="1234",
    hash="abcdefg",
)

client.add(file)

if client.check(file) is not None:
    removed_entry = client.delete(file)
    for entry in removed_entry:
        print(entry)

client.inspect(file)
```

## Use console scripts

### add
```shell
simple-catalog-cli --add --host localhost --user user --password passwd --database catalog --file test.exe --salt abcd1234 --product productname --revision 1234 --hash abcdefg
```

### delete
```shell
simple-catalog-cli --delete --host localhost --user user --password passwd --database catalog --file test.exe --salt abcd1234 --product productname --revision 1234 --hash abcdefg
```

### check
```shell
simple-catalog-cli --check --host localhost --user user --password passwd --database catalog --file test.exe
```

### inspect
Check if files included in the compressed file exist in the catalog.  
This feature supports ZIP, 7z, RAR file.
```shell
simple-catalog-cli --inspect --host localhost --user user --password passwd --database catalog --file test.zip --file_password file_password --output_format json
```

## Dependencies

* [pymysql](https://github.com/PyMySQL/PyMySQL)
* [py7zr](https://github.com/miurahr/py7zr)
* [rarfile](https://github.com/markokr/rarfile)