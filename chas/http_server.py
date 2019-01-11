import os
from chas.exceptions import JobNotFoundException
from flask import Flask, render_template
from threading import Thread
from chas import chas


http_server = Flask("chas")

http_server.logger.setLevel("DEBUG")

@http_server.route("/healthz")
def healthz():
    return "ok"

@http_server.route("/")
def main():
    return render_template("main.html", chas=chas)

@http_server.route("/jobs/<job_name>/run", methods=["POST"])
def job_run(job_name):
    try:
        chas.run_job(job_name)
    except JobNotFoundException as e:
        return "Job {} not found\n".format(job_name), 202
    return "ok", 200


class HTTPServerThread(Thread):
    def run(self):
        http_server.run('0.0.0.0', 5000)
