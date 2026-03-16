"""
Heurística baseada em entropia de Shannon.
"""
from .base import BaseHeuristic
import math

class EntropyHeuristic(BaseHeuristic):
    """
    Avalia a senha baseado na entropia (aleatoriedade) da mesma.
    """
    
    def analyze(self, password: str) -> dict:
        """
        Calcula a entropia e dá um score baseado nela.
        """
        if not password:
            return {
                "score": 0,
                "feedback": ["Senha vazia não é permitida."],
                "entropy_bits": 0
            }
        
        # Calcula entropia real
        entropy = self._calculate_entropy(password)
        
        # Tamanho do conjunto de caracteres
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(not c.isalnum() for c in password):
            charset_size += 32  # Símbolos comuns
        
        # Entropia máxima possível para este charset e tamanho
        max_entropy = math.log2(charset_size) * len(password) if charset_size > 0 else 0
        
        # Score baseado na razão entre entropia real e máxima
        if max_entropy > 0:
            ratio = entropy / max_entropy
            score = min(100, int(ratio * 100))
        else:
            score = 0
        
        # Feedback baseado na entropia
        feedback = []
        if entropy < 2:
            feedback.append("❌ Entropia muito baixa! Senha extremamente previsível.")
        elif entropy < 3:
            feedback.append("⚠️ Entropia baixa. Adicione mais variedade de caracteres.")
        elif entropy < 4:
            feedback.append("👍 Entropia moderada. Pode melhorar com mais caracteres especiais.")
        else:
            feedback.append("✅ Boa entropia! A senha tem boa aleatoriedade.")
        
        return {
            "score": score,
            "feedback": feedback,
            "entropy_bits": round(entropy, 2),
            "charset_size": charset_size,
            "max_possible_entropy": round(max_entropy, 2)
        }
