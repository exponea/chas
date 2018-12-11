import time
from main import sisyphus

@sisyphus.job("20:54")
def export_two(state):
    print("two")

