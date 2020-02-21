#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
cd /usr/local
tar xzvf softether-vpnserver*
cd vpnserver
printf '1\n1\n1\n'| make

