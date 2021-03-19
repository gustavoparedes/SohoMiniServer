#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import platform
import ipaddress
from pylxd import Client


fw_ip = "1"
ad1_ip = "2"
ad2_ip = "3"
fs_ip = "4"
vpn_ip = "5"
fw_name = "fw"
ad1_name = "ad1"
ad2_name = "ad2"
fs_name = "fs"
vpn_name = "vpn"

def wait(t):
    for i in range(t,-1,-1):
        print ("\033[A                             \033[A")
        print(i)
        time.sleep(1)
    print ("\033[A                             \033[A")
    
def get_domain_name():
    
    global domain
    global realm
    
    control = 0
    while control == 0:
        realm = input("Digite el nombre de dominio: \n")
        domain = realm.split(".")
        if (len(domain)) > 3:
            print("El dombre de dominio debe ser: ejemplo.com")
            print("o : subdominio.ejemplo.com")
        elif (len(domain)) < 2:
            print("El dombre de dominio debe ser: ejemplo.com")
            print("o : subdominio.ejemplo.com")
        elif "" in domain:
            print("El dombre de dominio debe ser: ejemplo.com")
            print("o : subdominio.ejemplo.com")
        else:
            #verificar si meta dominio tiene numeros
            #if len(domain) == 2 and has domain:
                
            
            if len(domain[0]) > 15:
                print("El nombre ", domain[0], "tiene", len(domain[0]), "caracteres,  maximo 15")
            else:
                #print("Ok, el nombre de dominio sera: ", domain[0])
                #print("El nombre de realm (ambito) sera: ", realm)
                control = 1

def get_lan_addr():
    
    global lan_addr
    global lan_netmask
    global lan_prefix
    global lan_total_addr
    global lan_bcast
    
    control = 0
    while control == 0: 
        try:
            lan = input("Digite la direccion de la red LAN en formato CIRD (max prefijo de red /26), p.e 10.0.0.0/16: ")
            ipaddress.ip_network(lan)
            if ipaddress.ip_network(lan).prefixlen > 26:
                print("Formato incorrecto o prefijo de red LAN incorrecto ")
                print("La direccion de la red LAN debe estar en formato CIRD, p.e 10.0.0.0/16 ")
                print("El prefijo de red es: ", ipaddress.ip_network(lan).prefixlen, " el prefijo de red maximo es de 26 ")
                
            else:
                control = 1
        except ValueError:
            print("Direccion de red IP no valida ")
    
    lan_addr = ipaddress.ip_network(lan).network_address
    lan_netmask = ipaddress.ip_network(lan).netmask
    lan_prefix = ipaddress.ip_network(lan).prefixlen
    lan_total_addr = ipaddress.ip_network(lan).num_addresses
    lan_bcast = ipaddress.ip_network(lan).broadcast_address
    
    

def get_wan_addr():
    
    global wan_ip
    global wan_mask
    global wan_gw
    
    type_wan_ip = input("Se usara una direccion WAN asignada de forma automatica (dhcp)? (s/n)")
    if type_wan_ip == "n":
        control = 0
        while control == 0: 
            try:
                wan_ip = input("Digite la direccion ip WAN: ")
                ipaddress.ip_address(wan_ip)
                print("Ip valida, y su tipo es: ", type(wan_ip))
                control = 1
            except ValueError:
                print("IP no valida")
                
        control = 0
        while control == 0:
            wan_mask = input("Digite la mascara de red:" )
            try:
                wan_mask = int(wan_mask)
                print("Es un numero")
                if wan_mask < 8 or wan_mask > 30:
                    print("La mascara debe ser un numero entero entre 8 y 30")
                else:
                    ip_eval = str(wan_ip) + "/" + str(wan_mask)
                    try:
                        ipaddress.ip_network(ip_eval)
                        print("No es una direccion ip, es una direccion de red ip")
                    except ValueError:
                        print("Direccion ip WAN valida")
                        control = 1
            except ValueError:
                    print("No numero La mascara debe ser un numero entero entre 8 y 30")
        
        control = 0
        while control == 0: 
            try:
                wan_gw = input("Digite la direccion ip de la puerta de enlace (gateway): ")
                ipaddress.ip_address(wan_gw)
                print("Ip valida, y su tipo es: ", type(wan_gw))
                ip_eval = str(wan_gw) + "/" + str(wan_mask)
                try:
                    ipaddress.ip_network(ip_eval)
                    print("La direccion gateway digitada es una direccion de red ip")
                except ValueError:
                    print("Direccion Gateway WAN valida")
                    control = 1
            except ValueError:
                print("IP no valida")      
    
    else:
        wan_ip = "dhcp"
    
      

def get_nics():
    
    global wan_nic
    global lan_nic
    
    ifaces = os.listdir('/sys/class/net/')
    print("Seleccione las interfaces de red WAN y LAN")
    print("Interfaces de red disponibles: ")
    print(*ifaces, sep="\t")
    control = 0
    while control == 0:
        wan_nic = input("Digite interfaz de red WAN: ")
        if wan_nic not in ifaces:
            print("Interfaz de red incorrecta")
        else:
            print("Ok, la WAN usara la interfaz de red: ", wan_nic)
            control = 1
    
    control = 0        
    while control == 0:
        lan_nic = input("Digite interfaz de red LAN: ")
        if (lan_nic not in ifaces) or (lan_nic == wan_nic):
            print("Interfaz de red inexistente o igual a la WAN")
        else:
            print("Ok, la LAN usara la interfaz de red: ", lan_nic)
            control = 1
            
def summary_report():
    
    print("==" * 100 )
    print("Informacion de Dominio: \n")
    print("-----> Nombre de dominio sera: ", domain[0])
    print("-----> Realm (ambito) sera: ", realm, "\n")
    print("Informacion de direccionamiento LAN: \n")
    print("-----> Direccion LAN: ", lan_addr)
    print("-----> Mascara de red: ", lan_netmask, "prefijo", lan_prefix)
    print("-----> Total direcciones para esta red: ", lan_total_addr)
    print("-----> Direccion de bcast: ", lan_bcast, "\n")
    print("Informacion de direccionamiento WAN: \n")
    if wan_ip == "dhcp":
        print("EL direccionamiento WAN sera tomado usando DHCP: ", "\n")
    else:
        print("-----> Direccion WAN: ", wan_ip)
        print("-----> Mascara de red para la direccion WAN: ", wan_mask)
        print("-----> Gateway o puerta de enlace: ", wan_gw, "\n")
    print("Informacion de interfaces de red: \n")
    print("-----> La interfaz WAN sera: ", wan_nic)
    print("-----> La interfaz LAN sera: ", lan_nic)
    
    
def set_arch():
    
    global tmin
    global tmed
    global tmax
    global rb_hw
    
    rb_hw = False
    rb_pi3 = "Raspberry Pi 3"
    rb_pi4 = "Raspberry Pi 4"
    
    if platform.machine() == "x86_64":
        tmin = 5
        tmed = 15
        tmax = 30
           
    
    if platform.machine() == "armv7l":
        try:
            rb = subprocess.check_output(["cat", "/sys/firmware/devicetree/base/model"])
            rb = str(rb)
        except subprocess.CalledProcessError as e:
            print("No Raspberry Pi")
            rb_hw = False
        
        if rb.find(rb_pi4) > 0:
            print("******************** Detectado Raspberry Pi 4 ************************* \n")
            rb_hw = True
            tmin = 5
            tmed = 10
            tmax = 15
            subprocess.run(["apt", "install", "hostapd", "-y"])
            hostap_default()
            hostap_conf()
            
        if rb.find(rb_pi3) > 0:
            print("******************** Detectado Raspberry Pi 3 ************************* \n")
            rb_hw = True
            tmin = 15
            tmed = 30
            tmax = 45
            subprocess.run(["apt", "install", "hostapd", "-y"])
            hostap_default()
            hostap_conf()            
                        
def provision():
   
    
    client = Client()
    plantillas = ['fw', 'samba', 'vpn']
    for i in plantillas:
        if platform.machine() == "x86_64":
            config = {'name': i, 'source': {'type': 'image', "mode": "pull", "server":
            "https://cloud-images.ubuntu.com/daily", "protocol": "simplestreams", 'alias': 'focal/amd64'},
            'profiles': ['default'] }        
            
            
        if platform.machine() == "armv7l":
            config = {'name': i, 'source': {'type': 'image', "mode": "pull", "server":
            "https://cloud-images.ubuntu.com/daily", "protocol": "simplestreams", 'alias': 'focal/armhf'},
            'profiles': ['default'] }                   
        print("Creando maquina: ", i)
        a = client.containers.create(config, wait=True)
        print("Encendiendo maquina: ", i + "\n")
        a.start()
    
    
    a = client.containers.all()
    l = len(a)
    print("Numero de maquinas a provisionar: ",l)
    print("Esperando ",tmax , " segundos que levanten la configuracion inicial de red: \n")
    wait(tmax)
    
    
    for x in range(len(a)):
        print("Provisionando plnatilla de contenedor", a[x].name)
        if a[x].name == "fw":
            print("Buscando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'update'])
            print(so)
            print("Aplicando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'upgrade', '-y'])
            print(so)
            print("Instalando paquetes sobre: ", a[x].name)
            sw = ['acl', 'attr', 'samba', 'samba-dsdb-modules', 'samba-vfs-modules', 'winbind', 'libpam-winbind', 'libnss-winbind', 'libpam-krb5', 'krb5-config', 'krb5-user', 'smbclient', 'isc-dhcp-server']
            for i in sw:
                print("Instalando: ", i, " sobre ", a[x].name)
                e, so, se = a[x].execute(['apt-get', 'install', i , '-yq'], environment={'DEBIAN_FRONTEND': 'noninteractive'})
                if e == 0:
                    print("Instalacion OK")
                else:
                    print("La instalacion fallo, revise su conexion a internet, ejecute CleanUP.py y repita el proceso")
                    sys.exit()
                
            
            subprocess.run(['lxc',  'exec', 'fw', '--', 'bash', '-c', 'apt-get install freeradius -y'])
            a[x].stop()
            time.sleep(5)
            subprocess.run(["lxc", "publish", a[x].name, "--alias", a[x].name])
            print("Imagen de ", a[x].name + " se genero")
            print("Borrando contenedor: ", a[x].name, "\n")
            a[x].delete()
            wait(tmed)


        if a[x].name == "samba":
            print("Buscando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'update'])
            print(so)
            print("Aplicando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'upgrade', '-y'])
            print(so)
            print("Instalando paquetes sobre: ", a[x].name)
            sw = ['acl', 'attr', 'samba', 'samba-dsdb-modules', 'samba-vfs-modules', 'winbind', 'libpam-winbind', 'libnss-winbind', 'libpam-krb5', 'krb5-config', 'krb5-user', 'smbclient']
            for i in sw:
                print("Instalando: ", i, " sobre ", a[x].name)
                e, so, se = a[x].execute(['apt-get', 'install', i , '-yq'], environment={'DEBIAN_FRONTEND': 'noninteractive'})
                if e == 0:
                    print("Instalacion OK")
                else:
                    print("La instalacion fallo, revise su conexion a internet, ejecute CleanUP.py y repita el proceso")
                    sys.exit()
            print("Generando imagen de: ",a[x].name)
            a[x].stop()
            time.sleep(5)
            subprocess.run(["lxc", "publish", a[x].name, "--alias", a[x].name])
            print("Imagen de ", a[x].name + " se genero")
            print("Borrando contenedor: ", a[x].name, "\n")
            a[x].delete()
            wait(tmed)

        if a[x].name == "vpn":
            print("Buscando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'update'])
            print(so)
            print("Aplicando actualizaciones sobre: ", a[x].name)
            e, so, se = a[x].execute(['apt-get', 'upgrade', '-y'])
            print(so)
            print("Instalando paquetes sobre: ", a[x].name)
            sw = ['build-essential']
            for i in sw:
                print("Instalando: ", i, " sobre ", a[x].name)
                e, so, se = a[x].execute(['apt-get', 'install', i , '-yq'], environment={'DEBIAN_FRONTEND': 'noninteractive'})
                if e == 0:
                    print("Instalacion OK")
                else:
                    print("La instalacion fallo, revise su conexion a internet, ejecute CleanUP.py y repita el proceso")
                    sys.exit()
            print("Descargando VPN Server.....: \n")
            if platform.machine() == "x86_64":
                subprocess.run(['lxc',  'exec', 'vpn', '--', 'bash', '-c', 'wget https://www.softether-download.com/files/softether/v4.34-9745-rtm-2020.04.05-tree/Linux/SoftEther_VPN_Server/64bit_-_Intel_x64_or_AMD64/softether-vpnserver-v4.34-9745-rtm-2020.04.05-linux-x64-64bit.tar.gz -O /usr/local/softether-vpnserver.tar.gz'])
            if platform.machine() == "armv7l":
                subprocess.run(['lxc',  'exec', 'vpn', '--', 'bash', '-c', 'wget https://www.softether-download.com/files/softether/v4.34-9745-rtm-2020.04.05-tree/Linux/SoftEther_VPN_Server/32bit_-_ARM_EABI/softether-vpnserver-v4.34-9745-rtm-2020.04.05-linux-arm_eabi-32bit.tar.gz -O /usr/local/softether-vpnserver.tar.gz'])
            print("Generando imagen de: ",a[x].name)
            a[x].stop()
            time.sleep(5)
            subprocess.run(["lxc", "publish", a[x].name, "--alias", a[x].name])
            print("Imagen de ", a[x].name + " se genero")
            print("Borrando contenedor: ", a[x].name, "\n")
            a[x].delete()
            wait(tmed)
    

def netplan_raspberry():
        
    lanbcast = str(lan_bcast)
    tmp = lanbcast.split(".")
    lanaddr = str(lan_addr)
    tmp2 = lanaddr.split(".")
    last_lan_ip = int(tmp[3]) - 1
    filename = "50-cloud-init.yaml"
    l1 = "network:"
    l2 = " version: 2"
    l3 = " ethernets:"
    l4 = "  " + lan_nic + ":"
    l5 = "   dhcp4: no"
    #l6 = "   match:"
    #l7 = "    macaddress: " + mac0
    #l8 = "   set-name: eth0"
    l9 = " bridges:"
    l10 = "  LAN:"
    l11 = "   addresses: " + "[" + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + str(last_lan_ip) + "/" + str(lan_prefix) + "]"
    l12 = "   gateway4: " + tmp2[0] + "." + tmp2[1] + "." + tmp2[2] + "." + fw_ip
    l13 = "   nameservers:"
    l14 = "    search: " + "[" + realm + "]"
    l15 = "    addresses: " + "[" + tmp2[0] + "." + tmp2[1] + "." + tmp2[2] + "." + ad1_ip + "," + tmp2[0] + "." + tmp2[1] + "." + tmp2[2] + "." + ad2_ip + "]"
    l16 = "   interfaces:"
    l17 = "    - " + lan_nic
    l18 = " ethernets:"
    l19 = "  " + wan_nic + ":"
    l20 = "   dhcp4: no"
    #l21 = "   match:"
    #l22 = "    macaddress: " + mac1
    #l23 = "   set-name: eth1"
    l24 = " bridges:"
    l25 = "  WAN:"
    l26 = "   interfaces:"
    l27 = "    - " + wan_nic
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        #out.write(l6 + '\n')
        #out.write(l7 + '\n')
        #out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.write(l13 + '\n')
        out.write(l14 + '\n')
        out.write(l15 + '\n')
        out.write(l16 + '\n')
        out.write(l17 + '\n')
        out.write(l18 + '\n')
        out.write(l19 + '\n')
        out.write(l20 + '\n')
        #out.write(l21 + '\n')
        #out.write(l22 + '\n')
        #out.write(l23 + '\n')
        out.write(l24 + '\n')
        out.write(l25 + '\n')
        out.write(l26 + '\n')
        out.write(l27 + '\n')
        out.close()
        subprocess.run(["rm", "/etc/netplan/50-cloud-init.yaml"])
        subprocess.run(["cp", "50-cloud-init.yaml", "/etc/netplan/50-cloud-init.yaml"])
        subprocess.run(["netplan", "apply"])


def profiles():
    client = Client()
    profile = client.profiles.create("WAN", config = {}, devices={"eth0": {"name": "eth0", "nictype": 
              "bridged", "parent": "LAN", "type": "nic"}, "eth1": {"name": "eth1", "nictype": "bridged", 
              "parent": "WAN", "type": "nic"}, "root": {"path": "/", "pool": "default", "type": "disk"}})
    
    profile = client.profiles.create("AD", config = {"security.privileged": "True"}, devices={"eth0": {"name": "eth0", "nictype": 
              "bridged", "parent": "LAN", "type": "nic"}, "root": {"path": "/", "pool": "default", "type": "disk"}})
    
    profile = client.profiles.create("LAN", config = {}, devices={"eth0": {"name": "eth0", "nictype": 
              "bridged", "parent": "LAN", "type": "nic"}, "root": {"path": "/", "pool": "default", "type": "disk"}})


def resolv(machine_name):
    
    lanaddr = str(lan_addr)
    tmp = lanaddr.split(".")    
    filename = "files" + "/" + realm + "-" + machine_name + "-" + "resolv.conf"
    l1 = "search " + realm
    if machine_name == "ad1":
        l2 = "nameserver " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad1_ip
    elif machine_name == "ad2":
        l2 = "nameserver " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad2_ip
    else:
        l2 = "nameserver " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad1_ip
        l3 = "nameserver " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad2_ip
        
    if machine_name == "ad1" or machine_name == "ad2":
        with open(filename, "w+") as out:
            out.write(l1 + '\n')
            out.write(l2 + '\n') 
            out.close()
    if machine_name == "fw" or machine_name == "fs" or machine_name == "vpn":
        with open(filename, "w+") as out:
            out.write(l1 + '\n')
            out.write(l2 + '\n')
            out.write(l3 + '\n')
            out.close()        


def hosts(machine_ip, machine_name):
    
    lanaddr = str(lan_addr)
    tmp = lanaddr.split(".")    
    filename = "files" + "/" + realm + "-" + machine_name + "-" + "hosts"
    l1 = "127.0.0.1 localhost"
    l2 =  tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + machine_ip + " " + machine_name + "." + realm + " " + machine_name 
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.close()

def netplan(machine_ip, machine_name):
    
    lanaddr = str(lan_addr)
    tmp = lanaddr.split(".")    
    filename = "files" + "/" + realm + "-" + machine_name + "-"+ "50-cloud-init.yaml"
    l1 = "network:"
    l2 = " version: 2"
    l3 = " ethernets:"
    l4 = "  " + "eth0" + ":"
    l5 = "   addresses:"
    l6 = "   " + "-" + " " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + machine_ip + "/" + str(lan_prefix)
    l7 = "   gateway4:" + " " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + fw_ip
    l8 = "   nameservers:"
    l9 = "    search:" + " " + "[" + realm + "]" 
    l10 = "    addresses:" + " " + "[" + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad1_ip + "," + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad2_ip + "]"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.close()


def netplanfw(machine_ip, machine_name):
    
    lanaddr = str(lan_addr)
    tmp = lanaddr.split(".")    
    filename = "files" + "/" + realm + "-" + machine_name + "-"+ "50-cloud-init.yaml"     
    l1 = "network:"
    l2 = " version: 2"
    l3 = " ethernets:"
    l4 = "  " + "eth0" + ":"
    l5 = "   addresses:"
    l6 = "    " + "-" + " " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + machine_ip + "/" + str(lan_prefix)
    l7 = "   nameservers:"
    l8 = "    search:" + " " + "[" + realm + "]" 
    l9 = "    addresses:" + " " + "[" + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad1_ip + "," + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad2_ip + "]"
    l10 = " ethernets:"
    l11 = "  " + "eth1" + ":"
    if wan_ip != "dhcp":
        l12 = "   addresses:"
        l13 = "    " + "-" + " " + str(wan_ip) + "/" + str(lan_prefix)
        l14 = "   gateway4:" + " " + str(wan_gw)
    if wan_ip == "dhcp":
        l12 = "   dhcp4: true"
        l13 = "   dhcp4-overrides:"
        l14 = "    use-dns: false"
    
    if wan_ip != "dhcp":
        with open(filename, "w+") as out:
            out.write(l1 + '\n')
            out.write(l2 + '\n')
            out.write(l3 + '\n')
            out.write(l4 + '\n')
            out.write(l5 + '\n')
            out.write(l6 + '\n')
            out.write(l7 + '\n')
            out.write(l8 + '\n')
            out.write(l9 + '\n')
            out.write(l10 + '\n')
            out.write(l11 + '\n')
            out.write(l12 + '\n')
            out.write(l13 + '\n')
            out.write(l14 + '\n')
            out.close() 
            
    if wan_ip == "dhcp":
        with open(filename, "w+") as out:
            out.write(l1 + '\n')
            out.write(l2 + '\n')
            out.write(l3 + '\n')
            out.write(l4 + '\n')
            out.write(l5 + '\n')
            out.write(l6 + '\n')
            out.write(l7 + '\n')
            out.write(l8 + '\n')
            out.write(l9 + '\n')
            out.write(l10 + '\n')
            out.write(l11 + '\n')
            out.write(l12 + '\n')
            out.write(l13 + '\n')
            out.write(l14 + '\n')
            out.close()


def samba_inst_ad1(machine_name):
    
    filename = "files" + "/" + realm + "-" + machine_name + "-"+ "samba.sh"
    r = realm.split(".")
    l1 = "#!/bin/bash"
    l2 = "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
    l3 = "systemctl stop smbd nmbd winbind systemd-resolved"
    l4 = "killall nmbd winbindd smbd"
    l5 = "rm /etc/krb5.conf"
    l6 = "rm /etc/samba/smb.conf"
    l7 = "echo \"nameserver 1.1.1.1\" > /etc/resolv.conf"
    l8 = "samba-tool domain provision --server-role=dc  --use-rfc2307 --dns-backend=SAMBA_INTERNAL  --realm=" + realm + " " + "--domain=" + r[0] + " " + "--adminpass=Abcd1234"
    l9 = "cp /var/lib/samba/private/krb5.conf /etc/"
    l10 = "systemctl stop smbd nmbd winbind systemd-resolved"
    l11 = "systemctl disable smbd nmbd winbind systemd-resolved"
    l12 = "systemctl unmask samba-ad-dc"
    l13 = "rm /etc/resolv.conf"
    l14 = "systemctl enable samba-ad-dc"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.write(l13 + '\n')
        out.write(l14 + '\n')
        out.close()    


def samba_inst_ad2(machine_name):
    filename = "files" + "/" + realm + "-" + machine_name + "-"+ "samba.sh"
    r = realm.split(".")
    l1 = "#!/bin/bash"
    l2 = "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
    l3 = "systemctl stop smbd nmbd winbind systemd-resolved"
    l4 = "killall nmbd winbindd smbd"
    l5 = "rm /etc/samba/smb.conf"    
    l6 = "samba-tool domain join" + " " + realm + " " + "DC -U\"" + r[0] + "\\administrator\" --password=Abcd1234"
    l7 = "systemctl stop smbd nmbd winbind systemd-resolved"
    l8 = "systemctl disable smbd nmbd winbind systemd-resolved"
    l9 = "systemctl unmask samba-ad-dc"
    l10 = "systemctl enable samba-ad-dc"
    
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.close()


def samba_ws_file():
    filename = "files" + "/" + realm + "-" + "sambawsfile"
    tmp = realm.upper()
    r = tmp.split(".")
    l1 = "security = ADS"
    l2 = "workgroup =" + " " + r[0]
    l3 = "realm =" + " " + realm.upper()
    l4 = ""
    l5 = "log file = /var/log/samba/%m.log"
    l6 = "log level = 1"
    l7 = ""
    l8 = "idmap config * : backend = tdb"
    l9 = "idmap config * : range = 3000-7999"
    l10 = ""
    l11 = "idmap config" + " " + r[0] + " " + ": backend = rid"
    l12 = "idmap config" + " " +  r[0] + " " + ": range = 10000-999999"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.close()
def samba_fs_setup():
    filename = "files" + "/" + realm + "-" + "samba_fs_setup"
    r = (realm.upper()).split(".")
    U = "Users"
    l1 = "echo \"Abcd1234\" | net rpc rights grant \"" + r[0] + "\Domain Admins\" SeDiskOperatorPrivilege -U \"" + r[0] + "\\administrator\""
    l2 = "mkdir /Users"
    l3 = "sleep 15"
    l4 = "chown " + r[0] + "\\\\" + "administrator" + ":" + r[0] + "\\\\" + "domain\ users" + " /Users"
    l5 = "chmod 2750 /Users"
    l6 = "echo \"vfs objects = acl_xattr\" >> /etc/samba/smb.conf"
    l7 = "echo \"map acl inherit = yes\"  >> /etc/samba/smb.conf"
    l8 = "echo [Users] >> /etc/samba/smb.conf"
    l9 = "echo \"path = /Users\" >> /etc/samba/smb.conf"
    l10 = "echo \"read only = no\" >> /etc/samba/smb.conf"
    l11 = "echo \"force create mode = 0600\" >> /etc/samba/smb.conf"
    l12 = "echo \"force directory mode = 0700\" >> /etc/samba/smb.conf"
    
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.close()


def krb5():
    filename = "files" + "/" + realm + "-" + "krb5"
    r = realm.upper()
    l1 = "[" + "libdefaults" + "]"
    l2 = "    dns_lookup_realm = false"
    l3 = "    dns_lookup_kdc = true"
    l4 = "    default_realm = " + r
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.close()

def nsswitch():
    
    filename = "files" + "/" + realm + "-" + "nsswitch"
    l1 = "passwd:         compat winbind"
    l2 = "group:          compat winbind"
    l3 = "shadow:         compat"
    l4 = "gshadow:        files"
    l5 = "hosts:          files dns"
    l6 = "networks:       files"
    l7 = "protocols:      db files"
    l8 = "services:       db files"
    l9 = "ethers:         db files"
    l10 = "rpc:            db files"
    l11 = "netgroup:       nis"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.close()


def dhcpd(machine_name):
    
    filename = "files" + "/" + realm + "-" + "dhcpd"
    l = list(ipaddress.ip_network(str(lan_addr) + "/" + str(lan_prefix)).hosts())
    real_lan_total_addr = lan_total_addr - 3
    
    if lan_prefix >= 16:
        total_addr_range =  int((real_lan_total_addr * 70) / 100)
        bottom_addr = real_lan_total_addr - total_addr_range
        top_addr_lan = real_lan_total_addr
        text1 = " ---- Total direcciones a entregar por el dhcp server (cerca de el 70% del total): "
    else:
        total_addr_range = 60000
        bottom_addr = real_lan_total_addr - total_addr_range
        top_addr_lan = real_lan_total_addr    
         
    
    print(" ---- La direccion de la red es: ", lan_addr)
    print(" ---- La mascara de red es: ", lan_netmask)
    print(" ---- El prefijo de red es: ", lan_prefix)
    print(" ---- El numero de hosts usable para esta red es: ", lan_total_addr)
    print(" ---- La direccion de bcast es: ", lan_bcast)
    print(" ---- Direccion de bcast en string", str(lan_bcast))
    print("Rango de direcciones para dhcp server: ")
    print(" ---- Total direcciones a entregar por el dhcp server: ", total_addr_range)
    print(" ---- Primera IP del rango es: ", l[bottom_addr])
    last_ip = str(lan_bcast).split(".")
    print(" ---- Ultima IP del rango es: ", last_ip[0] + "." + last_ip[1] + "." + last_ip[2] + "." + str(int(last_ip[3]) - 3))    
    
    tmp = str(lan_addr)
    tmp2 = str(lan_netmask)
    l1 = "INTERFACES=\"eth0\";"
    l2 = "default-lease-time 600;"
    l3 = "max-lease-time 7200;"
    l4 = ""
    l5 = "subnet " + tmp + " " + "netmask " + tmp2 + "{"
    l6 = " range " + str(l[bottom_addr]) + " " + last_ip[0] + "." + last_ip[1] + "." + last_ip[2] + "." + str(int(last_ip[3]) - 3) + ";"
    tmp = str(lan_addr).split(".")
    l7 = " option routers " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + fw_ip + ";"
    l8 = " option domain-name-servers " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad1_ip + ", " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + ad2_ip + ";"
    l9 = " option domain-name \"" + realm + "\"" + ";"
    l10 = "}"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.close()

def radius_ntlm_auth():
    filename = "files" + "/" + realm + "-" + "radius_ntlm_auth"
    r = (realm.upper()).split(".")    
    l1 = "exec ntlm_auth {"
    l2 = "        wait = yes"
    l3 = "        program = \"/usr/bin/ntlm_auth --request-nt-key --domain=" + r[0] + " --username=%{mschap:User-Name} --password=%{User-Password}\""
    l4 = "}"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.close()

def radius_mschap():
    
    filename = "files" + "/" + realm + "-" + "radius_mschap"
    r = (realm.upper()).split(".")    
    l1 = "mschap {"
    l2 = "        ntlm_auth = \"/usr/bin/ntlm_auth --request-nt-key --username=%{mschap:User-Name:-None} --domain=%{%{mschap:NT-Domain}:-" + r[0] + "} --challenge=%{mschap:Challenge:-00} --nt-response=%{mschap:NT-Response:-00}\""
    l3 = "        pool {"
    l4 = "                start = ${thread[pool].start_servers}"
    l5 = "                min = ${thread[pool].min_spare_servers}"
    l6 = "                max = ${thread[pool].max_servers}"
    l7 = "                spare = ${thread[pool].max_spare_servers}"
    l8 = "                uses = 0"
    l9 = "                retry_delay = 30"
    l10 = "                lifetime = 86400"
    l11 = "                cleanup_interval = 300"
    l12 = "                idle_timeout = 600"
    l13 = "          }"
    l14 = "          passchange {"
    l15 = "          }"
    l16 = "}"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n') 
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.write(l13 + '\n')
        out.write(l14 + '\n')
        out.write(l15 + '\n')
        out.write(l16 + '\n')
        out.close()


def radius_client():
    
    filename = "files" + "/" + realm + "-" + "radius_client"
    l1 = "client LAN {"
    l2 = "       ipaddr          = " + str(lan_addr) + "/" + str(lan_prefix)
    l3 = "       secret          = qwertyui"
    l4 = "}"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n') 
        out.close()


def fw_rules():
    filename = "files" + "/" + realm + "-" + "fw_rules"
    lanaddr = str(lan_addr)
    tmp = lanaddr.split(".")      
    l1 = "#!/bin/bash"
    l2 = "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
    l3 = "iptables -t nat -A  PREROUTING -p tcp -m tcp -i eth1 --dport 443 -j DNAT --to-destination " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + vpn_ip
    l4 = "iptables -t nat -A PREROUTING -p udp -m udp -m multiport -i eth1 --dports 500,1701,4500 -j DNAT --to-destination " + tmp[0] + "." + tmp[1] + "." + tmp[2] + "." + vpn_ip
    l5 = "iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE"
    #bloquear todo trafico entrante / block all incoming traffic
    l6 = "iptables -P INPUT DROP"
    l7 = "iptables -P FORWARD DROP"
    l8 = "iptables -P OUTPUT ACCEPT"
    #permitir todo sobre localhost / allow all on localhost
    l9 = "iptables -A INPUT -i lo -j ACCEPT"
    #Aceptar ping request sonbre la WAN / Accept ping request on WAN
    l10 = "iptables -A INPUT -i eth1 -p icmp --icmp-type 8/0 -j ACCEPT"
    l11 = "iptables -A INPUT -i eth1 -p icmp --icmp-type 0/0 -j ACCEPT"
    #Permitir ssh / allow ssh
    l12 = "iptables -A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT"
    #Permitir trafico iniciado en el fw / allow traffci from fw to any
    l13 = "iptables -I INPUT -i eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT"
    #Permitir a la LAN ir a cualquier parte
    l14 = "iptables -A FORWARD -s " + str(lan_addr) + "/" + str(lan_prefix) + " -j ACCEPT"
    l15 = "iptables -A FORWARD -d " + str(lan_addr) + "/" + str(lan_prefix) + " -j ACCEPT"
    l16 = "iptables -A INPUT -s " + str(lan_addr) + "/" + str(lan_prefix) + " -j ACCEPT"
    
    
    
    
    
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.write(l13 + '\n')
        out.write(l14 + '\n')
        out.write(l15 + '\n')
        out.write(l16 + '\n')
        out.close()
        
def hostap_default():
    filename = "files" + "/" + realm + "-" + "hostap_default"
    l1 = "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.close()
        
def hostap_conf():
    lanaddr = (str(lan_addr)).split(".")
    filename = "files" + "/" + realm + "-" + "hostap_conf"
    l1 = "interface=wlan0"
    l2 = "bridge=LAN"
    l3 = "driver=nl80211"
    l4 = "ssid=" + realm
    l5 = "hw_mode=g"
    l6 = "channel=7"
    l7 = "ieee8021x=1"
    l8 = "auth_algs=1"
    l9 = "eap_server=0"
    l10 = "eapol_key_index_workaround=1"
    l11 = "auth_server_addr=" + lanaddr[0] + "." + lanaddr[1] + "." + lanaddr[2] + "." + fw_ip
    l12 = "auth_server_port=1812"
    l13 = "auth_server_shared_secret=qwertyui"
    l14 = "wpa=1"
    l15 = "wpa_key_mgmt=WPA-EAP"
    l16 = "wpa_pairwise=TKIP CCMP"
    l17 = "wpa_group_rekey=300"
    l18 = "wpa_gmk_rekey=640"
    
    with open(filename, "w+") as out:
        out.write(l1 + '\n')
        out.write(l2 + '\n')
        out.write(l3 + '\n')
        out.write(l4 + '\n')
        out.write(l5 + '\n')
        out.write(l6 + '\n')
        out.write(l7 + '\n')
        out.write(l8 + '\n')
        out.write(l9 + '\n')
        out.write(l10 + '\n')
        out.write(l11 + '\n')
        out.write(l12 + '\n')
        out.write(l13 + '\n')
        out.write(l14 + '\n')
        out.write(l15 + '\n')
        out.write(l16 + '\n')
        out.write(l17 + '\n')
        out.write(l18 + '\n')
        out.close()

def genera_lxd():
    client = Client()
    machine = ['ad1', 'ad2', 'fs', 'vpn', 'fw']; 
    for i in machine:
        print(i)
        if i == "ad1":
            print("Generando maquina con perfil AD", i + "\n")
            config = ({'name': i, 'source': {'type': 'image', 'alias': 'samba'}, 'profiles': ['AD']})
            a = client.containers.create(config, wait=True)
            a.start()
            print("Se genero y encendio la maquina", a.name + "\n")
            wait(tmed)
            netplan(ad1_ip, ad1_name)
            hosts(ad1_ip, ad1_name)
            resolv(ad1_name)
            samba_inst_ad1(ad1_name)
            
        
        if i == "ad2":
            print("Generando maquina con perfil AD", i + "\n")
            config = ({'name': i, 'source': {'type': 'image', 'alias': 'samba'}, 'profiles': ['AD']})
            a = client.containers.create(config, wait=True)
            a.start()
            print("Se genero y encendio la maquina", a.name + "\n")
            wait(tmed)
            netplan(ad2_ip, ad2_name)
            hosts(ad2_ip, ad2_name)
            resolv(ad2_name)
            krb5()
            samba_inst_ad2(ad2_name)
            
        if i == "fs":
            print("Generando maquina con perfil LAN", i + "\n")
            config = ({'name': i, 'source': {'type': 'image', 'alias': 'samba'}, 'profiles': ['LAN']})
            a = client.containers.create(config, wait=True)
            a.start()
            print("Se genero y encendio la maquina", a.name + "\n")
            wait(tmed)
            netplan(fs_ip, fs_name)
            hosts(fs_ip, fs_name)
            resolv(fs_name)
            samba_ws_file()
            nsswitch()
            samba_fs_setup()
            
        if i == "vpn":
            print("Generando maquina con perfil LAN", i + "\n")
            config = ({'name': i, 'source': {'type': 'image', 'alias': 'vpn'}, 'profiles': ['LAN']})
            a = client.containers.create(config, wait=True)
            a.start()
            print("Se genero y encendio la maquina", a.name + "\n")
            wait(tmed)            
            netplan(vpn_ip, vpn_name)
            hosts(vpn_ip, vpn_name)
            resolv(vpn_name) 
            
        if i == "fw":
            print("Generando maquina con perfil WAN", i + "\n")
            config = ({'name': i, 'source': {'type': 'image', 'alias': 'fw'}, 'profiles': ['WAN']})
            a = client.containers.create(config, wait=True)
            a.start()
            print("Se genero y encendio la maquina", a.name + "\n")
            wait(tmed)
            netplanfw(fw_ip, fw_name)
            hosts(fw_ip, fw_name)
            resolv(fw_name)
            dhcpd(fw_name)
            radius_mschap()
            radius_ntlm_auth()
            radius_client()
            fw_rules()


def instala_lxd():
    client = Client()
    a = client.containers.all()
    for i in a:
        print(i.name)
        if i.name == "ad1" :
            n = i.name
            fixsmb = open('fix_smb.sh').read()
            sambainstall = open('files' + '/' + realm + '-' + n + '-' + 'samba.sh').read()
            netdata = open('files' + '/' + realm + '-' + n + '-' + '50-cloud-init.yaml').read()
            dnsdata = open('files' + '/' + realm + '-' + n + '-' + 'resolv.conf').read()
            hostsdata = open('files' + '/' + realm + '-' + n + '-' + 'hosts').read()
            print("Copiando hosts \n")
            i.files.put('/etc/hosts', hostsdata)
            print("Se acaba de copiar hosts \n")
            wait(tmin)
            print("Copiando netplan \n")
            i.files.put('/etc/netplan/50-cloud-init.yaml', netdata)
            print("Se acaba de copiar netplan \n")
            print("Reiniciando contenedor antes de provisionar AD \n")
            i.restart()
            wait(tmed)
            print("Copiando provisionamiento de samba \n")
            i.files.put('/root/samba.sh', sambainstall)
            wait(tmin)
            e, so, se = i.execute(['chmod', '755', '/root/samba.sh'])
            print(so)
            wait(tmin)
            print("Ejecutando provisionamiento de samba \n")
            e, so, se = i.execute(['/root/samba.sh'])
            print("Copiando resolv.conf \n")
            i.files.put('/etc/resolv.conf', dnsdata)
            print("Se acaba de copiar resolv.conf")
            print("Copiando fix_smb.sh \n")
            i.files.put('/root/fix_smb.sh', fixsmb)
            e, so, se = i.execute(['chmod', '755', '/root/fix_smb.sh'])
            e, so, se = i.execute(['/root/fix_smb.sh'])
            print("Reiniciando......\n")
            i.restart() 
            wait(tmax)
            print("Contenedor samba directorio principal aprovisionado \n")
            
        if i.name == "ad2" :
            n = i.name
            fixsmb = open('fix_smbad2.sh').read()            
            sambainstall = open('files' + '/' + realm + "-" + n + "-" + "samba.sh").read()
            netdata = open('files' + '/' + realm + "-" + n + "-" + '50-cloud-init.yaml').read()
            dnsdataad1 = open('files' + '/' + realm + "-" + "ad1" + "-" + 'resolv.conf').read()
            dnsdata = open('files' + '/' + realm + "-" + n + "-" + 'resolv.conf').read()
            hostsdata = open('files' + '/' + realm + "-" + n + "-" + 'hosts').read()
            krb5data = open('files' + '/' + realm + "-" + "krb5")
            print("Copiando hosts en: ", i.name + "\n")
            i.files.put('/etc/hosts', hostsdata)
            print("Se acaba de copiar hosts en: ", i.name + "\n")
            wait(tmin)
            print("Copiando netplan en: ", i.name + "\n")
            i.files.put('/etc/netplan/50-cloud-init.yaml', netdata)
            print("Se acaba de copiar netplan: ", i.name + "\n")
            print("Deshabilitando resolved y copiando resolv.conf en: ", i.name + "\n")
            e, so, se = i.execute(['systemctl', 'disable', 'systemd-resolved'])
            e, so, se = i.execute(['rm', '/etc/resolv.conf'])
            i.files.put('/etc/resolv.conf', dnsdataad1)
            wait(tmin)
            print("Copiando configuracionde kerberos en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/krb5.conf'])
            i.files.put('/etc/krb5.conf', krb5data)
            print("Reiniciando contenedor \n")
            i.restart()
            wait(tmed)
            print("Copiando provisionamiento de samba en: ", i.name + "\n")
            i.files.put('/root/samba.sh', sambainstall)
            wait(tmin)
            e, so, se = i.execute(['chmod', '755', '/root/samba.sh'])
            print(so)
            wait(tmin)
            print("Ejecutando provisionamiento de samba \n")
            e, so, se = i.execute(['/root/samba.sh'])
            print(e)
            print(so)
            print(se)
            print("Copiando resolv.conf definitivo en: ", i.name + "\n")
            i.files.put('/etc/resolv.conf', dnsdata)
            print("Se acaba de copiar resolv.conf \n")
            print("Copiando fix_smb.sh \n")
            i.files.put('/root/fix_smb.sh', fixsmb)
            e, so, se = i.execute(['chmod', '755', '/root/fix_smb.sh'])
            e, so, se = i.execute(['/root/fix_smb.sh'])            
            print("Reiniciando......\n")
            i.restart()
            wait(tmax)
            print("Contenedor samba directorio secundario aprovisionado \n")
            
            
        
        if i.name == "fs" :
            n = i.name
            netdata = open('files' + '/' + realm + "-" + n + "-" + '50-cloud-init.yaml').read()
            dnsdata = open('files' + '/' + realm + "-" + n + "-" + 'resolv.conf').read()
            hostsdata = open('files' + '/' + realm + "-" + n + "-" + 'hosts').read()
            krb5data = open('files' + '/' + realm + "-" + "krb5")
            smbfile = open('files' + '/' + realm + "-" + "sambawsfile")
            nsswitchdata = open('files' + '/' + realm + "-" + "nsswitch")
            fs_setup = open("files" + "/" + realm + "-" + "samba_fs_setup")
            print("Copiando hosts en: ", i.name + "\n")
            i.files.put('/etc/hosts', hostsdata)
            print("Se acaba de copiar hosts en: ", i.name + "\n")
            wait(tmin)
            print("Copiando netplan en: ", i.name + "\n")
            i.files.put('/etc/netplan/50-cloud-init.yaml', netdata)
            print("Se acaba de copiar netplan en: ", i.name + "\n")
            print("Deshabilitando resolved y copiando resolv.conf en: ", i.name + "\n")
            e, so, se = i.execute(['systemctl', 'disable', 'systemd-resolved'])
            e, so, se = i.execute(['rm', '/etc/resolv.conf'])
            i.files.put('/etc/resolv.conf', dnsdata)
            e, so, se = i.execute(['chmod', '755', '/etc/resolv.conf'])
            print("Copiando configuracionde kerberos en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/krb5.conf'])
            i.files.put('/etc/krb5.conf', krb5data)   
            print("Copiando configuracion de samba en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/samba/smb.conf'])
            i.files.put('/etc/samba/smb.conf', smbfile)
            e, so, se = i.execute(['chmod', '755', '/etc/samba/smb.conf'])
            print("Reiniciando antes del join al dominio....:\n")
            i.restart()
            wait(tmax)
            e, so, se = i.execute(['net', 'ads', 'join', '-U', 'administrator%Abcd1234'])
            print(e)
            print(so)
            print(se)
            print("Copiando /etc/nsswitch.conf en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/nsswitch.conf'])
            i.files.put('/etc/nsswitch.conf', nsswitchdata)
            print("Reiniciando........\n")
            wait(tmax)
            print("****** Setup FS *********")
            i.files.put('/root/fs_setup.sh', fs_setup)
            e, so, se = i.execute(['chmod', '755', '/root/fs_setup.sh'])
            print(e)
            print(so)
            print(se)
            i.restart()
            wait(tmax)
            e, so, se = i.execute(['/root/fs_setup.sh'])
            print(e)
            print(so)
            print(se)            
            print("Reiniciando........\n")
            i.restart()
            wait(tmax)
            
        if i.name == "vpn" :
            n = i.name
            netdata = open('files' + '/' + realm + "-" + n + "-" + '50-cloud-init.yaml').read()
            dnsdata = open('files' + '/' + realm + "-" + n + "-" + 'resolv.conf').read()
            hostsdata = open('files' + '/' + realm + "-" + n + "-" + 'hosts').read()            
            vpndata = open('vpn_install.sh')
            vpnservice = open('vpnserver.service')
            print("Copiando y provisionando vpn \n")
            i.files.put('/root/vpn_install.sh', vpndata)
            e, so, se = i.execute(['chmod', '755', '/root/vpn_install.sh'])
            e, so, se = i.execute(['/root/vpn_install.sh'])
            print(e)
            print(so)
            print(se)
            i.files.put('/lib/systemd/system/vpnserver.service', vpnservice)
            e, so, se = i.execute(['systemctl', 'enable', 'vpnserver.service'])
            print("Copiando hosts en: ", i.name + "\n")
            i.files.put('/etc/hosts', hostsdata)
            print("Se acaba de copiar hosts en: ", i.name + "\n")
            wait(tmin)
            print("Copiando netplan en: ", i.name + "\n")
            i.files.put('/etc/netplan/50-cloud-init.yaml', netdata)
            print("Se acaba de copiar netplan en: ", i.name)
            print("Deshabilitando resolved y copiando resolv.conf en: ", i.name + "\n")
            e, so, se = i.execute(['systemctl', 'disable', 'systemd-resolved'])
            e, so, se = i.execute(['rm', '/etc/resolv.conf'])
            i.files.put('/etc/resolv.conf', dnsdata)
            e, so, se = i.execute(['chmod', '755', '/etc/resolv.conf'])
            print("Reiniciando........\n")
            i.restart()
            wait(tmax)
            
        if i.name == "fw" :
            n = i.name
            netdata = open('files' + '/' + realm + "-" + n + "-" + '50-cloud-init.yaml').read()
            dnsdata = open('files' + '/' + realm + "-" + n + "-" + 'resolv.conf').read()
            hostsdata = open('files' + '/' + realm + "-" + n + "-" + 'hosts').read()
            krb5data = open('files' + '/' + realm + "-" + "krb5")
            smbfile = open('files' + '/' + realm + "-" + "sambawsfile")
            nsswitchdata = open('files' + '/' + realm + "-" + "nsswitch")
            dhcpddata = open("files" + "/" + realm + "-" + "dhcpd")
            radmschapdata = open("files" + "/" + realm + "-" + "radius_mschap")
            radntlmdata = open("files" + "/" + realm + "-" + "radius_ntlm_auth")
            radshdata = open("radius.sh")
            fix_radclntdata = open("fix_radclient.sh")
            radclientdata = open("files" + "/" + realm + "-" + "radius_client")
            fwdata = open("files" + "/" + realm + "-" + "fw_rules")
            sshkeydata = open("id_rsa.pub")
            sshconfdata = open("sshd_config")
            print("Copiando hosts en: ", i.name + "\n")
            i.files.put('/etc/hosts', hostsdata)
            print("Se acaba de copiar hosts en: ", i.name + "\n")
            wait(tmin)
            print("Copiando netplan en: ", i.name + "\n")
            i.files.put('/etc/netplan/50-cloud-init.yaml', netdata)
            print("Se acaba de copiar netplan en: ", i.name + "\n") 
            print("Deshabilitando resolved y copiando resolv.conf en: ", i.name + "\n")
            e, so, se = i.execute(['systemctl', 'disable', 'systemd-resolved'])
            e, so, se = i.execute(['rm', '/etc/resolv.conf'])
            i.files.put('/etc/resolv.conf', dnsdata)
            e, so, se = i.execute(['chmod', '755', '/etc/resolv.conf'])
            print("Copiando configuracionde kerberos en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/krb5.conf'])
            i.files.put('/etc/krb5.conf', krb5data)   
            print("Copiando configuracion de samba en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/samba/smb.conf'])
            i.files.put('/etc/samba/smb.conf', smbfile)
            e, so, se = i.execute(['chmod', '755', '/etc/samba/smb.conf'])
            print("Reiniciando antes del join al dominio....:\n")
            i.restart()
            wait(tmax)
            e, so, se = i.execute(['net', 'ads', 'join', '-U', 'administrator%Abcd1234'])
            print(e)
            print(so)
            print(se)
            print("Copiando /etc/nsswitch.conf en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/nsswitch.conf'])
            i.files.put('/etc/nsswitch.conf', nsswitchdata)
            print("Copiando /etc/dhcp/dhcpd.conf en: ", i.name + "\n")
            e, so, se = i.execute(['rm', '/etc/dhcp/dhcpd.conf'])
            i.files.put('/etc/dhcp/dhcpd.conf', dhcpddata)
            e, so, se = i.execute(['systemctl', 'enable', 'isc-dhcp-server.service'])
            print("Quitando archivos de freeradius: \n")
            e, so, se = i.execute(['rm', '/etc/freeradius/3.0/mods-available/mschap'])
            e, so, se = i.execute(['rm', '/etc/freeradius/3.0/mods-available/ntlm_auth'])
            print("Copiando archivos freeradius para el dominio \n")
            i.files.put('/etc/freeradius/3.0/mods-available/mschap', radmschapdata)
            i.files.put('/etc/freeradius/3.0/mods-available/ntlm_auth', radntlmdata)
            print("Activando autenticacion en freeradius: \n")
            i.files.put('/root/radius.sh', radshdata)
            e, so, se = i.execute(['chmod', '755', '/root/radius.sh'])
            e, so, se = i.execute(['/root/radius.sh'])
            e, so, se = i.execute(['systemctl', 'enable', 'freeradius'])
            e, so, se = i.execute(['usermod', '-a', '-G', 'winbindd_priv', 'freerad'])
            print("Configurando clientes de radius.....: ")
            i.files.put('/root/radclient.txt', radclientdata)
            i.files.put('/root/fix_radclient.sh', fix_radclntdata)
            e, so, se = i.execute(['chmod', '755', '/root/fix_radclient.sh'])
            e, so, se = i.execute(['/root/fix_radclient.sh'])
            print("Realizando ultimos ajustes sobre sshd........\n")
            i.files.put('/etc/ssh/sshd_config', sshconfdata)
            i.files.put('/root/.ssh/authorized_keys', sshkeydata)
            print("Instalando reglas de NAT: ")
            i.files.put('/etc/rc.local', fwdata)
            e, so, se = i.execute(['chmod', '755', '/etc/rc.local'])
            print("Reiniciando........\n")
            i.restart()
            wait(tmax)





def install_rbpi_ap():
    
    hostap_dflt = "files" + "/" + realm + "-" + "hostap_default"
    hostap_cfg = "files" + "/" + realm + "-" + "hostap_conf"
    subprocess.run(["systemctl", "unmask", "hostapd"])
    subprocess.run(["systemctl", "enable", "hostapd"])
    subprocess.run(["cp", hostap_dflt, "/etc/default/hostapd"])
    subprocess.run(["cp", hostap_cfg, "/etc/hostapd/hostapd.conf"])
    subprocess.run(["systemctl", "start", "hostapd"])
    subprocess.run(["systemctl", "mask", "ctrl-alt-del.target"])
    subprocess.run(["systemctl", "daemon-reload"])
    
def main():
    control = 0
    while control == 0:
        get_domain_name()
        get_lan_addr()
        get_wan_addr()
        get_nics()
        summary_report()
        ok = input("Es correcta la informacion de configuracion? (s/n)")
        if ok == "s":
            control = 1
    set_arch()
    provision()
    netplan_raspberry()
    profiles()
    genera_lxd()
    instala_lxd()
    if rb_hw == True:
        print("Configurando hostapd en Raspberry Pi: \n")
        install_rbpi_ap()
   
    
main()
