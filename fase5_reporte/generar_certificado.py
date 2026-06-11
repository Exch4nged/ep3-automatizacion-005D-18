#!/usr/bin/env python3
# Script que genera el certificado de compliance final

import os, datetime, yaml, glob

# Carga el archivo de variables del alumno
with open("../vars/vars_005D-18.yaml") as f:
    v = yaml.safe_load(f)

# Verifica resultado de validación NETCONF
# Busca la palabra CONFORME en el output de la Fase 3
netconf_ok = False
try:
    with open("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt") as f:
        contenido = f.read()
        netconf_ok = "CONFORME" in contenido and "NO CONFORME" not in contenido
except:
    pass

# Verifica resultado de validación RESTCONF
# Busca la palabra CONFORME en el output de la Fase 4
restconf_ok = False
try:
    with open("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt") as f:
        contenido = f.read()
        restconf_ok = "CONFORME" in contenido and "NO CONFORME" not in contenido
except:
    pass

# Verifica que el diff generó archivos con diferencias detectadas
diff_ok = False
diff_files = glob.glob("evidencias/diff_005D-18/*.txt")
if diff_files:
    diff_ok = True

# Resultado global: CONFORME solo si las 3 validaciones pasaron
resultado_global = "CONFORME" if (netconf_ok and restconf_ok and diff_ok) else "NO CONFORME"

# Genera el texto del certificado
certificado = f"""
========================================================
   CERTIFICADO DE COMPLIANCE — EP3 DRY7122
========================================================
Alumno   : {v['alumno']['nombre']}
Código   : {v['alumno']['codigo']}
Empresa  : {v['cliente']['empresa']}
Router   : {v['cliente']['hostname']}
Fecha    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------------------------
Validación NETCONF  : {"CONFORME" if netconf_ok else "NO CONFORME"}
Validación RESTCONF : {"CONFORME" if restconf_ok else "NO CONFORME"}
Diff baseline/final : {"DETECTADO" if diff_ok else "SIN CAMBIOS"}
--------------------------------------------------------
RESULTADO FINAL     : {resultado_global}
========================================================
El equipo {v['cliente']['hostname']} ha sido aprovisionado
correctamente y está listo para operar en producción.
========================================================
"""

# Imprime el certificado en pantalla
print(certificado)

# Guarda el certificado en archivo
os.makedirs("evidencias", exist_ok=True)
with open("evidencias/certificado_compliance_005D-18.txt", "w") as f:
    f.write(certificado)
print("Certificado guardado en evidencias/certificado_compliance_005D-18.txt")
