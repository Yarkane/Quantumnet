
import matplotlib.pyplot as plt
import json

"""
Format :

"tls_port": "4433", 
"sig": "p521_falcon1024",
"kex": "p521_ntru_hps4096821", 
"hybrid_sig": false, 
"hybrid_kex": false, 
"nodes": 2, 
"cpu": 1, 
"bandwith": 8, 
"delay": "10ms", 
"loss": 0.05, 
"queue": 14, 
"port": "4433", 
"time_exp": 60, 
"www": true, 
"nb_seconds": "60", 
"nb_connections_unrealsecs": "508", 
"nb_unrealsecs": "9.18", 
"nb_conn_user_secs": "55.34", 
"bytes_read": "153924\r", 
"nb_connections_realsecs": "508", 
"nb_realsecs": "61", 
"bytes_read_per_conn": "303"}
"""


# Functions


def get_experiments(filename):
    """
    Returns the experiment data ordered by nodes
    """
    data = json.load(open(filename, 'r'))
    ret = {}
    for experiment in data:
        nodes = str(experiment["nodes"])
        if nodes not in ret.keys():
            ret[nodes] = [experiment]
        else:
            ret[nodes].append(experiment)
    return ret


def get_rtt(experiment):
    return float(experiment["nb_realsecs"]) / float(experiment["nb_connections_realsecs"])


def make_filename(sig, kex, h_sig=False, h_kex=False, new=False):
    """
    sig : dil2, dil4, fal512, fal1024, rainbowIa, rainbowVc
    kex : lightsaber, saber, firesaber, kyber512, kyber768, kyber1024, ntru1, ntru3, ntru5
    """
    hybrid_s, hybrid_k = "", ""
    if h_sig:
        hybrid_s = "hybrid_"
    if h_kex:
        hybrid_k = "hybrid_"
    if new:
        folder = "results2"
    else:
        folder = "results"
    return f'{folder}/results_ALGS_{hybrid_s}{sig}_{hybrid_k}{kex}_VAR_nodes_loss.json'


def get_mean_RTT(data, nodes):
    # NOT FOR COMPARISON
    rtt = []
    for exp in data[nodes]:
        rtt.append(get_rtt(exp))
    return sum(rtt)/len(rtt)


def get_rtt_min_loss(data, nodes):
    min_loss = 100
    res = {}
    for exp in data[nodes]:
        if exp["loss"] < min_loss:
            res = exp
            min_loss = exp["loss"]
    return get_rtt(res), min_loss


def nodes_graph(data1, data2, title, filename):
    x, y = [], []
    minloss = 100
    for nodes in data1.keys():
        exp = get_rtt_min_loss(data1, nodes)
        x.append(int(nodes))
        y.append(exp[0])
        minloss = exp[1]
    plt.plot(x, y, label="Data from first experiments, loss = " + str(minloss) + " %")

    x, y = [], []
    minloss = 100
    for nodes in data2.keys():
        exp = get_rtt_min_loss(data2, nodes)
        x.append(int(nodes))
        y.append(exp[0])
        minloss = exp[1]
    plt.plot(x, y, label="Data from second experiments, loss = " + str(minloss) + " %")

    plt.xlabel("Number of nodes")
    plt.ylabel("Mean time per handshake + Download (seconds)")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.show()


dil2_lightsaber_res1 = get_experiments(make_filename("dil2", "lightsaber", new=False))
dil2_lightsaber_res2 = get_experiments(make_filename("dil2", "lightsaber", new=True))
nodes_graph(dil2_lightsaber_res1, dil2_lightsaber_res2, "Experiment 1 and 2 comparison (dilithium2 + lightsaber)",
            "figures_firt_exps/comparaison_dil2_light")
