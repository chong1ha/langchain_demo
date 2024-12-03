import time
from functools import wraps


def elapsed_time(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        print("Sync execution time:", (end_time - start_time))
        return result

    return wrapper
# End of elapsed_time