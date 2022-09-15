import time
import sys
from tqdm import tqdm

iterator = tqdm(range(99), file=open("/dev/null", "w"))

for x in iterator:
    print(iterator.__str__())
    sys.stdout.flush()
    time.sleep(0.2)