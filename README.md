# EP3 Automatización de Red — Axl Urrutia — 005D-18
# EP3 — Implementación de Automatización de Red con Compliance Auditado
**Alumno:** Axl Jesus Urrutia Maldonado | **Código:** 005D-18 | **Sección:** 005D

---

## 1. Objetivo del proyecto
Se implementó la automatización completa del aprovisionamiento del router RTR-LABBIOS para la empresa Laboratorios Bios SpA. El objetivo fue incorporar el equipo a la red corporativa aplicando configuración estándar de forma automatizada y verificable, dejando evidencia auditada en GitHub.

## 2. Alcance
Se configuró hostname corporativo, banner de acceso, servidor NTP, descripción de interfaz WAN y loopback de gestión. También se habilitaron los servicios NETCONF, RESTCONF y HTTP seguro. No se abordó configuración de routing dinámico, VLANs ni políticas de seguridad avanzadas. Las herramientas utilizadas fueron pyATS/Genie, Ansible, ncclient y Python requests.

## 3. Infraestructura utilizada
| Componente | Detalle |
|---|---|
| Router | Cisco CSR1000v — IOS XE 16.9 |
| IP Router | 192.168.56.104 |
| Estación de trabajo | DEVASC VM — Ubuntu / labvm |
| Ansible | 6.7.0 |
| Python | 3.8.10 |
| pyATS/Genie | Última versión disponible |

## 4. Tecnologías empleadas y justificación
- **pyATS/Genie:** Se usó en la Fase 1 y 5 para capturar y comparar el estado del router via SSH, sin requerir NETCONF habilitado previamente.
- **Ansible:** Se usó en la Fase 2 porque permite aplicar configuración de forma declarativa, idempotente y reproducible sobre dispositivos IOS.
- **NETCONF/ncclient:** Se usó en la Fase 3 para validar la configuración via protocolo estándar XML, independiente de Ansible.
- **RESTCONF/requests:** Se usó en la Fase 4 para verificar recursos específicos de configuración en formato JSON via HTTP.

## 5. Configuración aplicada
| Parámetro | Valor |
|---|---|
| Hostname | RTR-LABBIOS |
| Banner | ACCESO RESTRINGIDO - LABBIOS |
| NTP Server | 8.8.8.8 |
| Descripción WAN | Enlace-WAN-Chillan |
| Loopback18 IP | 10.5.18.1 / 255.255.255.0 |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado (HTTPS) |

## 6. Resultados de validación
| Criterio | NETCONF | RESTCONF |
|---|---|---|
| Hostname | CONFORME | CONFORME |
| Loopback IP | CONFORME | CONFORME |
| Loopback Mask | CONFORME | — |
| Descripción WAN | CONFORME | CONFORME |
| NTP Server | CONFORME | CONFORME |

## 7. Conclusiones
El router RTR-LABBIOS fue aprovisionado exitosamente con toda la configuración corporativa requerida. Las validaciones independientes via NETCONF (5/5) y RESTCONF (4/4) confirmaron que la configuración quedó aplicada correctamente. El diff entre el baseline inicial y el snapshot final evidenció los cambios realizados. El equipo fue entregado a operaciones en estado CONFORME.
