#!/usr/bin/env python3
import time
from pylxd import Client
client = Client()
a = client.containers.all()

for x in a:
    print("Borrando contenedor: ", x.name)
    x.stop()
    time.sleep(8)
    x.delete()
    
a = client.profiles.all()

for x in a:
    if x.name != "default":
        print("Borrando perfil: ", x.name)
        x.delete()
        time.sleep(8)

