import importlib
import datetime
import argparse
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
    files = [name for name in os.listdir(directory) if os.path.isfile(name) and "job_" == name[:4]]
    for file_name in files:
        file_name = file_name[:-3] # Strip .py suffix, because we are importing modules
        importlib.import_module(file_name)
    directories = [name for name in os.listdir(directory) if os.path.isdir(name) and "." != name[0] and "__" != name[:2]]
    for directory_name in directories:
        import_files_from_directory(directory_name)
import_files_from_directory(".")

if args.action == "list":
    jobs = sisyphus.get_jobs()
    if args.option_show_times is True:
        # Find the longest job name in order to pad columns properly
        column_width = max(len(job.name) for job in jobs) + 2
        print("".join(["Job".ljust(column_width), "Next run".ljust(column_width)]))
        for job in jobs:
            print("".join([job.name.ljust(column_width), str(job.next_run).ljust(column_width)]))
    else:
        print("Job")
        for job in jobs:
            print(job.name)
