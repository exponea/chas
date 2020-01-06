## Chas

### Installation
Install library through pip 
```bash
pip install chas
```
Add decorator to function in your script called `job_jobname.py` (note: it must start with prefix `job_`) that you want to run as cron job. For example:
```python
from chas import chas

@chas.job("08:00")
def print_hello_world():
    print("Hello, World!")
```
Finally, you can start up a server by running. This starts the cron scheduler, which will execute the function at given times, and also you can view and manage jobs on `localhost:5000`.
```bash
chas start --http-server
```

### Command line
Chas is convenient even from running jobs from your command line. You can do
```bash
chas list
```
Which prints out all the registered jobs
```
Job                Next run             Last run             Last status
print_hello_world  22-12-2018 08:00:00  N/A                  N/A 
```
You can run any of these jobs by typing
```bash
chas run print_hello_world
```

### Decorators
As already mentioned, `@chas.job(time)` registers a job at a particular time. There another decorator `@chas.setup()` which simply executes the script inside during the import time. This should be used for setting up environment variables. For example`

```python
import os
from chas import chas

@chas.setup()
def setup_environment():
    os.environ["foo"] = "bar"

@chas.job("09:00")
def print_env_var():
    print(os.environ["foo"])
```
On run would print `bar`.


### Packages
In case you structure your directory as a Python package, you will need to export all scripts with `@chas.job` from the package. Then, you will run all shell commands as above, but with adding parameter `--package folder_name` where `folder_name` specifies the entry point to your package.
For example, if you structure your package in the following way:
```
.
|-- src
|   -- __init__.py
|   -- script_one.py
|   -- script_two.py 
|-- LICENSE
|-- README.md
```
Then you can run `chas list --package src`.


### Prometheus
When starting the server with option `--http-server`, `chas` automatically opens up Prometheus metrics endpoint on `/metrics`. This allows you to easily monitor your chas script with Prometheus and complementary tools like Grafana, Alertmanager etc.
The two metrics gathered are Counter-type objects named `job_runs_total` and `job_runs_status_total`, first denoting the number of times a job was run and the second also counting their statuses, either `failed` or `succeeded`.

## Troubleshooting
What to do in case of ModuleNotFound error?
- This can happen due to incorrect PYTHONPATH environment variable. Make sure current working directory is in there. You can check it by `echo $PYTHONPATH`. Otherwise to append current working directory, run `export PYTHONPATH="${PYTHONPATH}:${PWD}"`.
