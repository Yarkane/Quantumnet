#!/bin/bash
set -ex
ROOT=$(pwd)

apt install build-essential \
            autoconf \
            automake \
            libtool \
            cmake \
            ninja-build \
            libssl-dev \
            libpcre3-dev \
            python3 \
            wget;

git clone --single-branch https://github.com/open-quantum-safe/liboqs
git clone --single-branch https://github.com/open-quantum-safe/openssl

# build liboqs
cd liboqs
mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=${ROOT}/openssl/oqs ..
ninja && ninja install

# build OQS-OpenSSL
cd ../../openssl
./Configure no-shared linux-x86_64 -lm
make

# Change perms
cd ../
chmod 774 liboqs
chmod 774 liboqs/*
chmod 774 openssl
chmod 774 openssl/*

# Install python dependencies
pip install requests-html
pip install click
pip install flask

