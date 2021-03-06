import time

from flask import Flask, request, render_template, jsonify
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
Time = 5  # Default value
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
    "RSA"
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
    "RSA": 0
}

# Functions definition

def run_subprocess(command, working_dir='.'):
    running_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=working_dir
    )
    return running_process


def parse_return(ret):
    return f'The experiment ran for {ret["nb_seconds"]} seconds. <br>' \
           f'<br>' \
           f'REAL RESULTS : {ret["nb_realsecs"]} real seconds, {ret["nb_connections_realsecs"]} connections, ' \
           f'{ret["bytes_read_per_conn"]} bytes read per connection.<br>' \
           f'<br>' \
           f'SIMULATED RESULTS : {ret["nb_unrealsecs"]} simulated seconds, {ret["nb_connections_unrealsecs"]} connections, ' \
           f'{ret["nb_conn_user_secs"]} connections per user seconds, {ret["bytes_read"]} bytes read.'


class ExperimentThread:
    def __init__(self):
        self.output = ""
        self.finished = False

    def run(self, port, kex, sig, bw, delay, loss, cpu, nodes, queue, time):
        self.finished = False
        ret = pq_server_simulation.simulate(port, kex, sig, float(bw), delay, float(loss), float(cpu), int(nodes), int(queue), int(time))
        self.output = ret
        self.finished = True


def isExperimentDone(thrd):
    return thrd.finished


# Flask server
app = Flask(__name__)
thread = ExperimentThread()


def launch(sig, kex, nodes, cpu, bw, delay, loss, queue, port, time):
    global SupportedSigs, SupportedKex, process, SignatureAlgorithmUsed, KeyExchangeAlgorithmUsed
    SignatureAlgorithmUsed = sig
    KeyExchangeAlgorithmUsed = kex
    exp_thr = threading.Thread(target=thread.run, args=(port, kex, sig, bw, delay, loss, cpu, nodes, queue, time))
    print("before thread")
    exp_thr.daemon = True  # Daemonize thread
    exp_thr.start()  # Start the execution
    print("after thread")
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
                            queue=QueueSize, result=parse_return(thread.output)))
    else:
        response = app.make_response(
            render_template("experiment_idle.html"))

    return response


@app.route("/", methods=['POST'])
def run():
    global IsAServerRunning, NumberOfNodes, CpuUsage, Bandwith, Delay, LossRate, QueueSize, TLSPort, process, Time
    action = request.form.get("action")
    if action == "go" and IsAServerRunning is not True:
        sig = request.form.get("sig")
        kex = request.form.get("kex")
        if sig in SupportedSigs and kex in SupportedKex:
            hybrid_sig = request.form.get("hybrid_sig")
            if hybrid_sig:
                level = LevelOfSecurity[sig]
                if level == 1 or level == 2:
                    sig = "p256_" + sig
                elif level == 3:
                    sig = "p384_" + sig
                elif level == 5:
                    sig = "p521_" + sig

            hybrid_kex = request.form.get("hybrid_kex")
            if hybrid_kex:
                level = LevelOfSecurity[kex]
                if level == 1:
                    kex = "p256_" + kex
                elif level == 3:
                    kex = "p384_" + kex
                elif level == 5:
                    kex = "p521_" + kex

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

            time = request.form.get("time")
            Time = time

            IsAServerRunning = True
            print("running")
            print("signature : ", sig)
            print("key exchange : ", kex)
            return launch(sig, kex, nodes, cpu, bw, delay, loss, queue, port, time)
    else:
        pass


# Python Client Link

@app.route("/controller", methods=['GET'])
def get_args():
    # We just return the algorithms we use.
    # This will be done by sending the experiment_running page.
    return render_template("experiment_running.html", kex=KeyExchangeAlgorithmUsed, sig=SignatureAlgorithmUsed, time=str(Time))


@app.route("/controller", methods=['POST'])
def send_args():
    global IsAServerRunning, NumberOfNodes, CpuUsage, Bandwith, Delay, LossRate, QueueSize, TLSPort, process, Time
    # We launch the experiment via a POST JSON request.
    j = request.get_json()
    if j is None:
        return "No JSON", 500
    if IsAServerRunning is not True:
        print(j)
        sig = j["sig"]
        kex = j["kex"]
        if sig in SupportedSigs and kex in SupportedKex:
            hybrid_sig = j["hybrid_sig"]
            if hybrid_sig:
                level = LevelOfSecurity[sig]
                if level == 1 or level == 2:
                    sig = "p256_" + sig
                elif level == 3:
                    sig = "p384_" + sig
                elif level == 5:
                    sig = "p521_" + sig

            hybrid_kex = j["hybrid_kex"]
            if hybrid_kex:
                level = LevelOfSecurity[kex]
                if level == 1:
                    kex = "p256_" + kex
                elif level == 3:
                    kex = "p384_" + kex
                elif level == 5:
                    kex = "p521_" + kex

            nodes = j["nodes"]
            NumberOfNodes = nodes

            cpu = j["cpu"]
            CpuUsage = cpu

            bw = j["bw"]
            Bandwith = bw

            delay = j["delay"]
            Delay = delay

            loss = j["loss"]
            LossRate = loss

            queue = j["queue"]
            QueueSize = queue

            port = j["port"]
            TLSPort = port

            time = j["time"]
            Time = time

            IsAServerRunning = True
            print("running")
            print("signature : ", sig)
            print("key exchange : ", kex)
            return launch(sig, kex, nodes, cpu, bw, delay, loss, queue, port, time)
        else:
            return "server already running", 500


@app.route("/result", methods=['GET'])
def res():
    global IsAServerRunning
    # We just return the last results
    while not isExperimentDone(thread):
        time.sleep(1)
    return jsonify(thread.output)


# Main
if __name__ == "__main__":
    app.run()
