Objetivo: Levantar una infraestructura minima para una oficina pequenia sobre un Raspberry Pi usando LXD y Ubuntu.


Firewall

Directorio

Directorio de backup

File server

VPN


p.e para una red tipo 192.168.100.0/24:


192.168.100.1 fw

192.168.100.2 ad1

192.168.100.3 ad2

192.168.100.4 fs

192.168.100.5 vpn

192.168.100.254 Raspberry PI


Todos los anteriores corriendo como contenedores / maquinas virtuales sobre LXD en Ubuntu server 19!



Que necesitas ?


Raspberry PI 3 B+, si tienes una Raspberry PI 4 mucho mejor .

Instalacion limpia de Ubuntu 19 sobre tu Raspberry (por defecto ya trae LXD)

Una tarjeta de red adicional (USB a RJ-45)

Script de instalacion

Conexion a internet


El script hara toda la instalacion de cada componente y la inicializacionde LXD


Instalacion:



1. Copiar llave publica de ssh en el directorio de instalacion (nanoNBXv1.0),la usara para acceder al fw via ssh. Despues copiar el directorio entero sobre la Raspberry. Verificar que tiene conexion a internet y la resolucion de nombre funciona bien.


2. Acceder a la Raspberry COMO ROOT , y posicionarse en el directorio donde esta el script, muy importante o no funcionara.


3. Con la cuenta de root, ejecutar init.sh, este script descarga el software necesario para el script principal e inicializa LXD.


4. Ejecutar NanoNBXv1.0.py, este script instala los 5 servidores y configura todo para que interactuen.


Si el punto anterior falla (falla descargando el software o algun otro) y queremos repetirlo, ejecutaremos el script llamado CleanUP.py y volveremos a el punto numero 4.


5. Introducir los datos


6. Esperar...



Usuarios y passwords:


Dominio:

Usuario : Administrator

Passwd: Abcd1234


FreeRadius secret (corriendo sobre el fw) : qwertyui


Al terminar, deberia ver una red wifi con el nombre de dominio que puso en el punto 5, de momento el unico usuario del dominio es el administrator, el cual puede usar para conectarse.


Dominio de Windows


Meter una maquina al dominio descargar RSAT (https://wiki.samba.org/index.php/Installing_RSAT) de microsoft y empezar a configurar usuarios y demas.


VPN


Decargar el software de administracion de softether y conectarse al vpn server (direccion terminada en 5)


1

- Click en IPSec / L2tp setting

- Activar L2tp over ipsec

- El IPsec PSK por defecto es vpn, puede usar ese o cambiarlo

- Click en OK


2

- Click en local bridge setting

- En virtual hub seleccion default

- En LAN Adapter seleccione eth0

- Click en create local bridge


3

- Doble click en el virtual hun DEFAULT

- Click en Authentication Server Setting

- Habilitar Use Radius Autehntication

- En Radius server la ip del firewall (la terminada en 1)

- Port 1812 por defecto

- shared secred: qwertyui

- Click en OK


4

- Click en Manage Users

- Click en New User

- Puede crear un usuario llamado * para referirise a cualquier usuario del directorio o el usuario como aparece en el user    logon name del directorio para dar acceso vpn a usuarios nombrados

- En auth type click en RADIUS Authentication

- Click en OK


La anterior configuracion puede usaerse facilmente con el cliente nativo de windows  / mac /iOS / android, protocolo l2tp.






Fileserver:


Al crear el usuario desde el "Active Directory Users and Computers" darle click con el boton derecho y elejir "properties" , ahi en home folder elegir connect, seleccionar una letra (p.e Z) y en el campo to colocar: \\fs\users\usuario.

Vera una advertencia de que el directorio no se pudo crear y que hay que ahcerlo manualmente y colocar los permisos. A decir verdad el directorio se creo automaticamente y solo falta colocar los permisos, para mi caso, supomiendo que el dominio es test.net y el usuario gustavo seria:


chown test\\gustavo:test\\domain\ users gustavo

chmod 700 gustavo/


root@fs:/Users# ls -ld gustavo/

drwx--S---+ 2 TEST\gustavo TEST\domain users 4096 Feb 19 20:31 gustavo/

root@fs:/Users#


Para una lista de usuarios lo ams sencillo seria hacer un script que lo cree y genere en directorio con los permisos








Como va la solucion:


1 Contenedor firewall: Es una estacion del dominio que se elija al momento de instalar, corre un servidor dhcp, responsable por asignar las direcciones IP a los clientes lan (el rango es el 70% del final de la direcciones aprox) , y un servidor freeRadius, responsable por autenticar a los usuarios de VPN y de la red WIFI (o cableada si se quiere) con 802.1x. Inicialmente solo tiene las reglas basicas de firewall / NAT (Permitir todo el trafico saliente, solo ping y ssh entrante y acceso a la VPN) , la idea es que cada quien configure sus propias reglas a medida, en mi caso particular uso fwbuilder (https://github.com/fwbuilder/fwbuilder).


2. Contenedor Directorio principal: Ejecuta samba 4 AD como Directorui Activo, por defecto el nivel de funcionalidad es el de un  AD 2008_R2 (mas informacion aqui (https://wiki.samba.org/index.php/Raising_the_Functional_Levels))


3. Contenedor Directorio securndario: Ejecuta una replica del directorio principal.


4. Contenedor File Server : Es una estacion del dominio que se elija al momento de instalar


5. Contenedor VPN: Esta mquina no pertenence al dominio, ejecuta el software de VPN softether (https://www.softether.org/).


6. La Raspberry PI como tal, ejecuta Ubuntu 19 y LXD como sistema de contenedores / virtualizador. Adicionalmente ejecuta hostapd, para usar la interfaz de red Wifi que trae el Raspberry PI como un accesspoint que autentica contra el directorio. Un access point aparte dara mayor cobertura, pero para un espacio pequenio (como el mio :)) el que me proporciona el Raspberry PI esta bien.


Direccionamiento de red interna:



X.X.X.X/8 Maximo, p.e 10.0.0.0/8 : 


Es una red enorme, para el Raspberry PI, siempre se puede correr sobre un servidor granade y potente que atienda varios usuarios. El limite esl el hardware.


X.X.X.X/26  Minimo, p.e 10.0.0.0/26: Que es una red suficientemente pequenia.


Se usaran las primeras 5 direcciones de la red para los contenedores y la ultima para administracion de la RaspberryPI, si tomamos como ejemplo la red 10.0.0.0/24 la cosa quedaria asi:


fw (firewall) 10.0.0.1

ad1 (active directory principal) 10.0.0.2

ad2 (active directory backup) 10.0.0.3

fs (file server) 10.0.0.4

vpn (servidor vpn) 10.0.0.5

Raspberry (maquina fisica) 10.0.0.254









