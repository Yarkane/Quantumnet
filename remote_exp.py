import requests
import time
import json

ADDRESS = "http://127.0.0.1:5000"


def remote_launch(address, args):
    r = requests.post(address + "/controller", json={
        "sig": args['sig'],
        "kex": args['kex'],
        "nodes": args['nodes'],
        "cpu": args['cpu'],
        "bw": args['bandwith'],
        "delay": args['delay'],
        "loss": args['loss'],
        "queue": args['queue'],
        "port": args['port'],
        "time": args['time_exp'],
        "hybrid_sig": args["hybrid_sig"],
        "hybrid_kex": args["hybrid_kex"]
    })
    return r


def experiment_one_case(address, args):
    ret = remote_launch(address, args)
    if ret.status_code == 200:
        time.sleep(3 + args['time_exp'])
        return requests.get(address + "/result")
    else:
        print("Error for an experiment.")
        return {}


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
    'time_exp': 5
}

# Experiment
results = []

for loss in [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2]:
    arguments["loss"] = loss
    res = experiment_one_case(ADDRESS, arguments)
    results.append(dict(arguments, **res))
    requests.get(ADDRESS, params={"action": "ok"})

with open('results.json', 'w') as outfile:
    json.dump(results, outfile)
