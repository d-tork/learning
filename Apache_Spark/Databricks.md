# Databricks CLI
```
$ pip3 install databricks-cli
```

## Importing a notebook
```
$ git clone https://github.com/databricks-academy/cli-demo
$ cd cli-demo
$ databricks workspace import -l PYTHON -f DBC notebooks.dbc /cli-demo
```
Now in your workspace, you have a folder `cli-demo` with all the notebooks 
contained in notebooks.dbc.

When you package as .dbc, you save the code _as well as_ the outputs.

## Install a Python wheel
```
$ cd wheel
$ ls
__init__.py						weather
setup.py						weather-1.0.0-py3-none-any.whl
$ databricks fs cp weather-1.0.0-py3-none-any.whl dbfs:/tmp/
```

Then in the workspace notebook:
```
dbutils.fs.s('/tmp')
```
to see that it's there. Install it on the cluster:
```
$ databricks libraries install --cluster-id 1112-123456-mains123 \
--whl dbfs:/tmp/weather-1.0.0-py3-none-any.whl
```
get cluster id from your notebook url or the command line:
```
databricks clusters get --cluster-name cli-demo
```
