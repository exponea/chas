import time
from main import sisyphus

@sisyphus.job("21:35")
def export_two(state):
    time.sleep(10)
    state.fail()

