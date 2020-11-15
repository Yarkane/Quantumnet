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

export OPENSSL_ROOT_DIR=/opt/openssl
NGINX_VERSION=1.17.5

# build liboqs
cd liboqs
mkdir -p build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=${ROOT}/openssl/oqs ..
ninja && ninja install

# build OQS-OpenSSL
cd ../../openssl
./Configure no-shared linux-x86_64 -lm
make

# build nginx
wget nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && tar -zxvf nginx-${NGINX_VERSION}.tar.gz;
cd nginx-1.17.5
./configure --prefix=${ROOT}/nginx \
                --with-debug \
                --with-http_ssl_module --with-openssl=${ROOT}/openssl \
                --without-http_gzip_module \
                --with-cc-opt="-I ${ROOT}/openssl/oqs/include" \
                --with-ld-opt="-L ${ROOT}/openssl/oqs/lib";
sed -i 's/libcrypto.a/libcrypto.a -loqs/g' objs/Makefile;
sed -i 's/EVP_MD_CTX_create/EVP_MD_CTX_new/g; s/EVP_MD_CTX_destroy/EVP_MD_CTX_free/g' src/event/ngx_event_openssl.c;
make && make install;

cd ../

mkdir -p pki
mkdir -p logs

chmod 774 pki
chmod 774 pki/*
chmod 774 logs
chmod 774 logs/*
chmod 774 liboqs/*
chmod 774 openssl
chmod 774 openssl/*
chmod 774 nginx
chmod 774 nginx/*
