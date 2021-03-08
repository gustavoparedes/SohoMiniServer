#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
sed '/authenticate {/a \ \ \ \ \ \ \ \ ntlm_auth' /etc/freeradius/3.0/sites-available/default > /etc/freeradius/3.0/sites-available/default.tmp
sed '/authenticate {/a \ \ \ \ \ \ \ \ ntlm_auth' /etc/freeradius/3.0/sites-available/inner-tunnel > /etc/freeradius/3.0/sites-available/inner-tunnel.tmp
cp /etc/freeradius/3.0/sites-available/default.tmp /etc/freeradius/3.0/sites-available/default
cp /etc/freeradius/3.0/sites-available/inner-tunnel.tmp /etc/freeradius/3.0/sites-available/inner-tunnel
echo "DEFAULT     Auth-Type = ntlm_auth" >> /etc/freeradius/3.0/users
