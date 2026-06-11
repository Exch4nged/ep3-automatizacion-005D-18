#!/usr/bin/env python3
# Indica que se ejecuta con Python 3

import sys, os, datetime
# sys: interacción con el sistema
# os: operaciones de archivos y carpetas
# datetime: obtener fecha y hora actual

from ncclient import manager
# ncclient: librería para conectarse via NETCONF

import yaml
# yaml: para leer el archivo vars_005D-18.yaml

from lxml import etree
# lxml: para parsear y navegar el XML que devuelve el router

# Imprime encabezado con datos del alumno, fecha y hostname de la VM
print("=" * 50)
print(f"Script  : validacion_netconf.py")
print(f"Alumno  : 005D-18 — Axl Jesus Urrutia Maldonado")
print(f"Fecha   : {datetime.datetime.now()}")
print(f"Host VM : {os.uname().nodename}")
print("=" * 50)

# Abre y carga el archivo de variables del alumno
with open("../vars/vars_005D-18.yaml") as f:
    v = yaml.safe_load(f)

# Accesos directos a las secciones router y cliente del yaml
r = v["router"]
c = v["cliente"]

# Filtro XML que le dice al router: "dame solo la config nativa de IOS-XE"
# Sin filtro devolvería TODA la config en miles de líneas
filtro = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""

print("\nConectando al router via NETCONF...")

# Abre sesión NETCONF con el router
# hostkey_verify=False: no verifica el certificado SSH del router
# allow_agent=False y look_for_keys=False: usa solo usuario/contraseña
with manager.connect(
    host=r["ip"],
    port=830,
    username=r["usuario"],
    password=r["password"],
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:
    # Solicita la configuración actual del router (running-config en formato XML)
    reply = m.get_config(source="running", filter=filtro)

# Crea la carpeta evidencias si no existe
os.makedirs("evidencias", exist_ok=True)

# Guarda el XML crudo que devolvió el router (entregable E13)
with open("evidencias/rpc_reply_raw.xml", "w") as f:
    f.write(str(reply))
print("XML guardado en evidencias/rpc_reply_raw.xml")

# Convierte el XML a un árbol navegable
root = etree.fromstring(reply.xml.encode())

# Namespaces necesarios para navegar el XML de Cisco IOS-XE
ns = {
    "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
    "ios-ntp": "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"
}

# Función auxiliar: busca un valor en el XML usando xpath
# Retorna el texto del elemento encontrado, o None si no existe
def get_text(xpath):
    try:
        result = root.xpath(xpath, namespaces=ns)
        return result[0].text if result else None
    except:
        return None

# Extrae cada valor de la config del router usando xpath
hostname_actual = get_text("//ios:native/ios:hostname")
loopback_ip     = get_text("//ios:native/ios:interface/ios:Loopback[ios:name='18']/ios:ip/ios:address/ios:primary/ios:address")
loopback_mask   = get_text("//ios:native/ios:interface/ios:Loopback[ios:name='18']/ios:ip/ios:address/ios:primary/ios:mask")
desc_wan        = get_text("//ios:native/ios:interface/ios:GigabitEthernet[ios:name='1']/ios:description")
ntp_server      = get_text("//ios:native/ios:ntp/ios-ntp:server/ios-ntp:server-list/ios-ntp:ip-address")

print("\n--- RESULTADO DE VALIDACION NETCONF ---")

# Lista de criterios a validar: (nombre, valor_obtenido_del_router, valor_esperado_del_yaml)
criterios = [
    ("Hostname",        hostname_actual, c["hostname"]),
    ("Loopback IP",     loopback_ip,     r["loopback_ip"]),
    ("Loopback Mask",   loopback_mask,   r["loopback_mask"]),
    ("Descripcion WAN", desc_wan,        r["descripcion_wan"]),
    ("NTP Server",      ntp_server,      r["ntp_server"]),
]

ok_count = 0
# Compara cada valor obtenido contra el esperado e imprime [OK] o [FAIL]
for nombre, actual, esperado in criterios:
    estado = "[OK]" if actual == esperado else "[FAIL]"
    if estado == "[OK]":
        ok_count += 1
    print(f"  {estado}  {nombre}: esperado='{esperado}' actual='{actual}'")

# Imprime resumen final
print(f"\nResultado: {ok_count}/5 criterios conformes")
print("\n>>> RESULTADO GLOBAL:", "CONFORME" if ok_count == 5 else "NO CONFORME")
