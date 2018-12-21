#!/usr/bin/env python3
import importlib.util
import datetime
import argparse
import time
import os
from chas.http_server import http_server, HTTPServerThread


# Helper to show all jobs with next run times
def print_jobs_with_times(chas):
    jobs = chas.get_jobs()
    if len(jobs) == 0:
        print("No jobs are registered.")
        return None
    # Find the longest job name in order to pad columns properly
    column_width_first = max(len(job.name) for job in jobs) + 2
    column_width_second = max(len(str(job.next_run)) for job in jobs) + 2
    column_width_third = max(len(job.last_state.status) for job in jobs) + 2
    print()
    print("========== Checking jobs at {} ==========".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    print("".join(["Job".ljust(column_width_first), "Next run".ljust(column_width_second), "Last run".ljust(column_width_second), "Last status".ljust(column_width_third)]))
    for job in jobs:
        next_run = job.next_run if isinstance(job.next_run, str) else job.next_run.strftime("%d-%m-%Y %H:%M:%S")
        last_run = job.last_run if isinstance(job.last_run, str) else job.last_run.strftime("%d-%m-%Y %H:%M:%S")
        print("".join([job.name.ljust(column_width_first), next_run.ljust(column_width_second), last_run.ljust(column_width_second), job.last_state.status.ljust(column_width_third)]))
    print()

# Find all jobs by crawling through directory
def import_files_from_directory(directory=os.getcwd(), chas=None):
    files = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and "job_" == name[:4] and ".py" == name[-3:]]
    for file_path in files:
        module_name = os.path.basename(file_path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        if chas is None:
            chas = foo.chas
    directories = [name for name in os.listdir(directory) if os.path.isdir(name) and "." != name[0] and "__" != name[:2]]
    for directory_name in directories:
        import_files_from_directory(directory_name, chas)
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
    parser.add_argument("--show-times", action="store_true", dest="option_show_times")
    parser.add_argument("--http-server", action="store_true", dest="option_http_server")
    args = parser.parse_args()

    # Register all chas jobs within the directory
    chas = import_files_from_directory()
    
    # Process command line command
    if args.action == "list": # python chas.py list
        jobs = chas.get_jobs()
        print_jobs_with_times(chas)
    elif args.action == "start": # python chas.py start
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
        while True:
            time.sleep(3)
            if chas.is_runnable_job:
                chas.run_jobs()
                print_jobs_with_times(chas)
    elif args.action == "run": # python chas.py run
        print("Running job {}".format(args.job))
        state = chas.run_job(args.job)
        if state is None:
            print("Job {} was not found.")
        else:
            print("Job {} ended with status {}".format(args.job, state.status))
