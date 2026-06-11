#!/usr/bin/env python3
# Ejecuta con Python 3

import requests, json, os, datetime, yaml
# requests: para hacer consultas HTTP/HTTPS al router via RESTCONF
# json: para guardar las respuestas en formato JSON
# os: operaciones de archivos y carpetas
# datetime: fecha y hora actual
# yaml: para leer el archivo de variables

import urllib3
# urllib3: para suprimir advertencias de certificado SSL autofirmado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Encabezado con datos del alumno
print("=" * 50)
print(f"Script  : validacion_restconf.py")
print(f"Alumno  : 005D-18 — Axl Jesus Urrutia Maldonado")
print(f"Fecha   : {datetime.datetime.now()}")
print(f"Host VM : {os.uname().nodename}")
print("=" * 50)

# Carga el archivo de variables del alumno
with open("../vars/vars_005D-18.yaml") as f:
    v = yaml.safe_load(f)

# Accesos directos a las secciones router y cliente
r = v["router"]
c = v["cliente"]

# URL base de RESTCONF en el router
BASE = f"https://{r['ip']}/restconf/data"

# Credenciales de autenticación
AUTH = (r["usuario"], r["password"])

# Header que indica que esperamos respuesta en formato JSON
HEADERS = {"Accept": "application/yang-data+json"}

# Crea la carpeta de respuestas si no existe
os.makedirs("evidencias/responses", exist_ok=True)

# Lista de endpoints a consultar:
# (nombre_interno, path_del_endpoint, archivo_donde_guardar)
endpoints = [
    ("hostname",   "Cisco-IOS-XE-native:native/hostname",
     "evidencias/responses/get_hostname.json"),

    ("loopback",   f"ietf-interfaces:interfaces/interface=Loopback{r['loopback_id']}",
     "evidencias/responses/get_loopback.json"),

    ("interfaces", "ietf-interfaces:interfaces/interface=GigabitEthernet1",
     "evidencias/responses/get_interfaces.json"),

    ("ntp",        "Cisco-IOS-XE-native:native/ntp",
     "evidencias/responses/get_ntp.json"),
]

responses = {}
# Recorre cada endpoint, consulta el router y guarda la respuesta JSON
for key, path, outfile in endpoints:
    url = f"{BASE}/{path}"
    # verify=False: ignora el certificado SSL autofirmado del router
    resp = requests.get(url, auth=AUTH, headers=HEADERS, verify=False)
    data = resp.json()
    with open(outfile, "w") as f:
        json.dump(data, f, indent=2)
    responses[key] = data
    print(f"  Guardado: {outfile}")

# Extrae los valores relevantes de cada respuesta JSON
# Acceso directo a cada campo según la estructura real del router
hostname_actual = responses["hostname"].get("Cisco-IOS-XE-native:hostname")

# La IP del loopback está dentro de una lista "address"
loopback_ip     = responses["loopback"]["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"][0]["ip"]

# La descripción WAN está directamente en el objeto interface
desc_wan        = responses["interfaces"]["ietf-interfaces:interface"].get("description")

# El servidor NTP está dentro de una lista "server-list"
ntp_actual      = responses["ntp"]["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"][0]["ip-address"]

print("\n--- RESULTADO DE VALIDACION RESTCONF ---")

# Lista de criterios: (nombre, valor_del_router, valor_esperado_del_yaml)
criterios = [
    ("Hostname",        hostname_actual, c["hostname"]),
    ("Loopback IP",     loopback_ip,     r["loopback_ip"]),
    ("Descripcion WAN", desc_wan,        r["descripcion_wan"]),
    ("NTP Server",      ntp_actual,      r["ntp_server"]),
]

ok_count = 0
# Compara cada valor y muestra [OK] o [FAIL]
for nombre, actual, esperado in criterios:
    estado = "[OK]" if actual == esperado else "[FAIL]"
    if estado == "[OK]":
        ok_count += 1
    print(f"  {estado}  {nombre}: esperado='{esperado}' actual='{actual}'")

# Resumen final
print(f"\nResultado: {ok_count}/4 criterios conformes")
print("\n>>> RESULTADO GLOBAL:", "CONFORME" if ok_count == 4 else "NO CONFORME")
