## Introduction

Quantumnet is a toolkit which contains multiple tools to test and benchmark the Post Quantum security algorithms.
It is mainly based on OQS-Openssl and Mininet.
OQS-OpenSSL is a OpenSSL fork, maintained by the Open Quantum Safe team which goal is to make public the research and the evolutions in the Post-Quantum Security Algorithm field.
Mininet is a tool available for certain linux distributions that allows to create nodes and switches, make them communicate and most importantly, apply constraints on the links between them.

This development server aims to be a tool for anyone who wants to benchmark this TLS implementation.

## Installation

First, run the Mininet installation process.
You can download the mininet.org VM, or, if you run an appropriate OS, enter these commands: 

    git clone git://github.com/mininet/mininet
    cd mininet
    git checkout -b 2.2.1 2.2.1
    cd ../
    sudo mininet/util/install.sh -a

To get the Quantumnet toolkit, type these commands nand it should be fine.

    git clone git@gitlab.epfl.ch:sjacquie/post-quantum-benchmark.git
    sudo ./install-prereqs-ubuntu.sh
    pip3 install requests-html click flask

## A minimal test server

The first tool that you can use to test if OQS-OpenSSL is working is the the minimal client-server experiment.

To launch the Flask server :

    python3 server.py

Then you should open your browser and go to the address 127.0.0.1:5000.
There, you will be able to setup the server with the selected Signature and Key-Exchange algorithm.

Once the TLS server is running, simply launch this command in another terminal :

    python3 client.py
    
Then, the client will get from the Flask server the algorithms you use, and test the connection with the TLS server.

Here is the list of the arguments you can pass to client.py :

    --flask : The IPv4 only address of the Flask server (default : 127.0.0.1:5000)
    --tls_server : The IPv4 only address of the TLS server (default : 127.0.0.1:4433)
    --force-sig : If you want to force a signature algorithm from the list
    --force-kex : If you want to force a key exchange algorithm from the list.

## A simple Mininet server

Then, you will want to test if the Mininet installation is working fine.
Quantumnet is provided with a simple "client-server" like Mininet workbench which will just create a nginx server and a client that will run a stime test from OpenSSL on the server.

Everything runs in this command :

    sudo python3 simple_nginx.py

There are also some arguments :

    --tls_port : The port that you want the node server to use (default : 4433)
    --sig : The Signature algorithm you want to benchmark (default : dilithium2)
    --kex : The Key Exchange algorithm you want to benchmark (default : saber)

## More complex Mininet server

If the simple Mininet server is working great, you can then start to customize your experiments using this command :
    
    sudo python3 pq_server_simulation.py

Using these arguments :

    --tls_port : Ther port that you want the node server to use (default : 4433)
    --sig : The Signature algorithm you want to benchmark (default : dilithium2)
    --kex : The Key Exchange algorithm you want to benchmark (default : saber)
    --bandwith : The bandwith of the switch - server link in Mbps (default : 8)
    --delay : The delay of the switch - server link, in the format ___ms (default : 10ms)
    --loss : The loss rate of the switch - server link, expressed in % (default : 0)
    --cpu : The CPU percentage allowed to the server (default : 1)
    --nodes : The number of clients (default : 1)
    --queue : The maximum size of the queue for the switch - server link (default : 14)
    --time_exp : The time during which the experiment will be conducted (default : 5)
    --hybrid_sig : When set, this flag combine the signature algorithm with the corresponding EC via traditional method
    --hybrid_kex : When set, this flag combine the key exchange algorithm with the corresponding EC via traditional method
    --www : When set, this flag makes the s_time command download a webpage at each Handshake. The webpage is a wikipedia page about PQ algorithms.

To help you with this, you can always use the **Web Interface** included with Quantumnet. To launch the Flask server that will handle your experiments, please use :

    sudo python3 pq_server.py

Then open a light web browser to the URL :

    http://localhost:5000/

Then enjoy !

## Supported OQS-algorithms

The supported algorithms are mainly taken from the NIST selection process (round 3).

Supported signature algorithms : 

    dilithium2, dilithium3, dilithium4
    falcon512, falcon1024
    rainbowlaclassic, rainbowVcclassic
    picnic3l1, picnic3l3, picnic3l5

Supported key exchange algorithms :

    lightsaber, saber, firesaber
    ntru_hps2048509, ntru_hps2048677, ntru_hps4096821, ntru_hrss701
    kyber512, kyber768, kyber1024, kyber90s512, kyber90s768, kyber90s1024

# Further documentation is available in the Wiki !