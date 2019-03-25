import os
from prometheus_flask_exporter import PrometheusMetrics
from chas.exceptions import JobNotFoundException
from flask import Flask, render_template
from threading import Thread
from chas import chas


http_server = Flask("chas")
# Set up Prometheus listening on /metrics endpoint
metrics = PrometheusMetrics(http_server)

http_server.logger.setLevel("DEBUG")

metrics.info('app_info', 'Chas version info', version='0.4.0')

@http_server.route("/healthz")
def healthz():
    return "ok"

@http_server.route("/")
def main():
    return render_template("main.html", chas=chas)

@http_server.route("/jobs/<job_name>/run", methods=["POST"])
def job_run(job_name):
    try:
        chas.run_job(name=job_name)
    except JobNotFoundException as e:
        return "Job {} not found\n".format(job_name), 202
    return "ok", 200


class HTTPServerThread(Thread):
    def run(self):
        http_server.run('0.0.0.0', 5000)
