#!/usr/bin/env python3
import importlib.util
import datetime
import argparse
import time
import sys
import os
from chas.http_server import http_server, HTTPServerThread
from chas.exceptions import JobNotFoundException


# Helper to show all jobs with next run times
def print_jobs_with_times(chas, checking=True):
    jobs = chas.get_jobs()
    if len(jobs) == 0:
        print("No jobs are registered.")
        return None
    # Find the longest job name in order to pad columns properly
    column_width_first = max(len(job.name) for job in jobs) + 2
    column_width_second = max(len(str(job.next_run)) for job in jobs) + 2
    column_width_third = max(len(job.last_state.status) for job in jobs) + 2
    if checking:
        print()
        print("========== Checking jobs at {} ==========".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    print("".join(["Job".ljust(column_width_first), "Next run".ljust(column_width_second), "Last run".ljust(column_width_second), "Last status".ljust(column_width_third)]))
    for job in jobs:
        next_run = job.next_run if isinstance(job.next_run, str) else job.next_run.strftime("%d-%m-%Y %H:%M:%S")
        last_run = job.last_run if isinstance(job.last_run, str) else job.last_run.strftime("%d-%m-%Y %H:%M:%S")
        print("".join([job.name.ljust(column_width_first), next_run.ljust(column_width_second), last_run.ljust(column_width_second), job.last_state.status.ljust(column_width_third)]))
    if checking:
        print()

# Find all jobs by crawling through directory
def import_files_from_directory(directory=os.getcwd(), chas=None, package=None):
    # Import jobs from inside a package by importing to top level module
    if package is not None:
        package = package[0] # argparse module returns a list of arguments
        file_path = os.path.join(directory, package, "__init__.py")
        spec = importlib.util.spec_from_file_location(package, file_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return foo.chas
    # Import jobs which are sparsed across current working directory
    files = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and "job_" == name[:4] and ".py" == name[-3:]]
    for file_path in files:
        module_name = os.path.basename(file_path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        if chas is None and hasattr(foo, "chas"):
            chas = foo.chas
    directories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) and "." != name[0] and "__" != name[:2] and name not in ["bin", "include", "lib"]]
    for directory_name in directories:
        import_files_from_directory(os.path.join(directory, directory_name), chas)
    return chas


###
###  Main script
###
def main():
    chas = None
    http_server_thread = HTTPServerThread()

    # Create a command line parser
    parser = argparse.ArgumentParser(description="chas system for running statefull or stateless cron jobs.")
    parser.add_argument("action", choices=["list", "start", "run"])
    parser.add_argument("job", nargs="?")
    parser.add_argument("--package", "-p", nargs=1, dest="option_package")
    parser.add_argument("--show-times", action="store_true", dest="option_show_times")
    parser.add_argument("--http-server", action="store_true", dest="option_http_server")
    args = parser.parse_args()
    # Register all chas jobs within the directory
    sys.path.append(os.getcwd())
    chas = import_files_from_directory(package=args.option_package)

    if chas is None:
        print("No jobs registered.")
        return None
    
    # Process command line command
    if args.action == "list":
        jobs = chas.get_jobs()
        print_jobs_with_times(chas, checking=False)
    elif args.action == "start":
        if args.option_http_server is True:
            # Start Flask app in a different thread
            http_server_thread.start()
            time.sleep(1)
            print_jobs_with_times(chas)
            # Cron jobs will run in main thread
            while True:
                time.sleep(3)
                if chas.is_runnable_job:
                    chas.run_jobs()
                    print_jobs_with_times(chas)
        else:
            print_jobs_with_times(chas)
            while True:
                time.sleep(3)
                if chas.is_runnable_job:
                    chas.run_jobs()
                    print_jobs_with_times(chas)
    elif args.action == "run":
        try:
            state = chas.run_job(name=args.job, different_thread=False)
        except Exception as e:
            if isinstance(e, JobNotFoundException):
                print(e)
            else:
                raise(e)
