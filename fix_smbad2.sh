#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
sed '/global/a \ \ \ \ \ \ \ \ dns forwarder = 1.1.1.1' /etc/samba/smb.conf > /etc/samba/smb.conf.tmp
sed '/workgroup/a \ \ \ \ \ \ \ \ ntlm auth = yes' /etc/samba/smb.conf.tmp > /etc/samba/smb.conf.fix
cp /etc/samba/smb.conf.fix /etc/samba/smb.conf
