import time

timers = {}

def start_timer(name = "default"):
    timers[name] = time.time()
    print(f"Timer {name} started...")

def stop_timer(name = "default"):
    if name not in timers:
        print(f"Timer {name} has not been started.")
        return None

    elapsed_time = time.time() - timers[name]
    print(f"Timer {name}: {elapsed_time:.2f} s")
    del(timers[name])
    return(elapsed_time)
