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

class HTTPServerThread(Thread):
    def run(self):
        http_server.run('0.0.0.0', 5000)

