import math
def stationary_distribution(lam: float, mu: float, s: int, N: int) -> list[float]:
    """Return [P_0, ..., P_N] for an M/M/s/N queue."""
    rho = lam / (s * mu)
    weights = []
    for n in range(N+1):
        if(n<s):
            w_n = (1/math.factorial(n)) * ((lam/mu) ** n)
            weights.append(w_n)
        else:
            w_n = (1/math.factorial(s)) * ((lam/mu) ** s) * (rho ** (n-s))
            weights.append(w_n)
    P_0 = 1/sum(weights)
    return [w * P_0 for w in weights]

def performance_measures(lam: float, mu: float, s: int, N: int) -> dict[str, float]:
    """Return P_block, L, Lq, lam_eff, W, Wq for an M/M/s/N queue."""
    p = stationary_distribution(lam, mu, s, N)
    perf_measures = {}
    perf_measures["P_block"] = p[-1]
    L_ = []
    for n in range(1,N+1):
        L_.append(n*p[n])
    L = sum(L_)
    perf_measures["L"] = L
    L_q_ = []
    for n in range(s,N+1):
        L_q_.append((n-s)*p[n])
    L_q = sum(L_q_)
    perf_measures["Lq"] = L_q
    lam_eff = lam * (1-p[-1])
    perf_measures["lam_eff"] = lam_eff
    W = L/ lam_eff
    W_q = L_q/ lam_eff
    perf_measures["W"] = W
    perf_measures["Wq"] = W_q
    return perf_measures

def total_cost(lam: float, mu: float, s: int, N: int,
               c_server: float, c_wait: float, c_loss: float) -> float:
    """Expected cost per unit time of an M/M/s/N queue."""
    measures = performance_measures(lam, mu, s, N)
    Lq = measures["Lq"]
    P_block = measures["P_block"]
    cost = (s * c_server) + (Lq * c_wait) + (lam * P_block * c_loss)
    return cost

def optimal_servers(lam: float, mu: float, N: int,
                    c_server: float, c_wait: float, c_loss: float) -> tuple[int, dict[int, float]]:
    """Return (best s, {s: cost}) for s = 1..N."""
    opt_servers = {}
    for s in range(1, N+1):
        opt_servers[s] = total_cost(lam, mu, s, N, c_server, c_wait, c_loss)
    best_servers = min(opt_servers, key = opt_servers.get)
    return (best_servers, opt_servers)
