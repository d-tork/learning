# Shell Data Science

## Jeroen Janssens - _Data Science at the Command Line_
https://datascienceatthecommandline.com/

Left off at ch. 5; resources on dolores at ~/dsatcl2e

### Ch. 6 - Project Management with Make
A Makefile issues instructions for setting up the project (downloading data, creating folders and
files). You should always begin every project with one.

Two things in a makefile: targets and rules. When you run the Makefile you can specify a target,
or it will run the first one by default.
```bash
make publish
```
Declare the targets that should run each time no matter what with `.PHONY` at the top of the
Makefile.
```Makefile
.PHONY: clean publish docker-run
```

### Ch. 7 - Exploring Data

#### List columns in a CSV and their datatypes
```bash
$ < venture.csv head -n 1 | tr , '\n'
```
where you're taking the first row (headers) and `tr` translates the comma-separator into newlines.

If it's available, you can do the same thing with `csvcut`
```bash
$ csvcut -n venture.csv
```

To get datatypes, use `csvsql`:
```bash
csvsql venture.csv
```

### Ch. 9 - Modeling

#### Toolset
| tool     | use                      |
|----------|--------------------------|
| `tapkee` | dimensionality reduction |
| `vw`     | regression               |
| `skll`   | classification           |


