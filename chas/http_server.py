from flask import Flask, render_template
from threading import Thread
from chas import chas
import os


http_server = Flask("chas")

http_server.logger.setLevel("DEBUG")

@http_server.route("/healthz")
def healthz():
    return "ok"

@http_server.route("/")
def main():
    return render_template("main.html", chas=chas)

@http_server.route("/jobs/<job_name>/restart", methods=["POST"])
def job_restart(job_name):
    print("new request for RESTART {}".format(job_name))
    job_thread = Thread(target=run_job, args=[job_name])
    job_thread.start()
    return "{}".format(os.__file__)


# Callable target for a thread, which runs the job
def run_job(job_name):
    try:
        state = chas.run_job(job_name)
    except Exception as e:
        print("Expection in job thread: {}".format(str(e)))


class HTTPServerThread(Thread):
    def run(self):
        http_server.run('0.0.0.0', 5000)
