# queueing-mmsn

Exact analysis of the M/M/s/N queue in Python: stationary distribution
and performance measures (blocking probability, L, Lq, W, Wq), with tests.

## Usage

    from queueing.analytical import performance_measures
    performance_measures(lam=1, mu=2, s=1, N=2)

## Tests

    pip install -e ".[dev]"
    pytest

## Roadmap
- [x] Analytical module
- [ ] Staffing cost optimization
- [ ] Discrete-event simulation and validation against theory