import pq_server_simulation
import json

# Parameters
arguments = {
    'sig': "dilithium2",
    'kex': "saber",
    'hybrid_sig': False,
    'hybrid_kex': False,
    'nodes': 5,
    'cpu': 1,
    'bandwith': 8,
    'delay': "10ms",
    'loss': 0,
    'queue': 14,
    'port': "4433",
    'time_exp': 15
}

# Experiment : more and more nodes, more and more loss

results = []

for nodes in [2, 4, 8, 16]:
    arguments["nodes"] = nodes
    for loss in [1, 2, 3, 4, 5, 8, 10, 15, 20]:
        arguments["loss"] = loss
        res = pq_server_simulation.simulate("4433", arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"],
                                            arguments["nodes"], arguments["queue"], arguments["time_exp"])
        results.append({**arguments, **res})

with open('results/results_ALGS_dil2_saber_VAR_nodes_loss.json', 'w') as outfile:
    json.dump(results, outfile)
