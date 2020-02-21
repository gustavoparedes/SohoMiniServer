#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
cat /root/radclient.txt >> /etc/freeradius/3.0/clients.conf
