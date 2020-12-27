import pq_server_simulation
import json

# Parameters
arguments = {
    'tls_port': "4433",
    'sig': "p521_falcon1024",
    'kex': "p521_ntru_hps4096821",
    'hybrid_sig': False,
    'hybrid_kex': False,
    'nodes': 5,
    'cpu': 1,
    'bandwith': 8,
    'delay': "10ms",
    'loss': 0,
    'queue': 14,
    'port': "4433",
    'time_exp': 60,
    'www': True
}

# ---

# -- RSA DSA
results = []
arguments["sig"] = "DSA"
arguments["kex"] = "RSA"


for nodes in [2, 4, 8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 5, 10, 15, 20]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_RSA_DSA_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)


# BELOW ARE LOSS0 ADDITIONS


# -- L1
results = []
arguments["sig"] = "dilithium2"
arguments["kex"] = "lightsaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_lightsaber_VAR_nodes_loss.json'
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)


arguments["sig"] = "p256_dilithium2"
results = []

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_lightsaber_VAR_nodes_loss.json'

with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

arguments["sig"] = "dilithium2"
arguments["kex"] = "p256_lightsaber"
results = []

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_lightsaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)


arguments["sig"] = "p256_dilithium2"
results = []

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_hybrid_lightsaber_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

# Now we will do less things because it is too looong

# LOSS CURVES
results = []
arguments["sig"] = "dilithium3"
arguments["kex"] = "saber"


for nodes in [8]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil3_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "dilithium4"
arguments["kex"] = "firesaber"


for nodes in [8]:
    arguments["nodes"] = nodes
    for loss in [0]:
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil4_firesaber_VAR_nodes_loss.json'

with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

# Let's test picnic

results = []
arguments["sig"] = "picnic3l1"
arguments["kex"] = "saber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_picnic1_saber_VAR_nodes_loss.json'
 
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_picnic3l1"
arguments["kex"] = "saber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_picnic1_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "picnic3l3"
arguments["kex"] = "saber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_picnic3_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p384_picnic3l3"
arguments["kex"] = "saber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_picnic3_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "picnic3l5"
arguments["kex"] = "saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_picnic5_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p521_picnic3l5"
arguments["kex"] = "saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_picnic5_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

# Ok now new combinations
# Experiences manquantes : Fal768 en général, Fal512 en général, Rainbow en général, Fal1024xFiresaber
# MORE FALCONS

results = []
arguments["sig"] = "falcon512"
arguments["kex"] = "p384_saber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal512_hybrid_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "lightsaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal512_lightsaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p256_lightsaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal512_hybrid_lightsaber_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "lightsaber"
arguments["sig"] = "p256_falcon512"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal512_lightsaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p256_lightsaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal512_hybrid_lightsaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "falcon1024"
arguments["kex"] = "p521_ntru_hps4096821"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_hybrid_ntru5_VAR_nodes_loss.json'

with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p256_lightsaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_hybrid_lightsaber_VAR_nodes_loss.json'
 
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "ntru_hps2048677"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_ntru3_VAR_nodes_loss.json'
 
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_ntru_hps2048677"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_hybrid_ntru3_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p521_falcon1024"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_hybrid_ntru3_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "ntru_hps2048677"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_ntru3_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "firesaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_firesaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p521_firesaber"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_hybrid_firesaber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "falcon512"
arguments["kex"] = "kyber90s1024"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal512_kyber1024_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p521_kyber90s1024"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal512_hybrid_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "kyber90s1024"
arguments["sig"] = "p256_falcon512"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal512_kyber1024_VAR_nodes_loss.json'
 
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p521_kyber90s1024r"


for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal512_hybrid_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

# MORE KYBER

results = []
arguments["kex"] = "p384_saber"
arguments["sig"] = "dilithium2"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "kyber768"
arguments["sig"] = "dilithium2"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_kyber768_VAR_nodes_loss.json'
   
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_kyber768"
arguments["sig"] = "dilithium2"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_kyber768_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "kyber1024"
arguments["sig"] = "dilithium2"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_kyber1024"
arguments["sig"] = "dilithium2"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

# MORE RAINBOW

results = []
arguments["kex"] = "p384_saber"
arguments["sig"] = "rainbowIaclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowIa_hybrid_saber_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p256_lightsaber"
arguments["sig"] = "rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowVc_hybrid_lightsaber_VAR_nodes_loss.json'

with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "kyber1024"
arguments["sig"] = "rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowVc_kyber1024_VAR_nodes_loss.json'
  
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p521_rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowVc_kyber1024_VAR_nodes_loss.json'
   
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "rainbowVcclassic"
arguments["kex"] = "p521_kyber1024"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowVc_hybrid_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p521_rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowVc_hybrid_kyber1024_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "kyber512"
arguments["sig"] = "rainbowIaclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowIa_kyber512_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_rainbowIaclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowIa_kyber512_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "rainbowIaclassic"
arguments["kex"] = "p256_kyber512"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowIa_hybrid_kyber512_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_rainbowIaclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowIa_hybrid_kyber512_VAR_nodes_loss.json'
    
with open(filename, 'r') as infile:
    exps = json.load(infile)

results = results + exps

with open(filename, 'w+') as outfile:
    json.dump(results, outfile)


# - MORE RAINBOW

results = []
arguments["kex"] = "saber"
arguments["sig"] = "rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowVc_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowVc_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "rainbowVcclassic"
arguments["kex"] = "p384_saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowVc_hybrid_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_rainbowVcclassic"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_rainbowVc_hybrid_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "rainbowIaclassic"
arguments["kex"] = "p384_saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_rainbowIa_hybrid_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

# All in saber

results = []
arguments["sig"] = "fal1024"
arguments["kex"] = "saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_fal1024_hybrid_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p521_fal1024"
arguments["kex"] = "saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_saber"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_fal1024_hybrid_saber_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

# All in dil2

results = []
arguments["sig"] = "dil2"
arguments["kex"] = "ntru_hps4096821"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_ntru5_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p521_ntru_hps4096821"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_ntru5_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_dil2"
arguments["kex"] = "ntru_hps4096821"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_ntru5_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p521_ntru_hps4096821"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_hybrid_ntru5_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "dil2"
arguments["kex"] = "ntru_hps2048677"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_ntru3_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_ntru_hps2048677"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_dil2_hybrid_ntru3_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["sig"] = "p256_dil2"
arguments["kex"] = "ntru_hps2048677"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_ntru3_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)

results = []
arguments["kex"] = "p384_ntru_hps2048677"

for nodes in [8, 12, 16, 24, 30, 36, 42]:
    arguments["nodes"] = nodes
    for loss in [0, 1, 2, 3, 5]:
        arguments["loss"] = loss
        print(f"algs : {arguments['sig']},{arguments['kex']} | nodes : {nodes} | loss : {loss}")
        res = pq_server_simulation.simulate(arguments["tls_port"], arguments["kex"], arguments["sig"],
                                            arguments["bandwith"], arguments["delay"], arguments["loss"],
                                            arguments["cpu"], arguments["nodes"], arguments["queue"],
                                            arguments["time_exp"], arguments["www"])
        results.append({**arguments, **res})

filename = 'results2/results_ALGS_hybrid_dil2_hybrid_ntru3_VAR_nodes_loss.json'
with open(filename, 'w') as outfile:
    json.dump(results, outfile)
