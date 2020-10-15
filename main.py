from flask import Flask, request, render_template
from multiprocessing import Pool
import os
import subprocess

# Global variables
IsAServerRunning = False
SignatureAlgorithmUsed = "dilithium2"  # Default value
KeyExchangeAlgorithmUsed = "saber"  # Default value
SupportedSigs = [
    "dilithium2", "dilithium3", "dilithium4",
    "falcon512", "falcon1024",
    "rainbowlaclassic", "rainbowVcclassic"
]
SupportedKex = [
    "lightsaber", "saber", "firesaber",
    "ntru_hps2048509", "ntru_hps2048677", "ntru_hps4096821", "ntru_hrss701",
    "kyber512", "kyber768", "kyber1024", "kyber90s512", "kyber90s768", "kyber90s1024",
]
process = subprocess.Popen


# Functions definition


def run_subprocess(command, working_dir='.'):
    running_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_dir
    )
    return running_process


def launch_openssl_server(sig):
    """
    Fork then launch the server in the subprocess.
    The function returns the new process, and updates the global IsAServerRunning value
    :param sig:
    :return: a subprocess object that we can terminate
    """
    global IsAServerRunning
    command = [
        'openssl/apps/openssl', 's_server', '-cert', 'srv/' + sig + '_srv.crt',
        '-key', 'srv/' + sig + '_srv.key', '-www', '-tls1_3'
    ]
    print("Launching server with ")
    print(" > " + " ".join(command))
    IsAServerRunning = True
    return run_subprocess(command)


def terminate_openssl_server(serverprocess):
    global IsAServerRunning
    IsAServerRunning = False
    serverprocess.terminate()
    return


# Flask server
app = Flask(__name__)


def launch(sig, kex):
    global SupportedSigs, SupportedKex, process, SignatureAlgorithmUsed, KeyExchangeAlgorithmUsed
    if sig in SupportedSigs and kex in SupportedKex:
        SignatureAlgorithmUsed = sig
        KeyExchangeAlgorithmUsed = kex
        process = launch_openssl_server(sig)
    response = app.make_response(render_template("index_running.html"))
    return response


def stop():
    global process
    terminate_openssl_server(process)
    response = app.make_response(render_template("index_idle.html"))
    return response


@app.route("/", methods=['GET'])
def start():
    global SignatureAlgorithmUsed, KeyExchangeAlgorithmUsed
    if IsAServerRunning:
        response = app.make_response(
            render_template("index_running.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed))
    else:
        response = app.make_response(
            render_template("index_idle.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed))

    return response


@app.route("/", methods=['POST'])
def run():
    global IsAServerRunning
    action = request.form.get("action")
    if action == "go" and IsAServerRunning is not True:
        sig = request.form.get("sig")
        kex = request.form.get("kex")
        return launch(sig, kex)
    elif action == "stop" and IsAServerRunning is True:
        return stop()
    else:
        pass


# Main
if __name__ == "__main__":
    app.run()
