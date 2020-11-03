from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
import click
import time
import os
import re

wd = os.getcwd()
SupportedSigs = [
    "dilithium2", "dilithium3", "dilithium4",
    "falcon512", "falcon1024",
    "rainbowlaclassic", "rainbowVcclassic",
    "DSA"
]
SupportedKex = [
    "lightsaber", "saber", "firesaber",
    "ntru_hps2048509", "ntru_hps2048677", "ntru_hps4096821", "ntru_hrss701",
    "kyber512", "kyber768", "kyber1024", "kyber90s512", "kyber90s768", "kyber90s1024",
    "EC"
]


class DumbbellTopo(Topo):
    def build(self, bw=8, delay="10ms", loss=0, cpu_usage=1, n_nodes=1, max_queue=14):
        clients = []
        switch1 = self.addSwitch('switch1')
        switch2 = self.addSwitch('switch2')

        appServer = self.addHost('aServer', cls=CPULimitedHost, cpu=cpu_usage)
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
                    f"			root html;\n"
                    f"			index index.html index.htm;\n"
                    f"		}}\n"
                    f"	}}\n"
                    f"}}\n"
                    f"\n")
    filename = "nginx-conf/nginx.conf"
    with open(filename, 'w') as f:
        f.write(nginx_config)
        f.close()


def prepare_PKI(sig):
    # Returns the command that will prepare the PKI for the nginx server
    return f'rm -f {wd}/pki/* && cp {wd}/srv/{sig}_srv.key {wd}/pki/server.key && cp {wd}/srv/{sig}_srv.crt {wd}/pki' \
           f'/server.crt '


def s_time(tls_server, sig, kex):
    # Returns the command that will launch the s_time command for the nginx server
    return f"openssl/apps/openssl s_time -connect {tls_server} " \
           f"-CAfile CA/{sig}_CA.crt -curves {kex} -new -time 5"


def simulate(port, kex, sig, bw=8, delay="10ms", loss=0, cpu_usage=1.0, n_nodes=1, max_queue=14):
    dumbbell = DumbbellTopo(bw=bw, delay=delay, loss=loss, cpu_usage=cpu_usage, n_nodes=n_nodes, max_queue=max_queue)
    network = Mininet(topo=dumbbell, host=CPULimitedHost, link=TCLink, autoPinCpus=True)
    network.start()

    appServer = network.get('aServer')

    # wd = str(appServer.cmd("pwd"))[:-2]

    # Setup the server
    addr = appServer.IP() + ":" + port
    nginx_setup(addr)
    os.system(prepare_PKI(sig))

    # Launch the server
    appServer.cmd("sudo " + wd + "/nginx/sbin/nginx -c " + wd + "/nginx-conf/nginx.conf &")
    # Tell nginx to use configuration from the file we just created

    time.sleep(1)  # Server might need some time to start

    # Test
    # We will launch all the clients in a non blocking way, except the last one that will be blocking.
    clients = []
    for i in range(n_nodes - 1):
        app_client = network.get('aClient_' + str(i))
        if i != n_nodes - 1:
            app_client.cmd(s_time(addr, sig, kex) + " &")
    last_client = network.get('aClient_' + str(n_nodes - 1))
    ret = last_client.cmd(s_time(addr, sig, kex))
    print(ret)

    appServer.cmd("sudo nginx -s stop")
    network.stop()
    return ret


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
def main(tls_port, sig, kex, bandwith, delay, loss, cpu, nodes, queue):
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
    except ValueError:
        print("A numerical value has been wrongly passed")
    else:
        simulate(tls_port, kex, sig, int(bandwith), delay, int(loss), float(cpu), int(nodes), int(queue))


if __name__ == '__main__':
    main()
