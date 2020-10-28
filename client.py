import click
import os
from requests_html import HTMLSession
import re

# The program does provide the user a command with multiple arguments.
# It has to test the TLS server setup by Mash.
# We get the algorithms to use by asking the flask server

SupportedSigs = [
    "dilithium2", "dilithium3", "dilithium4",
    "falcon512", "falcon1024",
    "rainbowlaclassic", "rainbowVcclassic","DSA"
]
SupportedKex = [
    "lightsaber", "saber", "firesaber",
    "ntru_hps2048509", "ntru_hps2048677", "ntru_hps4096821", "ntru_hrss701",
    "kyber512", "kyber768", "kyber1024", "kyber90s512", "kyber90s768", "kyber90s1024","X25549"
]

@click.command()
@click.option('--flask', default="127.0.0.1:5000", help="The address of the Flask server")
@click.option('--tls_server', default="127.0.0.1:4433", help="The address of the TLS server")
@click.option('--force_sig', default="", help="Use this to force a signature algorithm.")
@click.option('--force_kex', default="", help="Use this to force a key exchange algorithm.")
def main(flask, tls_server, force_sig, force_kex):
    if re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",flask) is None:
        print("The flask server address is not a valid ipv4 address")
        return

    if re.search("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$",tls_server) is None:
        print("The TLS server address is not a valid ipv4 address")
        return

    session = HTMLSession()
    if force_sig == "" or force_kex == "":
        r = session.get("http://" + flask + "/controller")
        if not r:
            print("Address unreachable, invalid or the server could not respond.")
            return
        sig = r.html.search("Signature algorithm used : {}<br>")[0]
        kex = r.html.search("Key-Exchange algorithm used : {}<br>")[0]
    if force_sig != "":
        if force_sig not in SupportedSigs:
            print("Unsupported signature algorithm.")
            return
        else:
            sig = force_sig
    if force_kex != "":
        if force_kex not in SupportedKex:
            print("Unsupported key exchange algorithm.")
            return
        else:
            kex = force_kex

    command = f"openssl/apps/openssl s_client -connect {tls_server} " \
              f"-groups {kex} -CAfile CA/{sig}_CA.crt"
    print("> " + command)
    os.system(command)
    return

if __name__ == "__main__":
    main()


