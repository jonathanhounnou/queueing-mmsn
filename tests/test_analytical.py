import math
import pytest
from queueing.analytical import (
    stationary_distribution,
    performance_measures,
    total_cost,
    optimal_servers,
)


def test_small_case():
    p = stationary_distribution(lam=1, mu=2, s=1, N=2)
    assert p == pytest.approx([4/7, 2/7, 1/7])


def test_probabilities_sum_to_one():
    p = stationary_distribution(lam=10, mu=3, s=4, N=15)
    assert sum(p) == pytest.approx(1.0)

def test_performance_small_case():
    m = performance_measures(lam=1, mu=2, s=1, N=2)
    assert m["P_block"] == pytest.approx(1/7)
    assert m["L"] == pytest.approx(4/7)
    assert m["Lq"] == pytest.approx(1/7)
    assert m["lam_eff"] == pytest.approx(6/7)
    assert m["W"] == pytest.approx(2/3)
    assert m["Wq"] == pytest.approx(1/6)


def test_service_time_consistency():
    m = performance_measures(lam=10, mu=3, s=4, N=15)
    assert m["W"] - m["Wq"] == pytest.approx(1/3)

def test_rho_equal_one():
    # lam = s * mu  =>  rho = 1, tous les poids pour n >= s sont égaux
    p = stationary_distribution(lam=2, mu=1, s=2, N=5)
    assert sum(p) == pytest.approx(1.0)
    assert p[2] == pytest.approx(p[3])
    assert p[3] == pytest.approx(p[4])
    assert p[4] == pytest.approx(p[5])


@pytest.mark.parametrize("lam, mu, s, N", [
    (10, 3, 4, 15),   # rho != 1
    (2, 1, 2, 5),     # rho == 1
])
def test_p0_matches_closed_form(lam, mu, s, N):
    # P_0 de ton mémoire, formule (3.1)
    a = lam / mu
    rho = lam / (s * mu)
    first = sum(a**n / math.factorial(n) for n in range(s))
    geom = (1 - rho**(N - s + 1)) / (1 - rho) if rho != 1 else N - s + 1
    p0 = 1 / (first + a**s / math.factorial(s) * geom)
    assert stationary_distribution(lam, mu, s, N)[0] == pytest.approx(p0)

def test_total_cost_small_case():
    # P_block = 1/7, Lq = 1/7, lam = 1  =>  10 + 2/7 + 5/7 = 11
    c = total_cost(lam=1, mu=2, s=1, N=2, c_server=10, c_wait=2, c_loss=5)
    assert c == pytest.approx(11)


def test_optimal_servers_is_the_minimum():
    s_opt, costs = optimal_servers(lam=10, mu=3, N=15,
                                   c_server=20, c_wait=5, c_loss=50)
    assert costs[s_opt] == min(costs.values())
    assert set(costs) == set(range(1, 16))


def test_expensive_servers_give_one_server():
    s_opt, _ = optimal_servers(lam=1, mu=2, N=5,
                               c_server=1e6, c_wait=1, c_loss=1)
    assert s_opt == 1


def test_no_waiting_room_when_s_equals_N():
    m = performance_measures(lam=1, mu=2, s=1, N=1)
    assert m["P_block"] == pytest.approx(1/3)
    assert m["Lq"] == pytest.approx(0)
    assert m["Wq"] == pytest.approx(0)