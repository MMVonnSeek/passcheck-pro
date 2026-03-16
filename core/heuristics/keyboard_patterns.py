"""
Heurística para detectar padrões de teclado.
"""
from .base import BaseHeuristic

class KeyboardPatternHeuristic(BaseHeuristic):
    """
    Detecta padrões comuns como qwerty, asdf, 12345, etc.
    """
    
    def __init__(self):
        # Padrões comuns em teclados (QWERTY)
        self.keyboard_patterns = [
            "qwertyuiop", "asdfghjkl", "zxcvbnm",  # Linhas do QWERTY
            "qwerty", "asdf", "zxcv",  # Sequências comuns
            "1234567890", "123456", "12345678", "123456789",  # Números
            "!@#$%^&*()",  # Símbolos em sequência
            "q1w2e3r4t5", "a1s2d3f4", "z1x2c3v4",  # Misturas comuns
            "password", "senha", "admin", "1234", "abcd",  # Palavras muito comuns
            "abc123", "pass", "qwerty123", "admin123"  # Combinações comuns
        ]
        
        # Padrões reversos também são comuns
        self.all_patterns = []
        for pattern in self.keyboard_patterns:
            self.all_patterns.append(pattern)
            self.all_patterns.append(pattern[::-1])
    
    def analyze(self, password: str) -> dict:
        """
        Verifica se a senha contém padrões de teclado.
        """
        password_lower = password.lower()
        score_penalty = 0
        feedback = []
        patterns_found = []
        
        # Verifica cada padrão
        for pattern in self.all_patterns:
            if len(pattern) < 4:  # Padrões muito curtos não são tão relevantes
                continue
                
            if pattern in password_lower:
                # Penalidade baseada no tamanho do padrão encontrado
                penalty = len(pattern) * 5
                score_penalty += penalty
                patterns_found.append(pattern)
                
                if len(pattern) >= 8:
                    feedback.append(f"❌ Padrão de teclado longo detectado: '{pattern}'. Isso é extremamente fraco!")
                elif len(pattern) >= 5:
                    feedback.append(f"⚠️ Padrão de teclado detectado: '{pattern}'. Evite sequências óbvias.")
                else:
                    feedback.append(f"ℹ️ Pequeno padrão detectado: '{pattern}'. Considere evitar.")
        
        # Verifica caracteres repetidos (ex: aaaaa)
        for i in range(len(password) - 3):
            if len(set(password[i:i+4])) == 1:  # 4 caracteres iguais
                score_penalty += 30
                patterns_found.append(f"'{password[i:i+4]}' (repetido)")
                feedback.append("❌ Muitos caracteres repetidos! Evite repetições.")
                break
        
        # Score final (quanto maior a penalidade, menor o score)
        final_score = max(0, 100 - score_penalty)
        
        # Se não encontrou padrões, feedback positivo
        if not patterns_found:
            feedback.append("✅ Nenhum padrão de teclado óbvio encontrado.")
        
        return {
            "score": final_score,
            "feedback": feedback[:3],  # Limita a 3 mensagens
            "patterns_found": patterns_found,
            "penalty": score_penalty
        }
