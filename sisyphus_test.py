import time
from sisyphus import Sisyphus
from state import State


sisyphus = Sisyphus()
test_state = State()

@sisyphus.job("17:59")
def export_a(state):
    print("a")

@sisyphus.job("18:12")
def export_b(state):
    print("b")

@sisyphus.job("18:02")
def export_c(state):
    print("c")

@sisyphus.job("19:02")
def export_d(state):
    print("d")

sisyphus.check_jobs()
