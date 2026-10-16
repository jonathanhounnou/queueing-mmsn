import pytest
from queueing.simulator import simulate_trace
from queueing.analytical import stationary_distribution, performance_measures
from queueing.simulator import simulate_mmsn

def test_hand_example():
    arrivals = [0.5, 0.8, 1.2, 1.4, 2.4]
    services = [0.8, 0.6, 0.5, 0.7, 0.4]
    res = simulate_trace(arrivals, services, s=1, N=2)
    assert res["rejected"] == 1
    assert res["time_in_state"] == pytest.approx([0.5, 1.3, 1.2])
    assert res["total_time"] == pytest.approx(3.0)

def test_simulation_matches_theory():
     lam, mu, s, N = 1, 2, 1, 2
     res = simulate_mmsn(lam, mu, s, N, n_customers=50_000, seed=42)
     p_theory = stationary_distribution(lam, mu, s, N)
     for est, exact in zip(res["p_est"], p_theory):
        assert abs(est - exact) < 0.02
     assert abs(res["block_est"] - performance_measures(lam, mu, s, N)["P_block"]) < 0.02