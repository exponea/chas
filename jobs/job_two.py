import time
from main import sisyphus

@sisyphus.job("8:38")
def export_two(state):
    print("EXPORT TWOO")
    time.sleep(10)
    state.failed()

