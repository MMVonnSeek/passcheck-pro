"""
API REST para o analisador de senhas.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.analyzer import PasswordAnalyzer

app = Flask(__name__)
CORS(app)  # Permite requisições de frontends

@app.route('/', methods=['GET'])
def home():
    """Página inicial da API"""
    return jsonify({
        "name": "PassCheck Pro API",
        "version": "1.0.0",
        "description": "API avançada para análise de força de senhas",
        "endpoints": {
            "/health": "Verifica se a API está funcionando",
            "/analyze": "POST - Analisa uma senha (envie JSON com 'password')",
            "/analyze-with-context": "POST - Analisa com informações pessoais"
        },
        "author": "Seu Nome",
        "github": "https://github.com/seu-usuario/passcheck-pro"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint principal para análise de senhas.
    
    Espera um JSON:
    {
        "password": "senha_a_analisar"
    }
    """
    try:
        # Validação do JSON
        if not request.is_json:
            return jsonify({
                "error": "Content-Type deve ser application/json",
                "status": 400
            }), 400
        
        data = request.get_json()
        
        # Validação do campo password
        if not data or 'password' not in data:
            return jsonify({
                "error": "Campo 'password' é obrigatório",
                "status": 400
            }), 400
        
        password = data['password']
        
        # Validação adicional
        if not isinstance(password, str):
            return jsonify({
                "error": "Password deve ser uma string",
                "status": 400
            }), 400
        
        # Executa análise
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze(password)
        
        # Adiciona metadata
        result["timestamp"] = __import__('datetime').datetime.now().isoformat()
        result["api_version"] = "1.0.0"
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Erro interno no servidor: {str(e)}",
            "status": 500
        }), 500

@app.route('/analyze-with-context', methods=['POST'])
def analyze_with_context():
    """
    Endpoint para análise considerando contexto pessoal.
    
    Espera um JSON:
    {
        "password": "senha_a_analisar",
        "personal_info": {
            "name": "João Silva",
            "birth": "1990",
            "email": "joao@email.com"
        }
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type deve ser application/json"}), 400
        
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({"error": "Campo 'password' é obrigatório"}), 400
        
        password = data['password']
        personal_info = data.get('personal_info', {})
        
        # Valida o tipo das informações pessoais
        if not isinstance(personal_info, dict):
            return jsonify({"error": "personal_info deve ser um objeto JSON"}), 400
        
        # Executa análise com contexto
        analyzer = PasswordAnalyzer(personal_info)
        result = analyzer.analyze(password)
        
        result["timestamp"] = __import__('datetime').datetime.now().isoformat()
        result["api_version"] = "1.0.0"
        result["context_used"] = bool(personal_info)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    # Em produção, use debug=False
    app.run(host='0.0.0.0', port=5001, debug=True)
