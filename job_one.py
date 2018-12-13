import time
from main import sisyphus


@sisyphus.job("17:59")
def export_one_a(state):
    print("one_a")
    state.success()

@sisyphus.job("18:12")
def export_one_b(state):
    print("one_b")

@sisyphus.job("18:02")
def export_one_c(state):
    print("one_c")

@sisyphus.job("19:02")
def export_one_d(state):
    print("one_d")
