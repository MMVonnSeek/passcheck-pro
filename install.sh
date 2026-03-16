#!/bin/bash
echo "📦 Instalando PassCheck Pro"
echo "=========================="

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale com: sudo apt install python3"
    exit 1
fi

# Cria ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install flask flask-cors pytest pytest-cov requests python-dotenv

# Cria requirements.txt
pip freeze > requirements.txt

# Verifica instalação
echo "✅ Instalação completa!"
echo ""
echo "🚀 Para iniciar o projeto:"
echo "   ./start_dev.sh"
echo ""
echo "📁 Estrutura criada:"
ls -la
