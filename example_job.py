"""A simple python example to use with the ray-launch.sh script.

Example usage:

./ray-launch.sh -n 20 -e ray-python -p "example_job.py --num_tasks 50"

This will allocate 20 slots on the cluster, divide them (by default) into 20/4=5
nodes, and run this python script using the ray-python conda environment.
"""

import time
import argparse
import numpy as np
import ray

parser = argparse.ArgumentParser()
parser.add_argument('--num_tasks', help='Number of workers and actors to spawn.',
                    type=int, default=100, required=False)
num_tasks = parser.parse_args().num_tasks

# Connect to the existing Ray cluster we spun up with the ray-launch.sh script.
ray.init(address='auto')

print('\nResources available to this Ray client:')
for resource, count in ray.available_resources().items():
    print(f'{resource}: {count}')
print('')

@ray.remote
def do_work(x):
    """Simple stateless worker."""
    # Do something here.
    time.sleep(0.001)
    return x ** 2

@ray.remote
class Actor():
    """Stateful worker (Actor)."""

    def __init__(self, x):
        self._x = x

    def do_work(self, y):
        # Do something here.
        time.sleep(0.001)
        self._x = self._x + y

    def get_x(self):
        return self._x

# === Use stateless workers ===

# Dispatch `num_tasks` workers to do something with a random input.
print(f'Dispatching {num_tasks} workers')
futures = [do_work.remote(x=np.random.rand(1000)) for _ in range(num_tasks)]
# Wait until all workers return results.
result = ray.get(futures)
print('Worker tasks complete:', len(result))

# === Use stateful actors ===

print(f'Creating {num_tasks} actors')
# Create `num_tasks` actors before sending them work.
actors = [Actor.remote(x=np.random.rand(1000)) for _ in range(num_tasks)]
# Send some random work to the actors.
for actor in actors:
    actor.do_work.remote(y=np.random.rand(1000))
# Wait until all actors finish and return results.
futures = [actor.get_x.remote() for actor in actors]
result = ray.get(futures)
print('Actor tasks complete:', len(result))

print('Python script successfully finished, terminating Ray client.\n')
ray.shutdown()  # Cleanup.
