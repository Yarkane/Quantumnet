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

    python3 main.py

Then you should open your browser and go to the address 127.0.0.1:5000.

Everything will be there.

## TODO

A button to test the running server so we don't have to make the command ourselves.
