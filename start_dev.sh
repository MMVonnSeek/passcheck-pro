#!/bin/bash
echo "🚀 Iniciando ambiente de desenvolvimento PassCheck Pro"
echo "=================================================="

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ativa ambiente virtual
echo -e "${YELLOW}📦 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Mata processos nas portas
echo -e "${YELLOW}🛑 Limpando portas...${NC}"
fuser -k 5001/tcp 2>/dev/null
fuser -k 3000/tcp 2>/dev/null

# Inicia API em background
echo -e "${GREEN}🔥 Iniciando API na porta 5001...${NC}"
python api/app.py > api.log 2>&1 &
API_PID=$!

# Aguarda API iniciar
echo "⏳ Aguardando API inicializar..."
sleep 3

# Verifica se API está rodando
if curl -s http://localhost:5001/health > /dev/null; then
    echo -e "${GREEN}✅ API rodando!${NC}"
else
    echo -e "${RED}❌ API não respondeu. Verifique api.log${NC}"
    cat api.log
    exit 1
fi

# Inicia front-end
echo -e "${GREEN}🎨 Iniciando Front-end na porta 3000...${NC}"
python serve_frontend.py

# Quando front-end for encerrado, mata a API
kill $API_PID 2>/dev/null
