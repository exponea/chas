from flask import Flask, render_template
from threading import Thread
from main import sisyphus

http_server = Flask("sisyphus")

http_server.logger.setLevel("DEBUG")

@http_server.route("/healthz")
def healthz():
    return "ok"

@http_server.route("/")
def main():
    return render_template("main.html", sisyphus=sisyphus)

@http_server.route("/jobs/<job_name>/restart", methods=["POST"])
def job_restart(job_name):
    sisyphus.run_job(job_name)
    return "ok"

class HTTPServerThread(Thread):
    def run(self):
        http_server.run('0.0.0.0', 5000)

