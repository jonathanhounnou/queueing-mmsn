import matplotlib.pyplot as plt
from queueing.analytical import optimal_servers
results = optimal_servers(10, 3, 15, 20, 5, 50)
measures = results[1]
servers = measures.keys()
costs = measures.values()
plt.plot(servers, costs, marker="o")
plt.scatter([results[0]], [measures[results[0]]], color="red", s=120, zorder=3)
plt.xlabel("Number of servers")
plt.ylabel("Cost per unit of time")
plt.title("Costs variation over the number of servers")
plt.annotate(f"s optimal = {results[0]}", (results[0], measures[results[0]]),
             textcoords="offset points", xytext=(15, 15))
plt.grid(alpha=0.3)
plt.savefig("figures/costs_over_servers_graph.png", dpi = 150)
plt.show()