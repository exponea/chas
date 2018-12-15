import importlib
import datetime
import argparse
import time
import os
from http_server import http_server, HTTPServerThread
from main import sisyphus


# Helper to show all jobs with next run times
def print_jobs_with_times():
    jobs = sisyphus.get_jobs()
    # Find the longest job name in order to pad columns properly
    column_width_first = max(len(job.name) for job in jobs) + 2
    column_width_second = max(len(str(job.next_run)) for job in jobs) + 2
    column_width_third = max(len(job.last_state.status) for job in jobs) + 2
    print()
    print("========== Checking jobs at {} ==========".format(datetime.datetime.now().strftime("%H:%M:%S")))
    print("".join(["Job".ljust(column_width_first), "Next run".ljust(column_width_second), "Last run".ljust(column_width_second), "Last status".ljust(column_width_third)]))
    for job in jobs:
        print("".join([job.name.ljust(column_width_first), str(job.next_run).ljust(column_width_second), str(job.last_run).ljust(column_width_second), str(job.last_state.status).ljust(column_width_third)]))
    print()

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


###
###  Main script
###

http_server_thread = HTTPServerThread()

# Create a command line parser
parser = argparse.ArgumentParser(description="Sisyphus system for running statefull or stateless cron jobs.")
parser.add_argument("action", choices=["list", "start", "run"])
parser.add_argument("job", nargs="?")
parser.add_argument("--show-times", action="store_true", dest="option_show_times")
parser.add_argument("--http-server", action="store_true", dest="option_http_server")
args = parser.parse_args()

# Register all sisyphus jobs within the directory
import_files_from_directory(".")

# Process command line command
if args.action == "list": # python sisyphus.py list
    jobs = sisyphus.get_jobs()
    print_jobs_with_times()
elif args.action == "start": # python sisyphus.py start
    if args.option_http_server is True:
        # Start Flask app in a different thread
        http_server_thread.start()
        time.sleep(1)
        print_jobs_with_times()
        # Cron jobs will run in main thread
        while True:
            time.sleep(3)
            if sisyphus.is_runnable_job:
                sisyphus.run_jobs()
                print_jobs_with_times()
    while True:
        time.sleep(3)
        if sisyphus.is_runnable_job:
            sisyphus.run_jobs()
            print_jobs_with_times()
elif args.action == "run": # python sisyphus.py run
    print("Running job {}".format(args.job))
    state = sisyphus.run_job(args.job)
    if state is None:
        print("Job {} was not found.")
    else:
        print("Job {} ended with status {}".format(args.job, state.status))
