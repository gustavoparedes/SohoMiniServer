#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
sed  '/idmap_ldb/a \ \ \ \ \ \ \ \ ntlm auth = yes' /etc/samba/smb.conf > /etc/samba/smb.conf.fix
cp /etc/samba/smb.conf.fix /etc/samba/smb.conf
