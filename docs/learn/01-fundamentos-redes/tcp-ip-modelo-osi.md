# 🌐 TCP/IP y Modelo OSI

## 📚 Objetivos de Aprendizaje

Al finalizar este módulo, serás capaz de:
- Comprender la arquitectura de red TCP/IP
- Explicar las capas del modelo OSI
- Identificar las diferencias entre ambos modelos
- Aplicar estos conceptos en el contexto de ciberseguridad

## 🔍 Modelo OSI (Open Systems Interconnection)

### 📋 Descripción General

El modelo OSI es un marco conceptual que describe cómo se comunican los sistemas de red. Fue desarrollado por la ISO (International Organization for Standardization) en 1984.

### 🏗️ Las 7 Capas del Modelo OSI

#### **Capa 7: Capa de Aplicación**
- **Función:** Proporciona servicios de red a las aplicaciones del usuario
- **Protocolos:** HTTP, HTTPS, FTP, SMTP, DNS, SSH, Telnet
- **Ejemplos de Ataques:**
  - Ataques de inyección SQL
  - Cross-site scripting (XSS)
  - Ataques de fuerza bruta

#### **Capa 6: Capa de Presentación**
- **Función:** Traduce, encripta y comprime datos
- **Protocolos:** SSL/TLS, JPEG, MPEG, ASCII
- **Ejemplos de Ataques:**
  - Ataques contra SSL/TLS
  - Manipulación de formatos de archivo

#### **Capa 5: Capa de Sesión**
- **Función:** Establece, gestiona y termina conexiones entre aplicaciones
- **Protocolos:** NetBIOS, RPC, SQL
- **Ejemplos de Ataques:**
  - Session hijacking
  - Session fixation

#### **Capa 4: Capa de Transporte**
- **Función:** Proporciona comunicación confiable entre hosts
- **Protocolos:** TCP, UDP
- **Ejemplos de Ataques:**
  - SYN flood
  - TCP hijacking
  - Port scanning

#### **Capa 3: Capa de Red**
- **Función:** Determina la ruta de los datos a través de la red
- **Protocolos:** IP, ICMP, ARP, OSPF, BGP
- **Ejemplos de Ataques:**
  - IP spoofing
  - Man-in-the-middle
  - Routing attacks

#### **Capa 2: Capa de Enlace de Datos**
- **Función:** Transfiere datos entre nodos de la red
- **Protocolos:** Ethernet, PPP, Frame Relay
- **Ejemplos de Ataques:**
  - MAC flooding
  - ARP spoofing
  - VLAN hopping

#### **Capa 1: Capa Física**
- **Función:** Transmite bits a través del medio físico
- **Medios:** Cable de cobre, fibra óptica, ondas de radio
- **Ejemplos de Ataques:**
  - Wiretapping
  - Jamming
  - Eavesdropping

## 🌐 Suite de Protocolos TCP/IP

### 📋 Descripción General

TCP/IP es el conjunto de protocolos de comunicación utilizados en Internet y en la mayoría de redes informáticas.

### 🏗️ Las 4 Capas de TCP/IP

#### **Capa 4: Capa de Aplicación**
- **Corresponde a:** Capas 5, 6 y 7 del modelo OSI
- **Protocolos:**
  - **HTTP/HTTPS:** Navegación web
  - **FTP:** Transferencia de archivos
  - **SMTP/POP3/IMAP:** Correo electrónico
  - **DNS:** Resolución de nombres
  - **SSH:** Acceso remoto seguro
  - **Telnet:** Acceso remoto (inseguro)

#### **Capa 3: Capa de Transporte**
- **Corresponde a:** Capa 4 del modelo OSI
- **Protocolos:**
  - **TCP (Transmission Control Protocol):**
    - Orientado a conexión
    - Confiable y ordenado
    - Control de flujo y congestión
  - **UDP (User Datagram Protocol):**
    - No orientado a conexión
    - No confiable
    - Sin control de flujo

#### **Capa 2: Capa de Internet**
- **Corresponde a:** Capa 3 del modelo OSI
- **Protocolos:**
  - **IP (Internet Protocol):**
    - Direccionamiento lógico
    - Fragmentación de paquetes
    - Enrutamiento
  - **ICMP (Internet Control Message Protocol):**
    - Mensajes de control y error
    - Ping y traceroute
  - **ARP (Address Resolution Protocol):**
    - Mapeo IP a MAC

#### **Capa 1: Capa de Acceso a Red**
- **Corresponde a:** Capas 1 y 2 del modelo OSI
- **Funciones:**
  - Acceso al medio físico
  - Control de enlace de datos
  - Direccionamiento físico (MAC)

## 🔄 Flujo de Datos en la Red

### 📤 Proceso de Encapsulación

```
Datos de Aplicación
    ↓
+------------------+
|   Datos + Header | ← Capa de Aplicación
+------------------+
    ↓
+------------------+
| Segmento + Header| ← Capa de Transporte
+------------------+
    ↓
+------------------+
| Paquete + Header | ← Capa de Internet
+------------------+
    ↓
+------------------+
| Trama + Header   | ← Capa de Acceso a Red
+------------------+
    ↓
Bits en el medio físico
```

### 📥 Proceso de Desencapsulación

El proceso inverso ocurre en el destino, donde cada capa elimina su header correspondiente.

## 🛡️ Implicaciones de Seguridad

### ⚠️ Vulnerabilidades por Capa

#### **Capa de Aplicación**
- **Vulnerabilidades:** Inyección de código, XSS, CSRF
- **Contramedidas:** Validación de entrada, WAF, HTTPS

#### **Capa de Transporte**
- **Vulnerabilidades:** SYN flood, port scanning
- **Contramedidas:** Firewalls, IDS/IPS, rate limiting

#### **Capa de Internet**
- **Vulnerabilidades:** IP spoofing, man-in-the-middle
- **Contramedidas:** Filtrado de paquetes, VPN, IPsec

#### **Capa de Acceso a Red**
- **Vulnerabilidades:** ARP spoofing, MAC flooding
- **Contramedidas:** Port security, VLANs, 802.1X

## 🧪 Ejercicios Prácticos

### 📝 Ejercicio 1: Identificación de Capas
Identifica a qué capa del modelo OSI pertenece cada protocolo:
- HTTP
- TCP
- IP
- Ethernet
- SSL
- DNS

### 📝 Ejercicio 2: Análisis de Paquetes
Usando Wireshark, captura tráfico HTTP y analiza:
1. Headers de cada capa
2. Tamaño de los paquetes
3. Secuencia de números TCP

### 📝 Ejercicio 3: Simulación de Ataques
En un entorno controlado, simula:
1. SYN flood usando hping3
2. ARP spoofing con arpspoof
3. Port scanning con nmap

## 📚 Referencias

### 📖 Libros Recomendados
- "Computer Networks" - Andrew S. Tanenbaum
- "TCP/IP Illustrated" - W. Richard Stevens
- "Network Security Essentials" - William Stallings

### 🌐 Recursos Online
- [RFC 791 - Internet Protocol](https://tools.ietf.org/html/rfc791)
- [RFC 793 - Transmission Control Protocol](https://tools.ietf.org/html/rfc793)
- [OSI Model - Wikipedia](https://en.wikipedia.org/wiki/OSI_model)

### 🛠️ Herramientas Prácticas
- **Wireshark:** Análisis de protocolos
- **tcpdump:** Captura de paquetes
- **netstat:** Estadísticas de red
- **nmap:** Escaneo de puertos

## ✅ Evaluación

### 📋 Preguntas de Repaso
1. ¿Cuál es la diferencia entre TCP y UDP?
2. ¿Qué capa del modelo OSI maneja el direccionamiento IP?
3. ¿Cómo se relacionan las capas de TCP/IP con el modelo OSI?
4. ¿Qué vulnerabilidades son comunes en la capa de aplicación?
5. ¿Cómo funciona el proceso de encapsulación?

### 🎯 Objetivos de Competencia
- [ ] Explicar las 7 capas del modelo OSI
- [ ] Describir las 4 capas de TCP/IP
- [ ] Identificar protocolos por capa
- [ ] Analizar implicaciones de seguridad
- [ ] Usar herramientas de análisis de red

---

**Próximo módulo:** [Protocolos de Red](protocolos-red.md)
