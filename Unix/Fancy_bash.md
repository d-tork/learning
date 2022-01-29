# Fancy Bash
Tools that may not be available out of the box

## `bat`
Improved version of `cat`, detects the language based on the `#!` line and does syntax highlighting.

## CSV tools
Install these with `apt install csvkit`.

```bash
$ < tmnt-with-header.csv csvsql --query "select * from stdin where nickname = 'Leo'" | csvlook
| name     | nickname | mask_color | weapon        |
| -------- | -------- | ---------- | ------------- |
| Leonardo | Leo      | blue       | two ninjakens |
```

### `csvlook`
Pretty-prints a csv

### `in2csv`
Converts Excel to CSV.

### `csvsql`
Execute SQL commands against a CSV file

The filename without extension is used as the default table name, but if the filename has illegal
characters like `-` then specify the name manually:
```bash
csvsql --tables tmnt --query "select * from tmnt" tmnt-with-header.csv
```

If no command line arguments are passed, it generates the SQL statement that would be needed if you
were to insert this data into an actual database (useful for seeing the column datatypes)
```bash
$ csvsql datatypes.csv
CREATE TABLE datatypes (
		a DECIMAL NOT NULL,
        b DECIMAL,
        c BOOLEAN NOT NULL,
        d VARCHAR NOT NULL,
        e TIMESTAMP,
        f DATE
);
```

### `sql2csv`
Query a database and save the results to CSV.

Two things you need: 
* `--db`, the database url, of the form `dialect+driver://username:password@host:port/database`
* `--query`

But it can also work against a local `.db` file:
```bash
sql2csv --db 'sqlite:///r-datasets.db' --query 'SELECT * FROM mtcars ORDER BY mpg'
```
