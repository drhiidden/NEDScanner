# 🔍 Reconocimiento Pasivo

## 📚 Objetivos de Aprendizaje

- Comprender técnicas de reconocimiento pasivo
- Identificar fuentes de información pública
- Realizar OSINT (Open Source Intelligence)
- Aplicar técnicas de footprinting

## 🔍 ¿Qué es el Reconocimiento Pasivo?

Recolección de información sobre un objetivo sin interactuar directamente con sus sistemas. Se basa en fuentes públicas y no deja rastros.

### Características
- ✅ No detectable
- ✅ Legal y ético
- ✅ Información pública
- ✅ Sin interacción directa

## 🌐 Fuentes de Información

### 1. **WHOIS y Registros de Dominio**

#### Información Disponible
- Propietario del dominio
- Fechas de registro y expiración
- Servidores DNS
- Información de contacto

#### Herramientas
```bash
whois example.com
whois -H example.com
```

### 2. **Registros DNS**

#### Tipos de Registros
- **A:** Dirección IPv4
- **AAAA:** Dirección IPv6
- **MX:** Servidores de correo
- **NS:** Servidores de nombres
- **TXT:** Información de texto
- **CNAME:** Alias de dominio

#### Herramientas
```bash
nslookup example.com
dig MX example.com
dig -x 192.168.1.1
```

### 3. **Búsqueda de Subdominios**

#### Técnicas
1. Diccionarios comunes
2. Búsqueda en motores
3. Certificados SSL
4. DNS bruteforce

#### Herramientas
```bash
gobuster dns -d example.com -w wordlist.txt
sublist3r -d example.com
amass enum -d example.com
```

### 4. **Información de Redes Sociales**

#### Plataformas
- LinkedIn (empleados, estructura)
- Twitter (actividad, menciones)
- Facebook (páginas oficiales)
- GitHub (código, proyectos)

### 5. **Motores de Búsqueda**

#### Operadores Avanzados
```
site:example.com
inurl:admin
filetype:pdf
intitle:"login"
```

#### Herramientas Especializadas
- **Shodan:** Dispositivos IoT
- **Censys:** Certificados SSL
- **Google Dorks:** Búsquedas avanzadas

### 6. **Certificados SSL/TLS**

#### Información
- Dominios incluidos
- Fechas de validez
- Información de la organización

#### Herramientas
```bash
openssl s_client -connect example.com:443
censys search "parsed.subject_dn:example.com"
```

## 🛠️ Herramientas de OSINT

### 1. **Recon-ng**
Framework completo para reconocimiento
```bash
git clone https://github.com/lanmaster53/recon-ng.git
recon-ng
workspaces create example
use recon/domains-hosts/google_site_web
set SOURCE example.com
run
```

### 2. **Maltego**
Herramienta gráfica para mapeo de relaciones

### 3. **TheHarvester**
Recolección de correos y subdominios
```bash
theHarvester -d example.com -b google
theHarvester -d example.com -b linkedin
```

### 4. **SpiderFoot**
Automatización de OSINT
```bash
pip install spiderfoot
sf.py -s example.com -m sfp_whois,sfp_dns
```

## 📊 Metodología

### Fase 1: Identificación del Objetivo
1. Definir el alcance
2. Identificar dominios principales
3. Establecer límites legales

### Fase 2: Recolección de Información
1. Consultas WHOIS
2. Análisis DNS
3. Búsqueda de subdominios
4. Revisión de redes sociales

### Fase 3: Análisis y Correlación
1. Organizar información
2. Identificar patrones
3. Correlacionar datos
4. Validar información

### Fase 4: Documentación
1. Generar reporte
2. Crear diagramas
3. Identificar vectores de ataque
4. Proponer contramedidas

## 🧪 Ejercicios Prácticos

### Ejercicio 1: Análisis WHOIS
```bash
whois google.com
whois microsoft.com
whois github.com
```

### Ejercicio 2: Enumeración DNS
```bash
dig ANY example.com
for sub in www mail ftp admin blog api; do
    host $sub.example.com
done
```

### Ejercicio 3: Búsqueda en Redes Sociales
1. Busca empleados en LinkedIn
2. Analiza publicaciones en Twitter
3. Revisa repositorios en GitHub

### Ejercicio 4: Análisis de Certificados
```bash
openssl s_client -connect example.com:443 < /dev/null | openssl x509 -text
```

## ⚠️ Consideraciones Éticas

### ✅ Permitido
- Consulta de información pública
- Análisis de registros DNS
- Búsqueda en motores
- Revisión de redes sociales públicas

### ❌ Prohibido
- Acceso no autorizado
- Violación de términos de servicio
- Recolección de información privada
- Uso para actividades maliciosas

## 📚 Referencias

### Herramientas
- **Recon-ng:** https://github.com/lanmaster53/recon-ng
- **Maltego:** https://www.maltego.com/
- **TheHarvester:** https://github.com/laramies/theHarvester
- **SpiderFoot:** https://github.com/smicallef/spiderfoot

### Recursos
- **Shodan:** https://www.shodan.io/
- **Censys:** https://censys.io/
- **VirusTotal:** https://www.virustotal.com/

## ✅ Evaluación

### Preguntas de Repaso
1. ¿Qué es el reconocimiento pasivo?
2. ¿Qué información se obtiene de WHOIS?
3. ¿Cómo funcionan los registros DNS?
4. ¿Qué herramientas usarías para OSINT?
5. ¿Cuáles son las consideraciones éticas?

### Objetivos de Competencia
- [ ] Realizar consultas WHOIS
- [ ] Analizar registros DNS
- [ ] Buscar subdominios
- [ ] Usar herramientas OSINT
- [ ] Aplicar metodología ética

---

**Próximo módulo:** [Reconocimiento Activo](reconocimiento-activo.md)
