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

ciphertext_or_signature_sizes = {  # In bytes
    "kyber512": 736,
    "kyber768": 1088,
    "kyber1024": 1568,
    "ntru1": 699,
    "ntru3": 930,
    "ntru5": 1230,
    "lightsaber": 736,
    "saber": 1088,
    "firesaber": 1472,
    "dil2": 2044,
    "dil3": 2701,
    "dil4": 3366,
    "falcon512": 690,
    "falcon1024": 1330,
    "picnic3l1": 14612,
    "picnic3l3": 35028,
    "picnic3l5": 61028,
    "rainbowIa": 64,
    "rainbowVc": 204
}

public_key_sizes = {  # In bytes
    "kyber512": 800,
    "kyber768": 1184,
    "kyber1024": 1568,
    "ntru1": 699,
    "ntru3": 930,
    "ntru5": 1230,
    "lightsaber": 672,
    "saber": 992,
    "firesaber": 1312,
    "dil2": 1184,
    "dil3": 1472,
    "dil4": 1760,
    "falcon512": 897,
    "falcon1024": 1793,
    "picnic3l1": 35,
    "picnic3l3": 49,
    "picnic3l5": 65,
    "rainbowIa": 148992,
    "rainbowVc": 1705536
}

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


def get_rtt_max_loss(data, nodes):
    max_loss = 0
    res = {}
    for exp in data[nodes]:
        if exp["loss"] > max_loss:
            res = exp
            max_loss = exp["loss"]
    return get_rtt(res), max_loss

# Loss variations for L1


def loss_graph(nodes, data, legend):
    x, y = [], []
    for exp in data[nodes]:
        x.append(exp["loss"])
        y.append(get_rtt(exp))
    plt.plot(x, y, label=legend)


dil2_lightsaber = get_experiments(make_filename("dil2", "lightsaber", new=True))
dil3_saber = get_experiments(make_filename("dil3", "saber", new=True))
dil4_firesaber = get_experiments(make_filename("dil4", "firesaber", new=True))

loss_graph("8", dil2_lightsaber, "Dilithium2 + Lightsaber (L1xL1)")
loss_graph("8", dil3_saber, "Dilithium3 + Saber (L2xL3)")
loss_graph("8", dil4_firesaber, "Dilithium4 + Firesaber (L3xL5)")

plt.xlabel("Packet Loss percentage (%)")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Handshake time evolution with the loss rate, 8 nodes")
plt.grid()
plt.legend()
plt.savefig("figures/LOSS")
plt.show()

# Loss variation against hybrids for L1

Hdil2_lightsaber = get_experiments(make_filename("dil2", "lightsaber", new=True, h_sig=True))
dil2_Hlightsaber = get_experiments(make_filename("dil2", "lightsaber", new=True, h_kex=True))
Hdil2_Hlightsaber = get_experiments(make_filename("dil2", "lightsaber", new=True, h_sig=True, h_kex=True))

loss_graph("8", dil2_lightsaber, "Dilithium2 + Lightsaber")
loss_graph("8", Hdil2_lightsaber, "Dilithium2 and EC curve + Lightsaber")
loss_graph("8", dil2_Hlightsaber, "Dilithium2 + Lightsaber and EC curve")
loss_graph("8", Hdil2_Hlightsaber, "Dilithium2 and EC curve + Lightsaber and EC curve")

plt.xlabel("Packet Loss percentage (%)")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Handshake time evolution with the loss rate, 8 nodes")
plt.grid()
plt.legend()
plt.savefig("figures/LOSS_hybrids")
plt.show()

# Nodes evolution

def nodes_graph(data, title):
    x, y = [], []
    exp = (0, 100)
    for nodes in data.keys():
        exp = get_rtt_min_loss(data, nodes)
        x.append(int(nodes))
        y.append(exp[0])
    plt.plot(x, y, label=title + ", loss = " + str(exp[1]) + " %")


old_dil2_lightsaber = get_experiments(make_filename("dil2", "lightsaber", new=False))

nodes_graph(dil2_lightsaber, "Dilithium2 + Lightsaber (L1)")
nodes_graph(old_dil2_lightsaber, "Dilithium2 + Lightsaber (L1)")


plt.xlabel("Number of nodes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Handshake time evolution with the nodes")
plt.grid()
plt.legend()
plt.savefig("figures/NODES")
plt.show()

# Nodes evolution against hybrids

nodes_graph(dil2_lightsaber, "Dilithium2 + Lightsaber")
nodes_graph(Hdil2_lightsaber, "Dilithium2 and EC curve + Lightsaber")
nodes_graph(dil2_Hlightsaber, "Dilithium2 + Lightsaber and EC curve")
nodes_graph(Hdil2_Hlightsaber, "Dilithium2 and EC curve + Lightsaber and EC curve")


plt.xlabel("Number of nodes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Handshake time evolution with the nodes")
plt.grid()
plt.legend()
plt.savefig("figures/NODES_hybrid")
plt.show()

# Comparing blank / hybrid / double hybrid


def hybrid_graph(data_qq, data_hq, data_qh, data_hh, nodes, title, filename, kex, sig, all_same=True, bot=0.2, top=0.5):
    x, y = [], []
    if all_same:
        f = get_mean_RTT
    else:
        f = get_rtt_min_loss

    x.append(kex + "\n" + sig)
    y.append(f(data_qq, nodes)[0])

    x.append("Hybrid " + kex + "\n" + sig)
    y.append(f(data_hq, nodes)[0])

    x.append(kex + "\n" + "Hybrid " + sig)
    y.append(f(data_qh, nodes)[0])

    x.append("Hybrid " + kex + "\n" + "Hybrid " + sig)
    y.append(f(data_hh, nodes)[0])

    plt.bar(x, y)
    plt.ylabel("Mean time per handshake + download (seconds)")
    plt.ylim(bottom=bot)
    plt.ylim(top=top)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


hybrid_graph(dil2_lightsaber, Hdil2_lightsaber, dil2_Hlightsaber, Hdil2_Hlightsaber, "16",
             "Hybrid comparisons for low loss rate values and 16 nodes\nDilithium2 + Lightsaber (L1 schemes)",
             "figures/HYBRID_dil2_lightsaber", "Lightsaber", "Dilithium2", all_same=False, bot=0.1, top=0.4)

rainIa_kyber512 = get_experiments(make_filename("rainbowIa", "kyber512", new=True))
HrainIa_kyber512 = get_experiments(make_filename("rainbowIa", "kyber512", new=True, h_sig=True))
rainIa_Hkyber512 = get_experiments(make_filename("rainbowIa", "kyber512", new=True, h_kex=True))
HrainIa_Hkyber512 = get_experiments(make_filename("rainbowIa", "kyber512", new=True, h_sig=True, h_kex=True))

hybrid_graph(rainIa_kyber512, HrainIa_kyber512, rainIa_Hkyber512, HrainIa_Hkyber512, "8",
             "Hybrid comparisons for low loss rate values and 8 nodes\nRainbowIa + Kyber512 (L1 schemes)",
             "figures/HYBRID_rainbowIa_kyber512", "Kyber512", "RainbowIa", all_same=False, bot=1.1, top=1.5)

rainVc_kyber1024 = get_experiments(make_filename("rainbowVc", "kyber1024", new=True))
HrainVc_kyber1024 = get_experiments(make_filename("rainbowVc", "kyber1024", new=True, h_sig=True))
rainVc_Hkyber1024 = get_experiments(make_filename("rainbowVc", "kyber1024", new=True, h_kex=True))
HrainVc_Hkyber1024 = get_experiments(make_filename("rainbowVc", "kyber1024", new=True, h_sig=True, h_kex=True))

hybrid_graph(rainVc_kyber1024, HrainVc_kyber1024, rainVc_Hkyber1024, HrainVc_Hkyber1024, "8",
             "Hybrid comparisons for low loss rate values and 8 nodes\nRainbowVc + Kyber1024 (L1 schemes)",
             "figures/HYBRID_rainbowVc_kyber1024", "Kyber1024", "RainbowVc", all_same=False, bot=10, top=16)

# Picnic Comparisons

picnic1_saber = get_experiments(make_filename("picnic1", "saber", new=True))
Hpicnic1_saber = get_experiments(make_filename("picnic1", "saber", new=True, h_sig=True))
picnic3_saber = get_experiments(make_filename("picnic3", "saber", new=True))
Hpicnic3_saber = get_experiments(make_filename("picnic3", "saber", new=True, h_sig=True))
picnic5_saber = get_experiments(make_filename("picnic5", "saber", new=True))
Hpicnic5_saber = get_experiments(make_filename("picnic5", "saber", new=True, h_sig=True))

loss_graph("8", picnic1_saber, "Picnic1 + Saber")
loss_graph("8", Hpicnic1_saber, "Hybrid Picnic1 + Saber")
loss_graph("8", picnic3_saber, "Picnic3 + Saber")
loss_graph("8", Hpicnic3_saber, "Hybrid Picnic3 + Saber")
loss_graph("8", picnic5_saber, "Picnic5 + Saber")
loss_graph("8", Hpicnic5_saber, "Hybrid Picnic5 + Saber")

plt.xlabel("Packet Loss percentage (%)")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Handshake time evolution with the loss rate, 8 nodes")
plt.grid()
plt.legend()
plt.savefig("figures/LOSS_Picnic_all")
plt.ylim(top=2)
plt.savefig("figures/LOSS_Picnic_detail")
plt.show()

# LOW LOSS, CIPHERTEXT SIZE

old_dil2_saber = get_experiments(make_filename("dil2", "saber", new=False))
old_dil2_firesaber = get_experiments(make_filename("dil2", "firesaber", new=False))
old_dil2_kyber512 = get_experiments(make_filename("dil2", "kyber512", new=False))
old_dil2_ntru1 = get_experiments(make_filename("dil2", "ntru1", new=False))

x, y = [], []
for exp in [(old_dil2_lightsaber, "lightsaber"), (old_dil2_saber, "saber"), (old_dil2_firesaber, "firesaber"), (old_dil2_kyber512, "kyber512"), (old_dil2_ntru1, "ntru1")]:
    res = get_mean_RTT(exp[0], "8")
    plt.scatter(ciphertext_or_signature_sizes[exp[1]], res)
    plt.annotate(exp[1], (ciphertext_or_signature_sizes[exp[1]], res))

plt.plot(x, y)
plt.xlabel("Ciphertext size in Bytes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Completion time evoluting with ciphertext size for low loss rate, 8 nodes.")
plt.grid()
plt.savefig("figures/CIPHERTEXT_LOW_LOSS")
plt.show()

# LOW LOSS, SIGNATURE SIZE

old_dil4_saber = get_experiments(make_filename("dil4", "saber", new=False))
old_fal512_saber = get_experiments(make_filename("fal512", "saber", new=False))
old_rainbowIa_saber = get_experiments(make_filename("rainbowIa", "saber", new=False))

x, y = [], []
for exp in [(old_dil2_saber, "dil2"), (old_dil4_saber, "dil4"), (old_fal512_saber, "falcon512"), (old_rainbowIa_saber, "rainbowIa")]:
    res = get_mean_RTT(exp[0], "8")
    plt.scatter(ciphertext_or_signature_sizes[exp[1]], res)
    plt.annotate(exp[1], (ciphertext_or_signature_sizes[exp[1]], res))

plt.plot(x, y)
plt.xlabel("Signature size in Bytes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Completion time evoluting with signature size for low loss rate, 8 nodes.")
plt.grid()
plt.savefig("figures/SIGNATURE_LOW_LOSS")
plt.show()


# HIGH LOSS, CIPHERTEXT SIZE

dil2_kyber768 = get_experiments(make_filename("dil2", "kyber768", new=True))
dil2_kyber1024 = get_experiments(make_filename("dil2", "kyber1024", new=True))
dil3_saber = get_experiments(make_filename("dil3", "saber", new=True))

x, y = [], []
for exp in [(dil2_lightsaber, "lightsaber"), (dil2_kyber768, "kyber768"), (dil2_kyber1024, "kyber1024"), (dil3_saber, "saber")]:
    res = get_mean_RTT(exp[0], "8")
    plt.scatter(ciphertext_or_signature_sizes[exp[1]], res)
    plt.annotate(exp[1], (ciphertext_or_signature_sizes[exp[1]], res))

plt.plot(x, y)
plt.xlabel("Ciphertext size in Bytes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Completion time evoluting with ciphertext size for high loss rate, 8 nodes.")
plt.grid()
plt.savefig("figures/CIPHERTEXT_HIGH_LOSS")
plt.show()

# HIGH LOSS, CIPHERTEXT SIZE

dil2_Hsaber = get_experiments(make_filename("dil2", "saber", h_kex=True, new=True))
fal512_Hsaber = get_experiments(make_filename("fal512", "saber", h_kex=True, new=True))
rainIa_Hsaber = get_experiments(make_filename("rainbowIa", "saber", h_kex=True, new=True))

x, y = [], []
for exp in [(dil2_Hsaber, "dil2"), (dil4_firesaber, "dil4"), (fal512_Hsaber, "falcon512"), (picnic1_saber, "picnic3l1"), (picnic3_saber, "picnic3l3"), (picnic5_saber, "picnic3l5"), (rainIa_Hsaber, "rainbowIa")]:
    res = get_mean_RTT(exp[0], "8")
    plt.scatter(ciphertext_or_signature_sizes[exp[1]], res)
    plt.annotate(exp[1], (ciphertext_or_signature_sizes[exp[1]], res))

plt.plot(x, y)
plt.xlabel("Signature size in Bytes")
plt.ylabel("Mean time per handshake + download (seconds)")
plt.title("Completion time evoluting with signature size for high loss rate, 8 nodes.")
plt.grid()
plt.savefig("figures/SIGNATURE_HIGH_LOSS")
plt.show()