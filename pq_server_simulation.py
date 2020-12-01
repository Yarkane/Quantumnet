from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet, Host
import click
import time
import os
import re

wd = os.getcwd()
SupportedSigs = [
    "dilithium2", "dilithium3", "dilithium4",
    "falcon512", "falcon1024",
    "rainbowIaclassic", "rainbowVcclassic",
    "DSA"
]
SupportedKex = [
    "lightsaber", "saber", "firesaber",
    "ntru_hps2048509", "ntru_hps2048677", "ntru_hps4096821", "ntru_hrss701",
    "kyber512", "kyber768", "kyber1024", "kyber90s512", "kyber90s768", "kyber90s1024",
    "EC"
]
LevelOfSecurity = {
    "dilithium2": 1,
    "dilithium3": 2,
    "dilithium4": 3,
    "falcon512": 1,
    "falcon1024": 5,
    "rainbowIaclassic": 1,
    "rainbowVcclassic": 5,
    "lightsaber": 1,
    "saber": 3,
    "firesaber": 5,
    "ntru_hps2048509": 1,
    "ntru_hps2048677": 3,
    "ntru_hps4096821": 5,
    "ntru_hrss701": 3,
    "kyber512": 1,
    "kyber768": 3,
    "kyber1024": 5,
    "kyber90s512": 1,
    "kyber90s768": 3,
    "kyber90s1024": 5,
    "DSA": 0,
    "EC": 0
}


class QuantumTopo(Topo):
    def build(self, bw=8, delay="10ms", loss=0, cpu_usage=1, n_nodes=1, max_queue=14):
        clients = []
        switch1 = self.addSwitch('switch1')
        switch2 = self.addSwitch('switch2')

        if cpu_usage < 1:
            appServer = self.addHost('aServer', cls=CPULimitedHost, cpu=cpu_usage)
        else:
            appServer = self.addHost('aServer')
        crossServer = self.addHost('cServer')

        for i in range(n_nodes):
            appClient = self.addHost('aClient_' + str(i))
            clients.append(appClient)
            crossClient = self.addHost('cClient_' + str(i))
            self.addLink(appClient, switch1)
            self.addLink(crossClient, switch1)

        self.addLink(appServer, switch2)
        self.addLink(crossServer, switch2)
        self.addLink(switch1, switch2, bw=bw, delay=delay, loss=loss, max_queue_size=max_queue)


def parse_return(ret):
    """
    Format :
    Collecting Connection statistics for 5 seconds
    *******

    x connections in xs; x connections/user sec, bytes read 0
    x connections in x real seconds, x bytes read per connection
    """
    lines = ret.split("\n")
    try:
        nb_seconds = lines[0].split(" ")[4]
        nb_connections_unrealsecs = lines[3].split(" ")[0]
        nb_unrealsecs = lines[3].split(" ")[3][:-2]
        nb_conn_user_secs = lines[3].split(" ")[4]
        bytes_read = lines[3].split(" ")[9]
        nb_connections_realsecs = lines[4].split(" ")[0]
        nb_realsecs = lines[4].split(" ")[3]
        bytes_read_per_conn = lines[4].split(" ")[6]
        return {
            "nb_seconds": nb_seconds,
            "nb_connections_unrealsecs": nb_connections_unrealsecs,
            "nb_unrealsecs": nb_unrealsecs,
            "nb_conn_user_secs": nb_conn_user_secs,
            "bytes_read": bytes_read,
            "nb_connections_realsecs": nb_connections_realsecs,
            "nb_realsecs": nb_realsecs,
            "bytes_read_per_conn": bytes_read_per_conn
        }
    except:
        return ret




def nginx_setup(addr):
    # addr : format x.x.x.x:pppp
    nginx_config = (f"\n"
                    f"#user nobody;\n"
                    f"worker_processes auto;\n"
                    f"\n"
                    f"#pid logs/nginx.pid;\n"
                    f"\n"
                    f"events {{\n"
                    f"	worker_connections 1024;\n"
                    f"}}\n"
                    f"\n"
                    f"http {{\n"
                    f"#	include ../conf/mime.types;\n"
                    f"#	default_type application/octet-stream;\n"
                    f"\n"
                    f"	sendfile on;\n"
                    f"	keepalive_timeout 65;\n"
                    f"\n"
                    f"	# HTTPS server\n"
                    f"	server {{\n"
                    f"		listen {addr} ssl;\n"
                    f"\n"
                    f"		access_log {wd}/logs/access.log;\n"
                    f"		error_log {wd}/logs/error.log;\n"
                    f"\n"
                    f"		ssl_certificate {wd}/pki/server.crt;\n"
                    f"		ssl_certificate_key {wd}/pki/server.key;\n"
                    f"\n"
                    f"		ssl_session_cache shared:SSL:1m;\n"
                    f"		ssl_session_timeout 5m;\n"
                    f"\n"
                    f"		ssl_protocols TLSv1.3;\n"
                    f"\n"
                    f"		location / {{\n"
                    f"			root {wd}/html;\n"
                    f"			index index.html index.htm;\n"
                    f"		}}\n"
                    f"	}}\n"
                    f"}}\n"
                    f"\n")
    filename = "nginx/conf/nginx.conf"
    with open(filename, 'w') as f:
        f.write(nginx_config)
        f.close()


def prepare_PKI(sig):
    # Returns the command that will prepare the PKI for the nginx server
    return f'rm -f {wd}/pki/* && cp {wd}/srv/{sig}_srv.key {wd}/pki/server.key && cp {wd}/srv/{sig}_srv.crt {wd}/pki' \
           f'/server.crt '


def s_time(tls_server, sig, kex, time_exp, www=False):
    # Returns the command that will launch the s_time command for the nginx server
    ret = f"openssl/apps/openssl s_time -connect {tls_server} " \
           f"-CAfile CA/{sig}_CA.crt -curves {kex} -new -time {str(time_exp)}"
    if www:
        ret += " -www /index.html"
    return ret


def simulate(port, kex, sig, bw=8, delay="10ms", loss=0, cpu_usage=1.0, n_nodes=1, max_queue=14, time_exp=5, www=False):
    dumbbell = QuantumTopo(bw=bw, delay=delay, loss=loss, cpu_usage=cpu_usage, n_nodes=n_nodes, max_queue=max_queue)
    if cpu_usage == 1:
        network = Mininet(topo=dumbbell, link=TCLink)
    else:
        network = Mininet(topo=dumbbell, host=CPULimitedHost, link=TCLink, autoPinCpus=True)
        network.get("aServer").setCPUs(cores=1)
    network.start()

    appServer = network.get('aServer')

    # wd = str(appServer.cmd("pwd"))[:-2]

    # Setup the server
    addr = appServer.IP() + ":" + port
    nginx_setup(addr)
    os.system(prepare_PKI(sig))

    # Launch the server
    appServer.cmd("sudo " + wd + "/nginx/sbin/nginx -c " + wd + "/nginx/conf/nginx.conf &")
    # Tell nginx to use configuration from the file we just created

    time.sleep(1)  # Server might need some time to start

    # Test
    # We will launch all the clients in a non blocking way, except the last one that will be blocking.
    clients = []
    for i in range(n_nodes - 1):
        app_client = network.get('aClient_' + str(i))
        if i != n_nodes - 1:
            app_client.cmd(s_time(addr, sig, kex, time_exp, www) + " &")
    last_client = network.get('aClient_' + str(n_nodes - 1))
    ret = last_client.cmd(s_time(addr, sig, kex, time_exp, www))
    print(ret)

    appServer.cmd("sudo " + wd + "/nginx/sbin/nginx -s stop")
    network.stop()
    return parse_return(ret)


# simulate(port, kex, sig, bw=8, delay="10ms", loss=0, cpu_usage=1, n_nodes=1, max_queue=14) 
@click.command()
@click.option('--tls_port', default="4433", help="The port of the TLS server")
@click.option('--sig', default="dilithium2", help="Use this to specify a signature algorithm.")
@click.option('--kex', default="saber", help="Use this to specify a key exchange algorithm.")
@click.option('--bandwith', default="8", help="The bandwith of the 'switch <-> server' link.")
@click.option('--delay', default="10ms", help="The delay of the 'switch <-> server' link (in format : 10ms)")
@click.option('--loss', default="0", help="The loss percentage of the 'switch <-> server' link (from 0 to 1).")
@click.option('--cpu', default="1", help="The CPU usage percentage (from 0 to 1) allowed to the server.")
@click.option('--nodes', default="1", help="The number of clients.")
@click.option('--queue', default="14", help="The maximum size of the queue for the 'switch <-> server' link.")
@click.option('--time_exp', default="5", help="The time during which the experiment will be conducted.")
@click.option('--hybrid_sig', is_flag=True, help="To combine the signature algorithm with the corresponding EC.")
@click.option('--hybrid_kex', is_flag=True, help="To combine the key exchange algorithm with the corresponding EC.")
@click.option('--www', is_flag=True, help="To download the PQ Wikipedia webpage after each handshake.")
def main(tls_port, sig, kex, bandwith, delay, loss, cpu, nodes, queue, time_exp, hybrid_sig, hybrid_kex, www):
    if sig not in SupportedSigs:
        print("Signature algorithm not supported.")
    elif kex not in SupportedKex:
        print("Key Exchange algorithm not supported.")
    elif re.search("[0-9]+$", tls_port) is None:
        print("Non valid port value.")
    try:
        test = int(bandwith)
        test = int(loss)
        test = float(cpu)
        test = int(nodes)
        test = int(queue)
        test = int(time_exp)
    except ValueError:
        print("A numerical value has been wrongly passed")
    else:
        level_sig = LevelOfSecurity[sig]
        if level_sig == 0:
            print("Using a non post quantum signature algorithm.")
        elif level_sig == 1 or level_sig == 2:
            print("Using a post quantum signature algorithm, claimed level of security 1.")
            if hybrid_sig:
                curve = "p256"
                print("The signature will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                sig = curve + "_" + sig
        elif level_sig == 3:
            print("Using a post quantum signature algorithm, claimed level of security 3.")
            if hybrid_sig:
                curve = "p384"
                print("The signature will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                sig = curve + "_" + sig
        elif level_sig == 5:
            print("Using a post quantum signature algorithm, claimed level of security 5.")
            if hybrid_sig:
                curve = "p521"
                print("The signature will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                sig = curve + "_" + sig

        level_kex = LevelOfSecurity[kex]
        if level_kex == 0:
            print("Using a non post quantum key exchange algorithm.")
        elif level_kex == 1:
            print("Using a post quantum key exchange algorithm, claimed level of security 1.")
            if hybrid_kex:
                curve = "p256"
                print("The key exchange will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                kex = curve + "_" + kex
        elif level_kex == 3:
            print("Using a post quantum key exchange algorithm, claimed level of security 3.")
            if hybrid_kex:
                curve = "p384"
                print("The key exchange will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                kex = curve + "_" + kex
        elif level_kex == 5:
            print("Using a post quantum key exchange algorithm, claimed level of security 5.")
            if hybrid_kex:
                curve = "p521"
                print("The key exchange will be hybrid, with an Elliptic Curve" + curve + " of same level.")
                kex = curve + "_" + kex
        os.system("mn -c")
        ret = simulate(tls_port, kex, sig, int(bandwith), delay, int(loss), float(cpu), int(nodes), int(queue), time_exp, www)
        print(ret)


if __name__ == '__main__':
    main()
