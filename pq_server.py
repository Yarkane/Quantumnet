from flask import Flask, request, render_template
import subprocess
import pq_server_simulation
import threading

# Global variables
process = subprocess.Popen
IsAServerRunning = False
SignatureAlgorithmUsed = "dilithium2"  # Default value
KeyExchangeAlgorithmUsed = "saber"  # Default value
NumberOfNodes = 2  # Default value
CpuUsage = 1  # Default value
Bandwith = 8  # Default value
Delay = "10ms"  # Default value
LossRate = 0  # Default value
QueueSize = 14  # Default value
TLSPort = 4433  # Default value
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


# Functions definition

def run_subprocess(command, working_dir='.'):
    running_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_dir
    )
    return running_process


class ExperimentThread:
    def __init__(self):
        self.output = ""
        self.finished = False

    def run(self, port, kex, sig, bw, delay, loss, cpu, nodes, queue):
        self.finished = False
        ret = pq_server_simulation.simulate(port, kex, sig, int(bw), delay, int(loss), int(cpu), int(nodes), int(queue))
        self.output = ret
        self.finished = True


def isExperimentDone(thrd):
    return thrd.finished


# Flask server
app = Flask(__name__)
thread = ExperimentThread()


def launch(sig, kex, nodes, cpu, bw, delay, loss, queue, port):
    global SupportedSigs, SupportedKex, process, SignatureAlgorithmUsed, KeyExchangeAlgorithmUsed
    if sig in SupportedSigs and kex in SupportedKex:
        SignatureAlgorithmUsed = sig
        KeyExchangeAlgorithmUsed = kex
        exp_thr = threading.Thread(target=thread.run, args=(port, kex, sig, bw, delay, loss, cpu, nodes, queue))
        exp_thr.daemon = True  # Daemonize thread
        exp_thr.start()  # Start the execution
        response = app.make_response(
            render_template("experiment_running.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed))
        return response


# GUI

@app.route("/", methods=['GET'])
def start():
    global SignatureAlgorithmUsed, KeyExchangeAlgorithmUsed, IsAServerRunning, NumberOfNodes, CpuUsage, \
        Bandwith, Delay, LossRate, QueueSize
    action = request.args.get("action")

    # We just finished an experiment and clicked on "ok"
    if action == "ok" and isExperimentDone(thread):
        IsAServerRunning = False
        thread.output = ""
        thread.finished = False
        response = app.make_response(
            render_template("experiment_idle.html"))
        return response

    # All the other cases :
    if IsAServerRunning and not isExperimentDone(thread):
        response = app.make_response(
            render_template("experiment_running.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed))
    elif isExperimentDone(thread):
        response = app.make_response(
            render_template("experiment_done.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed,
                            nodes=NumberOfNodes, cpu=CpuUsage, bw=Bandwith, delay=Delay, loss=LossRate,
                            queue=QueueSize, result=thread.output))
    else:
        response = app.make_response(
            render_template("experiment_idle.html"))

    return response


@app.route("/", methods=['POST'])
def run():
    global IsAServerRunning, NumberOfNodes, CpuUsage, Bandwith, Delay, LossRate, QueueSize, TLSPort, process
    action = request.form.get("action")
    if action == "go" and IsAServerRunning is not True:
        sig = request.form.get("sig")
        kex = request.form.get("kex")

        nodes = request.form.get("nodes")
        NumberOfNodes = nodes

        cpu = request.form.get("cpu")
        CpuUsage = cpu

        bw = request.form.get("bw")
        Bandwith = bw

        delay = request.form.get("delay")
        Delay = delay

        loss = request.form.get("loss")
        LossRate = loss

        queue = request.form.get("queue")
        QueueSize = queue

        port = request.form.get("port")
        TLSPort = port

        IsAServerRunning = True
        return launch(sig, kex, nodes, cpu, bw, delay, loss, queue, port)
    else:
        pass


# Python Client Link

@app.route("/controller", methods=['GET'])
def send():
    # We just return the algorithms we use.
    # This will be done by sending the experiment_running page.
    return render_template("experiment_running.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed)


# Main
if __name__ == "__main__":
    app.run()
