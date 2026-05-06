#!/bin/bash

# give-back.sh — Auto-star script para NEDScanner
# Si el setup fue exitoso, pregunta al usuario si quiere dar una estrella al repo

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎁 NEDScanner — Give Back${NC}"
echo ""

# 1. Verificar que estamos en Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ NEDScanner solo funciona en Linux.${NC}"
    exit 1
fi

echo "✅ OS: Linux detected"

# 2. Verificar que Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 no encontrado. Instala Python 3.10+ primero."
    exit 1
fi

echo "✅ Python 3 instalado"

# 3. Verificar que Nmap está instalado
if ! command -v nmap &> /dev/null; then
    echo "⚠️  nmap no encontrado. NEDScanner necesita Nmap para escanear."
    echo "   Instala con: sudo apt install nmap"
    exit 1
fi

echo "✅ Nmap instalado"

# 4. Verificar capabilities (opcional, pero recomendado)
PYTHON_CAP=$(getcap $(which python3) 2>/dev/null || echo "")
NMAP_CAP=$(getcap $(which nmap) 2>/dev/null || echo "")

if [[ -z "$PYTHON_CAP" ]] || [[ -z "$NMAP_CAP" ]]; then
    echo -e "${YELLOW}⚠️  Capabilities no configuradas. Es recomendable configurarlas:${NC}"
    echo "   sudo setcap cap_net_raw,cap_net_admin+eip \$(which python3)"
    echo "   sudo setcap cap_net_raw,cap_net_admin+eip \$(which nmap)"
    echo ""
else
    echo "✅ Capabilities configuradas"
fi

# 5. Verificar que gh CLI está instalado
if ! command -v gh &> /dev/null; then
    echo "⚠️  gh CLI no encontrado. Necesitas instalarlo para dar estrella automáticamente."
    echo ""
    echo "Opciones:"
    echo "  1. Instalar gh: https://cli.github.com/"
    echo "  2. Dar estrella manualmente: https://github.com/drhiidden/NEDScanner"
    exit 0
fi

# 6. Verificar que gh está autenticado
if ! gh auth status &> /dev/null; then
    echo "⚠️  gh CLI no está autenticado."
    echo ""
    echo "Ejecuta: gh auth login"
    echo "Luego vuelve a ejecutar este script."
    exit 1
fi

# 7. Preguntar al usuario
echo ""
echo "✅ NEDScanner está configurado correctamente."
echo ""
echo "Si te gustó la herramienta, considera darle una estrella en GitHub."
echo "Ayuda a que más gente descubra el proyecto."
echo ""
read -p "¿Quieres dar una estrella ahora? (s/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[SsYy]$ ]]; then
    echo ""
    echo "⭐ Dando estrella a drhiidden/NEDScanner..."
    
    if gh repo star drhiidden/NEDScanner 2>&1 | grep -q "already starred"; then
        echo -e "${YELLOW}Ya habías dado estrella antes. ¡Gracias!${NC}"
    else
        echo -e "${GREEN}✅ ¡Estrella dada! Gracias por tu apoyo.${NC}"
    fi
else
    echo ""
    echo "No hay problema. Si cambias de opinión:"
    echo "  → https://github.com/drhiidden/NEDScanner"
    echo ""
    echo "¡Gracias por usar NEDScanner!"
fi
