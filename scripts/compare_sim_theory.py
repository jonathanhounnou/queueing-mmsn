import numpy as np
import matplotlib.pyplot as plt
from queueing.simulator import simulate_mmsn
from queueing.analytical import stationary_distribution, performance_measures

list_of_p_est = []
list_of_block_est = []
for seed in range(10):
    results = simulate_mmsn(10, 3, 4, 15, 50000, seed)
    list_of_p_est.append(results["p_est"])
    list_of_block_est.append(results["block_est"])
p = np.array(list_of_p_est)
b = np.array(list_of_block_est)
estimated_p_n = p.mean(axis = 0)
std_p = p.std(axis = 0)
estimated_block = b.mean(axis = 0)
std_block = b.std(axis = 0)
exact_p_n = stationary_distribution(10, 3, 4, 15)
exact_results = performance_measures(10, 3, 4, 15)
exact_block = exact_results["P_block"]
x = np.arange(16)
w = 0.4
plt.bar(x - w/2, exact_p_n, width = w, label="Theory")
plt.bar(x + w/2, estimated_p_n, width = w, yerr=std_p, label="Simulation")
plt.xlabel("System State")
plt.ylabel("Probabilities")
plt.xticks(x)
plt.legend()
plt.savefig("figures/sim_vs_theory.png", dpi=150)
print(f"P_block theory     = {exact_block:.4f}")
print(f"P_block simulation = {estimated_block:.4f} +/- {std_block:.4f}")
print(f"Max |P_n sim - P_n theory| = {np.max(np.abs(estimated_p_n - exact_p_n)):.4f}")
plt.show()
