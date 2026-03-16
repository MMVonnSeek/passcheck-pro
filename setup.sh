#!/bin/bash
echo "🔧 Configurando ambiente PassCheck Pro..."

# Ativa venv
source venv/bin/activate

# Instala dependências
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install flask flask-cors pytest pytest-cov requests python-dotenv

# Cria requirements.txt
pip freeze > requirements.txt

echo "✅ Setup completo!"
echo "🚀 Para iniciar a API: python api/app.py"
