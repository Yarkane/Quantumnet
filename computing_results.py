# Experiences manquantes : Fal768 en général, Fal512 en général, Rainbow en général, Fal1024xFiresaber

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
"""
L1_loss_graph("2", dil2_lightsaber,
              "Handshake and page download time\nDilithium2 + Lightsaber, 2 nodes",
              "figures/LOSS_dil2_lightsaber_2n")

L1_loss_graph("2", Hdil2_lightsaber,
              "Handshake and page download time\nHybrid Dilithium2 + Lightsaber, 2 nodes",
              "figures/LOSS_hybrid_dil2_lightsaber_2n")

L1_loss_graph("2", dil2_Hlightsaber,
              "Handshake and page download time\nDilithium2 + Hybrid Lightsaber, 2 nodes",
              "figures/LOSS_dil2_hybrid_lightsaber_2n")

L1_loss_graph("2", Hdil2_Hlightsaber,
              "Handshake and page download time\nHybrid Dilithium2 + Hybrid Lightsaber, 2 nodes",
              "figures/LOSS_hybrid_dil2_hybrid_lightsaber_2n")

L1_loss_graph("16", dil2_lightsaber,
              "Handshake and page download time\nDilithium2 + Lightsaber, 16 nodes",
              "figures/LOSS_dil2_lightsaber_16n")

L1_loss_graph("16", Hdil2_lightsaber,
              "Handshake and page download time\nHybrid Dilithium2 + Lightsaber, 16 nodes",
              "figures/LOSS_hybrid_dil2_lightsaber_16n")

L1_loss_graph("16", dil2_Hlightsaber,
              "Handshake and page download time\nDilithium2 + Hybrid Lightsaber, 16 nodes",
              "figures/LOSS_dil2_hybrid_lightsaber_16n")

L1_loss_graph("16", Hdil2_Hlightsaber,
              "Handshake and page download time\nHybrid Dilithium2 + Hybrid Lightsaber, 16 nodes",
              "figures/LOSS_hybrid_dil2_hybrid_lightsaber_16n")
"""
# Nodes evolution


def nodes_graph(data, title, filename):
    x, y = [], []
    for nodes in data.keys():
        x.append(int(nodes))
        y.append(get_mean_RTT(data, nodes))
    plt.plot(x, y)
    plt.xlabel("Number of nodes")
    plt.ylabel("Mean RTT per handshake (seconds)")
    plt.title(title)
    plt.grid()
    plt.savefig(filename)
    plt.show()

"""
nodes_graph(dil2_lightsaber,
            "Handshake and page download time\nDilithium2 + Lightsaber",
            "figures/NODES_dil2_lightsaber")

nodes_graph(Hdil2_lightsaber,
            "Handshake and page download time\nHybrid Dilithium2 + Lightsaber",
            "figures/NODES_hybrid_dil2_lightsaber")

nodes_graph(dil2_Hlightsaber,
            "Handshake and page download time\nDilithium2 + Hybrid Lightsaber",
            "figures/NODES_dil2_hybrid_lightsaber")

nodes_graph(Hdil2_Hlightsaber,
            "Handshake and page download time\nHybrid Dilithium2 + Hybrid Lightsaber",
            "figures/NODES_hybrid_dil2_hybrid_lightsaber")
"""
# --

dil4_saber = get_experiments(make_filename("dil4", "saber"))
Hdil4_saber = get_experiments(make_filename("dil4", "saber", h_sig=True))
dil4_Hsaber = get_experiments(make_filename("dil4", "saber", h_kex=True))
Hdil4_Hsaber = get_experiments(make_filename("dil4", "saber", h_sig=True, h_kex=True))
"""
nodes_graph(dil4_saber,
            "Handshake and page download time\nDilithium4 + Saber",
            "figures/NODES_dil4_saber")

nodes_graph(Hdil4_saber,
            "Handshake and page download time\nHybrid Dilithium4 + Saber",
            "figures/NODES_hybrid_dil4_saber")

nodes_graph(dil4_Hsaber,
            "Handshake and page download time\nDilithium4 + Hybrid Saber",
            "figures/NODES_dil4_hybrid_saber")

nodes_graph(Hdil4_Hsaber,
            "Handshake and page download time\nHybrid Dilithium4 + Hybrid Saber",
            "figures/NODES_hybrid_dil4_hybrid_saber")
"""
# --

# fal1024_firesaber = get_experiments(make_filename("fal1024", "firesaber"))
# Hfal1024_firesaber = get_experiments(make_filename("fal1024", "firesaber", h_sig=True))
fal1024_Hfiresaber = get_experiments(make_filename("fal1024", "firesaber", h_kex=True))
# Hfal1024_Hfiresaber = get_experiments(make_filename("fal1024", "firesaber", h_sig=True, h_kex=True))
"""
nodes_graph(fal1024_Hfiresaber,
            "Handshake and page download time\nFalcon1024 + Hybrid Firesaber",
            "figures/NODES_fal1024_hybrid_firesaber")
"""
# Comparing blank / hybrid / double hybrid


def hybrid_graph(data_qq, data_hq, data_qh, data_hh, nodes, title, filename, kex, sig):
    x, y = [], []
    x.append(kex + "\n" + sig)
    y.append(get_mean_RTT(data_qq, nodes))

    x.append("Hybrid " + kex + "\n" + sig)
    y.append(get_mean_RTT(data_hq, nodes))

    x.append(kex + "\n" + "Hybrid " + sig)
    y.append(get_mean_RTT(data_qh, nodes))

    x.append("Hybrid " + kex + "\n" + "Hybrid " + sig)
    y.append(get_mean_RTT(data_hh, nodes))

    plt.bar(x, y)
    plt.ylabel("Mean RTT per handshake (seconds)")
    plt.ylim(bottom=0.12)
    plt.ylim(top=0.24)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


hybrid_graph(dil2_lightsaber, Hdil2_lightsaber, dil2_Hlightsaber, Hdil2_Hlightsaber, "8",
             "Hybrid and non-hybrid comparison\nDilithium2 + Lightsaber, 8 nodes",
             "figures/HYBRID_dil2_lightsaber", "Dilithium2", "Lightsaber")

hybrid_graph(dil4_saber, Hdil4_saber, dil4_Hsaber, Hdil4_Hsaber, "8",
             "Hybrid and non-hybrid comparison\nDilithium4 + Saber, 8 nodes",
             "figures/HYBRID_dil4_saber", "Dilithium4", "Saber")
"""
fal1024_ntru5 = get_experiments(make_filename("fal1024", "ntru5"))
Hfal1024_ntru5 = get_experiments(make_filename("fal1024", "ntru5", h_sig=True))
fal1024_Hntru5 = get_experiments(make_filename("fal1024", "ntru5", h_kex=True))
Hfal1024_Hntru5 = get_experiments(make_filename("fal1024", "ntru5", h_sig=True, h_kex=True))

hybrid_graph(fal1024_ntru5, Hfal1024_ntru5, fal1024_Hntru5, Hfal1024_Hntru5, "8",
             "Hybrid and non-hybrid comparison\nFalcon1024 + NTRU HPS4096821, 8 nodes",
             "figures/HYBRID_fal1024_ntru5", "Falcon1024", "L5 NTRU")

fal1024_lightsaber = get_experiments(make_filename("fal1024", "lightsaber"))
Hfal1024_lightsaber = get_experiments(make_filename("fal1024", "lightsaber", h_sig=True))
fal1024_Hlightsaber = get_experiments(make_filename("fal1024", "lightsaber", h_kex=True))
Hfal1024_Hlightsaber = get_experiments(make_filename("fal1024", "lightsaber", h_sig=True, h_kex=True))

hybrid_graph(fal1024_lightsaber, Hfal1024_lightsaber, fal1024_Hlightsaber, Hfal1024_Hlightsaber, "8",
             "Hybrid and non-hybrid comparison\nFalcon1024 + Lightsaber, 8 nodes",
             "figures/HYBRID_fal1024_lightsaber", "Falcon1024", "lightsaber")
"""
dil2_ntru1 = get_experiments(make_filename("dil2", "ntru1"))
Hdil2_ntru1 = get_experiments(make_filename("dil2", "ntru1", h_sig=True))
dil2_Hntru1 = get_experiments(make_filename("dil2", "ntru1", h_kex=True))
Hdil2_Hntru1 = get_experiments(make_filename("dil2", "ntru1", h_sig=True, h_kex=True))

hybrid_graph(dil2_ntru1, Hdil2_ntru1, dil2_Hntru1, Hdil2_Hntru1, "8",
             "Hybrid and non-hybrid comparison\nDilithium2 + NTRU HPS2048509, 8 nodes",
             "figures/HYBRID_dil2_ntru1", "Dilithium2", "L1 NTRU")

# L1 duets
x, y = [], []

x.append("Dilithium2\nLightsaber")
y.append(get_mean_RTT(dil2_lightsaber, "8"))

x.append("Dilithium2\nL1 NTRU")
y.append(get_mean_RTT(dil2_ntru1, "8"))

dil2_kyber512 = get_experiments(make_filename("dil2", "kyber512"))
x.append("Dilithium2\nKyber 512")
y.append(get_mean_RTT(dil2_kyber512, "8"))

plt.bar(x, y)
plt.ylabel("Mean RTT per handshake (seconds)")
plt.ylim(bottom=0.14)
plt.ylim(top=0.18)
plt.title("L1xL1 schemes comparison, 8 nodes")
plt.savefig("figures/ALGS_L1_L1")
plt.show()

# L3 duets
x, y = [], []

x.append("Dilithium4\nSaber")
y.append(get_mean_RTT(dil4_saber, "8"))

dil4_ntru3 = get_experiments(make_filename("dil4", "ntru3"))
x.append("Dilithium4\nL3 NTRU")
y.append(get_mean_RTT(dil4_ntru3, "8"))

dil4_kyber768 = get_experiments(make_filename("dil4", "kyber768"))
x.append("Dilithium4\nKyber 768")
y.append(get_mean_RTT(dil4_kyber768, "8"))

plt.bar(x, y)
plt.ylabel("Mean RTT per handshake (seconds)")
plt.ylim(bottom=0.20)
plt.ylim(top=0.24)
plt.title("L3xL3 schemes comparison, 8 nodes")
plt.savefig("figures/ALGS_L3_L3")
plt.show()

# L5 duets
x, y = [], []

fal1024_ntru5 = get_experiments(make_filename("fal1024", "ntru5"))
x.append("Falcon 1024\nL5 NTRU")
y.append(get_mean_RTT(fal1024_ntru5, "8"))

fal1024_kyber1024 = get_experiments(make_filename("fal1024", "kyber1024"))
x.append("Falcon 1024\nKyber 1024")
y.append(get_mean_RTT(fal1024_kyber1024, "8"))

plt.bar(x, y)
plt.ylabel("Mean RTT per handshake (seconds)")
plt.ylim(bottom=0.16)
plt.ylim(top=0.18)
plt.title("L5xL5 schemes comparison, 8 nodes")
plt.savefig("figures/ALGS_L5_L5")
plt.show()

# L1xL3 duets
x, y = [], []

dil2_saber = get_experiments(make_filename("dil2", "saber"))
x.append("Dilithium2\nSaber")
y.append(get_mean_RTT(dil2_saber, "8"))

fal512_saber = get_experiments(make_filename("fal512", "saber"))
x.append("Falcon 512\nSaber")
y.append(get_mean_RTT(fal512_saber, "8"))

rainbowIa_saber = get_experiments(make_filename("rainbowIa", "saber"))
x.append("RainbowIaclassic\nSaber")
y.append(get_mean_RTT(rainbowIa_saber, "8"))

plt.bar(x, y)
plt.ylabel("Mean RTT per handshake (seconds)")
plt.ylim(bottom=0.12)
plt.ylim(top=1.5)
plt.title("L1xL3 schemes comparison, 8 nodes")
plt.savefig("figures/ALGS_L1_L3")
plt.show()

# L1xL5 duets
x, y = [], []

dil2_firesaber = get_experiments(make_filename("dil2", "firesaber"))
x.append("Dilithium2\nFiresaber")
y.append(get_mean_RTT(dil2_firesaber, "8"))

fal1024_lightsaber = get_experiments(make_filename("fal1024", "lightsaber"))
x.append("Falcon 1024\nLightsaber")
y.append(get_mean_RTT(fal1024_lightsaber, "8"))

rainbowVc_lightsaber = get_experiments(make_filename("rainbowVc", "lightsaber"))
x.append("RainbowVcClassic\nLightsaber")
y.append(get_mean_RTT(rainbowVc_lightsaber, "8"))

plt.bar(x, y)
plt.ylabel("Mean RTT per handshake (seconds)")
plt.ylim(bottom=0.12)
plt.ylim(top=15)
plt.title("L1xL5 schemes comparison, 8 nodes")
plt.savefig("figures/ALGS_L1_L5")
plt.show()
