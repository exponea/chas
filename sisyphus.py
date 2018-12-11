import importlib
import datetime
import argparse
import logger
import time
import os
from main import sisyphus


# Parse command line command
parser = argparse.ArgumentParser(description="Sisyphus system for running statefull or stateless cron jobs.")
parser.add_argument("action", choices=["list", "start"])
parser.add_argument("--show-times", action="store_true", dest="option_show_times")
args = parser.parse_args()

# Find all jobs by crawling through directory
def import_files_from_directory(directory):
    files = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and "job_" == name[:4] and ".py" == name[-3:]]
    for file_name in files:
        file_name = file_name[:-3] # Strip .py suffix, because we are importing modules
        if directory == ".":
            file_name = file_name[2:] # Strip ./ prefix
        else:
            file_name = file_name.replace("/", ".") # Convert path to Python module
        importlib.import_module(file_name)
    directories = [name for name in os.listdir(directory) if os.path.isdir(name) and "." != name[0] and "__" != name[:2]]
    for directory_name in directories:
        import_files_from_directory(directory_name)
import_files_from_directory(".")

if args.action == "list":
    jobs = sisyphus.get_jobs()
    if args.option_show_times is True:
        # Find the longest job name in order to pad columns properly
        column_width_first = max(len(job.name) for job in jobs) + 2
        column_width_second = max(len(str(job.next_run)) for job in jobs) + 2
        print("".join(["Job".ljust(column_width_first), "Next run".ljust(column_width_second), "Last run".ljust(column_width_second)]))
        for job in jobs:
            print("".join([job.name.ljust(column_width_first), str(job.next_run).ljust(column_width_second), str(job.last_run).ljust(column_width_second)]))
    else:
        print("Job")
        for job in jobs:
            print(job.name)
elif args.action == "start":
    while True:
        time.sleep(3)
        sisyphus.run_jobs()
