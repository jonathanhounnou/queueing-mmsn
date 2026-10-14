# queueing-mmsn

Exact analysis of the M/M/s/N queue in Python: stationary distribution
and performance measures (blocking probability, L, Lq, W, Wq), with tests.

## Usage

    from queueing.analytical import performance_measures
    performance_measures(lam=1, mu=2, s=1, N=2)

## Staffing optimization

 Cost per unit time = s * c_server + Lq * c_wait + lam * P_block * c_loss.
 Parameters: lam = 10, mu = 3, N = 15, c_server = 20, c_wait = 5, c_loss = 50.

 [Cost vs servers](figures/costs_over_servers_graph.png)
  The minimum cost is reached at s = 4. With fewer servers, the offered load
  (lam/mu ≈ 3.33) exceeds the service capacity s*mu, so many customers are rejected
  and the loss term dominates the cost. With more servers, waiting and blocking
  vanish and the cost is driven only by the staffing term s * c_server, which makes
  the curve a straight line of slope c_server = 20. The optimum is shallow: s = 5
  costs only slightly more than s = 4.

## Tests

    pip install -e ".[dev]"
    pytest

## Roadmap
- [x] Analytical module
- [x] Staffing cost optimization
- [ ] Discrete-event simulation and validation against theory