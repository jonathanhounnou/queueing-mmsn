import heapq
from collections import deque
import numpy as np

def simulate_trace(arrivals: list[float], services: list[float],
                   s: int, N: int) -> dict:
    """Simulate an M/M/s/N-like queue on a given list of arrivals and service times."""
    n = 0 # number of customers in the system
    t_last = 0.0 # time of last event
    time_in_state = [0.0] * (N + 1) # time spent in each state
    rejected = 0 # number of rejected customers
    departures = [] # list of departure times
    waiting = deque() # queue of waiting customers
    for a, d in zip(arrivals, services):
        while(departures and departures[0] <= a):
            t = heapq.heappop(departures)
            time_in_state[n] += t - t_last
            t_last = t
            n = n - 1
            if(waiting):
                d_next = waiting.popleft()
                heapq.heappush(departures, t + d_next)
        t = a
        time_in_state[n] += t - t_last
        t_last = t
        if( n == N):
            rejected += 1
        else:
            if(n < s):
                heapq.heappush(departures, a + d)
            else:
                waiting.append(d)
            n = n + 1
    while(departures):
        t = heapq.heappop(departures)
        time_in_state[n] += t - t_last
        t_last = t
        n = n - 1
        if(waiting):
            d_next = waiting.popleft()
            heapq.heappush(departures, t + d_next)
    results = {}
    results["time_in_state"] = time_in_state
    results["rejected"] = rejected
    results["total_time"] = t_last
    return results

def simulate_mmsn(lam: float, mu: float, s: int, N: int,
                  n_customers: int, seed: int = 0) -> dict:
    """Simulate an M/M/s/N queue with random arrivals and service times."""
    rng = np.random.default_rng(seed)
    arrivals = rng.exponential(1 / lam, n_customers)
    arrivals = np.cumsum(arrivals)
    services = rng.exponential(1 / mu, n_customers)
    results = simulate_trace(arrivals, services, s, N)
    estimation = {}
    estimation["p_est"] = [time / results["total_time"] for time in results["time_in_state"]]
    estimation["block_est"] = results["rejected"] / n_customers
    return estimation