#!/usr/bin/env python3

# spin_async_proc.py

# credits: Example by Luciano Ramalho inspired by
# Michele Simionato's multiprocessing example in the python-list:
# https://mail.python.org/pipermail/python-list/2009-February/538048.html

# BEGIN PRIME_ASYNCIO
import asyncio
import itertools
from concurrent import futures
import time

import primes

async def spin(msg):  # <1>
    for char in itertools.cycle('⠇⠋⠙⠸⠴⠦'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)  # <2>
        except asyncio.CancelledError:  # <3>
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


async def slow_function():  # <4>
    loop = asyncio.get_running_loop()
    with futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool,
                    primes.is_prime, 3033700317376073)
    return result


async def supervisor():  # <6>
    spinner = asyncio.create_task(spin('thinking!'))  # <7>
    print('spinner object:', spinner)  # <8>
    result = await slow_function()  # <9>
    spinner.cancel()  # <10>
    return result


def main():
    t0 = time.perf_counter()
    result = asyncio.run(supervisor())  # <11>
    dt = time.perf_counter() - t0
    print('Answer:', result)
    print(f'Elapsed time: {dt:0.3}s')


if __name__ == '__main__':
    main()
# END SPINNER_ASYNCIO
