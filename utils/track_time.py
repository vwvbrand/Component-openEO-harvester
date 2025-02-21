import time
from IPython.core.getipython import get_ipython

# dictionary to store execution times and start times
execution_times = {}
start_times = {}

# to track execution time for a named process
def track_time(process_name, execution_time):
    if process_name not in execution_times:
        execution_times[process_name] = 0  # if process was never defined initilaize
    execution_times[process_name] += execution_time
    print(f"[{process_name}] Total execution time (cumulative): {execution_times[process_name]:.2f} seconds")

# Function to register execution tracking for a specific process
def register_time(process_name="default"):
    ipython = get_ipython()

    # capture start time before run cells
    def pre_run_cell(*args, **kwargs):  # any arguments!
        start_times[process_name] = time.time()

    # capture end time after each cell runs
    def post_run_cell(result):  # receives ExecutionResult
        if process_name in start_times:
            execution_time = time.time() - start_times[process_name]
            track_time(process_name, execution_time)

    # register the event handlers
    ipython.events.register('pre_run_cell', pre_run_cell)
    ipython.events.register('post_run_cell', post_run_cell)

    # store functions for later removal
    start_times[f"{process_name}_pre"] = pre_run_cell
    start_times[f"{process_name}_post"] = post_run_cell

    print(f"Tracking execution time for process: {process_name}")

# stop tracking execution time
def stop_time(process_name="default"):
    ipython = get_ipython()

    # unregister event handlers
    pre_func = start_times.get(f"{process_name}_pre")
    post_func = start_times.get(f"{process_name}_post")

    if pre_func:
        ipython.events.unregister('pre_run_cell', pre_func)
    if post_func:
        ipython.events.unregister('post_run_cell', post_func)

    if process_name in execution_times:
        print(f"Stopped tracking execution time for process: {process_name}. Total time: {execution_times[process_name]:.2f} s")

# function to get the total execution time for a process
def get_time(process_name="default"):
    elapsed_time = execution_times.get(process_name, 0)
    print(f"Total execution time for {process_name}: {elapsed_time:.2f}")
    return elapsed_time
