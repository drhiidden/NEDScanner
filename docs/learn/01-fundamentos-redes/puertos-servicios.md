# 🔌 Puertos y Servicios de Red

## 📚 Objetivos de Aprendizaje

Al finalizar este módulo, serás capaz de:
- Comprender el concepto de puertos de red
- Identificar servicios comunes por puerto
- Analizar la seguridad de diferentes servicios
- Realizar escaneo de puertos de manera ética

## 🔌 Conceptos Básicos de Puertos

### 📋 ¿Qué es un Puerto?

Un puerto es un punto de entrada/salida lógico en un sistema informático que permite la comunicación entre aplicaciones a través de la red.

### 🏗️ Tipos de Puertos

#### **Puertos TCP (Transmission Control Protocol)**
- Orientados a conexión
- Confiables y ordenados
- Control de flujo
- Ejemplos: HTTP (80), HTTPS (443), SSH (22)

#### **Puertos UDP (User Datagram Protocol)**
- No orientados a conexión
- No confiables
- Sin control de flujo
- Ejemplos: DNS (53), DHCP (67/68), SNMP (161)

### 📊 Rango de Puertos

| Rango | Tipo | Descripción |
|-------|------|-------------|
| 1-1023 | Puertos del Sistema | Puertos bien conocidos, requieren privilegios de administrador |
| 1024-49151 | Puertos Registrados | Puertos registrados por aplicaciones |
| 49152-65535 | Puertos Dinámicos | Puertos efímeros para conexiones temporales |

## 🌐 Servicios Comunes por Puerto

### 🔒 **Puertos del Sistema (1-1023)**

#### **Puerto 21 - FTP (File Transfer Protocol)**
- **Protocolo:** TCP
- **Función:** Transferencia de archivos
- **Vulnerabilidades:**
  - Acceso anónimo
  - Transmisión en texto plano
  - Ataques de fuerza bruta
- **Contramedidas:**
  - Usar SFTP o FTPS
  - Deshabilitar acceso anónimo
  - Implementar autenticación fuerte

#### **Puerto 22 - SSH (Secure Shell)**
- **Protocolo:** TCP
- **Función:** Acceso remoto seguro
- **Vulnerabilidades:**
  - Ataques de fuerza bruta
  - Versiones vulnerables
  - Configuraciones débiles
- **Contramedidas:**
  - Usar claves SSH
  - Cambiar puerto por defecto
  - Implementar fail2ban

#### **Puerto 23 - Telnet**
- **Protocolo:** TCP
- **Función:** Acceso remoto (inseguro)
- **Vulnerabilidades:**
  - Transmisión en texto plano
  - Sin encriptación
  - Fácil interceptación
- **Contramedidas:**
  - Reemplazar por SSH
  - Deshabilitar completamente
  - Usar VPN

#### **Puerto 25 - SMTP (Simple Mail Transfer Protocol)**
- **Protocolo:** TCP
- **Función:** Envío de correo electrónico
- **Vulnerabilidades:**
  - Spam y phishing
  - Ataques de enumeración
  - Relay de correo
- **Contramedidas:**
  - Implementar autenticación
  - Usar SPF, DKIM, DMARC
  - Filtrado de spam

#### **Puerto 53 - DNS (Domain Name System)**
- **Protocolo:** TCP/UDP
- **Función:** Resolución de nombres
- **Vulnerabilidades:**
  - DNS poisoning
  - Amplificación DDoS
  - Zone transfer no autorizada
- **Contramedidas:**
  - DNSSEC
  - Rate limiting
  - Filtrado de consultas

#### **Puerto 80 - HTTP (Hypertext Transfer Protocol)**
- **Protocolo:** TCP
- **Función:** Navegación web
- **Vulnerabilidades:**
  - Transmisión en texto plano
  - Ataques de inyección
  - Cross-site scripting
- **Contramedidas:**
  - Usar HTTPS
  - Implementar WAF
  - Validación de entrada

#### **Puerto 443 - HTTPS (HTTP Secure)**
- **Protocolo:** TCP
- **Función:** Navegación web segura
- **Vulnerabilidades:**
  - Certificados débiles
  - Ataques SSL/TLS
  - Heartbleed
- **Contramedidas:**
  - Certificados válidos
  - Configuración SSL/TLS fuerte
  - Actualizaciones regulares

### 🔧 **Puertos Registrados (1024-49151)**

#### **Puerto 1433 - Microsoft SQL Server**
- **Protocolo:** TCP
- **Función:** Base de datos
- **Vulnerabilidades:**
  - Ataques de inyección SQL
  - Credenciales por defecto
  - Buffer overflow
- **Contramedidas:**
  - Cambiar puerto por defecto
  - Autenticación fuerte
  - Firewall

#### **Puerto 3306 - MySQL**
- **Protocolo:** TCP
- **Función:** Base de datos
- **Vulnerabilidades:**
  - Ataques de inyección SQL
  - Acceso remoto no autorizado
  - Privilegios excesivos
- **Contramedidas:**
  - Restringir acceso por IP
  - Usuarios con privilegios mínimos
  - Encriptación de conexiones

#### **Puerto 3389 - RDP (Remote Desktop Protocol)**
- **Protocolo:** TCP
- **Función:** Escritorio remoto
- **Vulnerabilidades:**
  - Ataques de fuerza bruta
  - BlueKeep
  - Credenciales débiles
- **Contramedidas:**
  - Autenticación de dos factores
  - Cambiar puerto por defecto
  - VPN

#### **Puerto 5432 - PostgreSQL**
- **Protocolo:** TCP
- **Función:** Base de datos
- **Vulnerabilidades:**
  - Ataques de inyección SQL
  - Configuraciones débiles
  - Acceso no autorizado
- **Contramedidas:**
  - Configuración de seguridad
  - Autenticación fuerte
  - Logs de auditoría

### 🔄 **Puertos Dinámicos (49152-65535)**
- Usados para conexiones temporales
- Asignados dinámicamente por el sistema
- No tienen servicios fijos asociados

## 🛡️ Análisis de Seguridad por Puerto

### ⚠️ **Puertos Críticos**

#### **Puertos de Administración**
- **22 (SSH):** Acceso remoto
- **23 (Telnet):** Acceso inseguro
- **3389 (RDP):** Escritorio remoto
- **5900 (VNC):** Escritorio remoto

#### **Puertos de Base de Datos**
- **1433 (SQL Server):** Base de datos Microsoft
- **3306 (MySQL):** Base de datos MySQL
- **5432 (PostgreSQL):** Base de datos PostgreSQL
- **1521 (Oracle):** Base de datos Oracle

#### **Puertos de Servicios Web**
- **80 (HTTP):** Servidor web
- **443 (HTTPS):** Servidor web seguro
- **8080 (HTTP Alt):** Servidor web alternativo
- **8443 (HTTPS Alt):** Servidor web seguro alternativo

### 🔍 **Técnicas de Escaneo de Puertos**

#### **Escaneo TCP Connect**
```bash
nmap -sT 192.168.1.1
```
- Establece conexión completa
- Detectado fácilmente
- Más lento

#### **Escaneo TCP SYN (Stealth)**
```bash
nmap -sS 192.168.1.1
```
- No completa la conexión
- Menos detectable
- Requiere privilegios de root

#### **Escaneo UDP**
```bash
nmap -sU 192.168.1.1
```
- Para servicios UDP
- Más lento que TCP
- Menos confiable

#### **Escaneo de Versiones**
```bash
nmap -sV 192.168.1.1
```
- Identifica versiones de servicios
- Más lento
- Más información

## 🧪 Ejercicios Prácticos

### 📝 **Ejercicio 1: Identificación de Servicios**
Usando nmap, identifica los servicios en tu red local:
```bash
nmap -sS -sV 192.168.1.0/24
```

### 📝 **Ejercicio 2: Análisis de Vulnerabilidades**
Para cada puerto abierto encontrado:
1. Identifica el servicio
2. Investiga vulnerabilidades comunes
3. Propón contramedidas

### 📝 **Ejercicio 3: Configuración de Firewall**
Configura un firewall para:
1. Bloquear puertos innecesarios
2. Restringir acceso a puertos críticos
3. Implementar logging

### 📝 **Ejercicio 4: Monitoreo de Puertos**
Implementa monitoreo para:
1. Detectar escaneos de puertos
2. Alertar sobre puertos abiertos inesperados
3. Registrar intentos de acceso

## 🛠️ Herramientas de Análisis

### 🔍 **Herramientas de Escaneo**
- **nmap:** Escaneo de puertos y servicios
- **masscan:** Escaneo rápido de puertos
- **netcat:** Análisis manual de puertos
- **telnet:** Prueba de conectividad

### 📊 **Herramientas de Monitoreo**
- **netstat:** Estadísticas de conexiones
- **ss:** Información de sockets
- **lsof:** Archivos abiertos por proceso
- **tcpdump:** Captura de tráfico

### 🛡️ **Herramientas de Seguridad**
- **fail2ban:** Protección contra ataques
- **iptables:** Firewall de Linux
- **ufw:** Firewall simplificado
- **snort:** IDS/IPS

## 📚 Referencias

### 📖 **Documentación Oficial**
- [IANA Port Numbers](https://www.iana.org/assignments/service-names-port-numbers/)
- [RFC 6335 - Service Name and Port Number Procedures](https://tools.ietf.org/html/rfc6335)
- [Nmap Documentation](https://nmap.org/docs.html)

### 🌐 **Recursos Online**
- [Common Ports - Wikipedia](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)
- [Port Security Best Practices](https://www.sans.org/reading-room/whitepapers/firewalls/port-security-best-practices-33249)

### 🛠️ **Herramientas Prácticas**
- **Nmap:** https://nmap.org/
- **Masscan:** https://github.com/robertdavidgraham/masscan
- **Netcat:** http://netcat.sourceforge.net/

## ✅ Evaluación

### 📋 **Preguntas de Repaso**
1. ¿Cuál es la diferencia entre puertos TCP y UDP?
2. ¿Por qué el puerto 22 es crítico para la seguridad?
3. ¿Qué vulnerabilidades son comunes en el puerto 21?
4. ¿Cómo se puede proteger el puerto 3389?
5. ¿Qué herramientas usarías para escanear puertos?

### 🎯 **Objetivos de Competencia**
- [ ] Identificar puertos comunes y sus servicios
- [ ] Analizar vulnerabilidades por puerto
- [ ] Realizar escaneo ético de puertos
- [ ] Implementar contramedidas de seguridad
- [ ] Usar herramientas de análisis de puertos

### 📊 **Proyecto Práctico**
Desarrolla un script que:
1. Escanee una red específica
2. Identifique servicios por puerto
3. Analice vulnerabilidades conocidas
4. Genere un reporte de seguridad
5. Proponga recomendaciones

---

**Próximo módulo:** [Direccionamiento IP](direccionamiento-ip.md)
