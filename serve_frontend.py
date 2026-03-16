#!/usr/bin/env python3
"""
Servidor simples para servir o front-end durante desenvolvimento.
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIRECTORY = "frontend"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Front-end rodando em http://localhost:{PORT}")
        print(f"📁 Servindo arquivos de: {os.path.abspath(DIRECTORY)}")
        print("🔒 Certifique-se que a API está rodando em http://localhost:5001")
        print("⚠️  Pressione Ctrl+C para parar o servidor")
        
        # Abre o navegador automaticamente
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor encerrado.")

if __name__ == "__main__":
    main()
