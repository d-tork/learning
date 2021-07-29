# Databricks
Cookbook for notebook interaction, DBFS, etc.

## Accessing DBFS
### Notebooks
```
%fs ls /mnt/training-data

%sh ls /tmp/testing
```
```python
dbutils.fs.ls('mnt/training-data')
```

### CLI/API
Use commands similar to Unix command line
```
dbfs cp -r test-dir dbfs:/test-dir
dbfs cp test.txt dbfs:/test.txt
```
----

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
$ databricks clusters get --cluster-name cli-demo
```

## Exporting a notebook via CLI
Say you've just edited a notebook, and want to update the .dbc file
```
$ databricks workspace export -o /cli-demo/weather-wheel weather-wheel.py

# -o for overwrite
# /cli-demo/weather-wheel is the notebook in the workspace
# weather-wheel.py is the file you are writing to
```

## Working with clusters
```
$ databricks clusters list
$ databricks clusters start --cluster-id 1112-123456-mains123
$ databricks jobs list
$ databricks jobs get --job-id 2  # returns a JSON describing the job
```

Jobs can be defined via JSON, pointing to a notebook in the workspace, 
specifying parameters, timeout, the cluster id, etc.

```
$ databricks jobs run-now --job-id 2
{
  "run_id": 3,
  "number_in_job": 1
}
$ databricks runs get-output --run-id 3
$ databricks clusters delete --cluster-id 1112-123456-mains123  # terminates
```
