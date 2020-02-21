#!/bin/bash

apt update
apt upgrade -y
apt install python3-pylxd -y

cat <<EOF | lxd init
no
yes
default
dir
no
yes
lxdbr0
auto
none
no
yes
no
EOF
