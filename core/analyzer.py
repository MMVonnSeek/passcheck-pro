"""
Analisador principal que orquestra todas as heurísticas.
"""
from typing import Dict, Any, List
from .heuristics.entropy import EntropyHeuristic
from .heuristics.keyboard_patterns import KeyboardPatternHeuristic

class PasswordAnalyzer:
    """
    Classe que coordena a análise de senhas usando múltiplas heurísticas.
    """
    
    def __init__(self, personal_info: Dict[str, str] = None):
        """
        Inicializa o analisador com as heurísticas disponíveis.
        
        Args:
            personal_info: Informações pessoais para análise contextual
        """
        self.personal_info = personal_info or {}
        self.heuristics = [
            EntropyHeuristic(),
            KeyboardPatternHeuristic()
            # Mais heurísticas serão adicionadas depois
        ]
    
    def analyze(self, password: str) -> Dict[str, Any]:
        """
        Executa todas as heurísticas na senha fornecida.
        
        Args:
            password: A senha a ser analisada
            
        Returns:
            Dicionário com resultados completos da análise
        """
        # Validações básicas
        if not password:
            return self._empty_password_result()
        
        if len(password) > 128:
            return self._too_long_result()
        
        # Executa cada heurística
        results = {}
        total_score = 0
        all_feedback = []
        
        for heuristic in self.heuristics:
            heuristic_name = heuristic.__class__.__name__
            
            try:
                result = heuristic.analyze(password)
                results[heuristic_name] = result
                total_score += result.get('score', 0)
                
                # Coleta feedback
                feedback = result.get('feedback', [])
                if isinstance(feedback, list):
                    all_feedback.extend(feedback)
                    
            except Exception as e:
                # Tratamento robusto de erros
                results[heuristic_name] = {
                    "error": str(e),
                    "score": 0,
                    "feedback": [f"Erro na análise: {str(e)}"]
                }
                all_feedback.append(f"⚠️ Erro em {heuristic_name}: análise incompleta")
        
        # Calcula score médio
        if self.heuristics:
            avg_score = total_score // len(self.heuristics)
        else:
            avg_score = 0
        
        # Classifica a força
        strength = self._classify_strength(avg_score)
        
        # Remove duplicatas do feedback
        unique_feedback = []
        for msg in all_feedback:
            if msg not in unique_feedback:
                unique_feedback.append(msg)
        
        return {
            "score": avg_score,
            "strength": strength,
            "feedback": unique_feedback[:5],  # Limita a 5 itens
            "details": results,
            "password_length": len(password),
            "heuristics_used": len(self.heuristics)
        }
    
    def _empty_password_result(self) -> Dict[str, Any]:
        """Retorna resultado para senha vazia"""
        return {
            "score": 0,
            "strength": "Inválida",
            "feedback": ["❌ A senha não pode estar vazia!"],
            "details": {},
            "password_length": 0,
            "heuristics_used": 0
        }
    
    def _too_long_result(self) -> Dict[str, Any]:
        """Retorna resultado para senha muito longa"""
        return {
            "score": 0,
            "strength": "Inválida",
            "feedback": ["❌ Senha muito longa (máximo 128 caracteres)"],
            "details": {},
            "password_length": 129,
            "heuristics_used": 0
        }
    
    def _classify_strength(self, score: int) -> str:
        """Classifica a força baseada no score"""
        if score < 20:
            return "🔴 Muito Fraca"
        elif score < 40:
            return "🟠 Fraca"
        elif score < 60:
            return "🟡 Moderada"
        elif score < 80:
            return "🟢 Forte"
        else:
            return "🟣 Muito Forte"
