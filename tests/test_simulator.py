import pytest
from queueing.simulator import simulate_trace


def test_hand_example():
    arrivals = [0.5, 0.8, 1.2, 1.4, 2.4]
    services = [0.8, 0.6, 0.5, 0.7, 0.4]
    res = simulate_trace(arrivals, services, s=1, N=2)
    assert res["rejected"] == 1
    assert res["time_in_state"] == pytest.approx([0.5, 1.3, 1.2])
    assert res["total_time"] == pytest.approx(3.0)