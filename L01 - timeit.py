from time import perf_counter, sleep
from random import random


def timeit(n):  # Accept n as an argument
    """
    Used as a decorator. Executes the decorated function n times and prints the average execution time.

    Parameters
    ----------
    n: int
        Number of times to execute the function.
    """

    def decorator(f): # This is the actual decorator
        def wrapper(*args, **kwargs):
            exec_time = 0
            return_value = None  # Inicializar

            for i in range(n):
                start = perf_counter()
                return_value = f(*args, **kwargs)  # Important to calculate the return value inside the loop
                end = perf_counter()
                exec_time += end - start
                avg_time = exec_time / n
                print(
                    f"@timeit Function {f.__name__}: Average execution time {avg_time:.6f} seconds over {n} iterations."
                )
            return return_value

        return wrapper

    return decorator # Return the decorator


if __name__ == "__main__":

    @timeit(5)
    def example_function():
        # This is where I would do something useful
        sleep(1 * random())

    example_function()