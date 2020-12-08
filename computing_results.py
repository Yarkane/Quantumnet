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


def make_filename(sig, kex, h_sig=False, h_kex=False):
    """
    sig : dil2, dil4, fal512, fal1024, rainbowIa, rainbowVc
    kex : lightsaber, saber, firesaber, kyber512, kyber768, kyber1024, ntru1, ntru3, ntru5
    """
    hybrid_s, hybrid_k = "", ""
    if h_sig:
        hybrid_s = "hybrid_"
    if h_kex:
        hybrid_k = "hybrid_"
    return f'results/results_ALGS_{hybrid_s}{sig}_{hybrid_k}{kex}_VAR_nodes_loss.json'


def get_mean_RTT(data, nodes):
    rtt = []
    for exp in data[nodes]:
        rtt.append(get_rtt(exp))
    return sum(rtt)/len(rtt)

# Loss variations for L1


def L1_loss_graph(nodes, data, title, filename):
    x, y = [], []
    for exp in data[nodes]:
        x.append(exp["loss"])
        y.append(get_rtt(exp))
    plt.plot(x, y)
    plt.xlabel("Packet Loss percentage (%)")
    plt.ylabel("Mean RTT per handshake (seconds)")
    plt.title(title)
    plt.grid()
    plt.savefig(filename)
    plt.show()


dil2_lightsaber = get_experiments(make_filename("dil2", "lightsaber"))
Hdil2_lightsaber = get_experiments(make_filename("dil2", "lightsaber", h_sig=True))
dil2_Hlightsaber = get_experiments(make_filename("dil2", "lightsaber", h_kex=True))
Hdil2_Hlightsaber = get_experiments(make_filename("dil2", "lightsaber", h_sig=True, h_kex=True))

L1_loss_graph("2", dil2_lightsaber,
              "RTT evolution with handshake\nDilithium2 + Lightsaber, 2 nodes",
              "figures/LOSS_dil2_lightsaber_2n")

L1_loss_graph("2", Hdil2_lightsaber,
              "RTT evolution with handshake\nHybrid Dilithium2 + Lightsaber, 2 nodes",
              "figures/LOSS_hybrid_dil2_lightsaber_2n")

L1_loss_graph("2", dil2_Hlightsaber,
              "RTT evolution with handshake\nDilithium2 + Hybrid Lightsaber, 2 nodes",
              "figures/LOSS_dil2_hybrid_lightsaber_2n")

L1_loss_graph("2", Hdil2_Hlightsaber,
              "RTT evolution with handshake\nHybrid Dilithium2 + Hybrid Lightsaber, 2 nodes",
              "figures/LOSS_hybrid_dil2_hybrid_lightsaber_2n")

L1_loss_graph("16", dil2_lightsaber,
              "RTT evolution with handshake\nDilithium2 + Lightsaber, 16 nodes",
              "figures/LOSS_dil2_lightsaber_16n")

L1_loss_graph("16", Hdil2_lightsaber,
              "RTT evolution with handshake\nHybrid Dilithium2 + Lightsaber, 16 nodes",
              "figures/LOSS_hybrid_dil2_lightsaber_16n")

L1_loss_graph("16", dil2_Hlightsaber,
              "RTT evolution with handshake\nDilithium2 + Hybrid Lightsaber, 16 nodes",
              "figures/LOSS_dil2_hybrid_lightsaber_16n")

L1_loss_graph("16", Hdil2_Hlightsaber,
              "RTT evolution with handshake\nHybrid Dilithium2 + Hybrid Lightsaber, 16 nodes",
              "figures/LOSS_hybrid_dil2_hybrid_lightsaber_16n")

# L1 Nodes evolution


