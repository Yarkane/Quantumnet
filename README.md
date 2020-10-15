## Introduction

Mash is a web server that runs an OQS-OpenSSL distribution.
OQS-OpenSSL is a OpenSSL fork, maintained by the Open Quantum Safe team which goal is to make public the research and the evolutions in the Post-Quantum Security Algorithm field.

This development server aims to be a tool for anyone who wants to benchmark this TLS implementation.

## Installation

Run the following commands and it should be fine.

    git clone git@gitlab.epfl.ch:sjacquie/post-quantum-benchmark.git
    sudo ./install-prereqs-ubuntu.sh

## Run

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

## Supported algorithms

The supported algorithms are mainly taken from the NIST selection process (round 3).

Supported signature algorithms : 

    dilithium2, dilithium3, dilithium4
    falcon512, falcon1024
    rainbowlaclassic, rainbowVcclassic

Supported key exchange algorithms :
    lightsaber, saber, firesaber
    ntru\_hps2048509, ntru\_hps2048677, ntru\_hps4096821, ntru\_hrss701
    kyber512, kyber768, kyber1024, kyber90s512, kyber90s768, kyber90s1024
]

## TODO

--
