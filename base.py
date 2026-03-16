"""
Classe base para todas as heurísticas de análise de senha.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import math
from collections import Counter

class BaseHeuristic(ABC):
    """
    Classe abstrata que define a interface para todas as heurísticas.
    """
    
    @abstractmethod
    def analyze(self, password: str) -> Dict[str, Any]:
        """
        Analisa a senha e retorna um dicionário com:
        - score: int (0-100) - Quanto maior, melhor a senha neste aspecto
        - feedback: list[str] - Mensagens de melhoria
        - outros detalhes específicos da heurística
        """
        pass
    
    def _calculate_entropy(self, password: str) -> float:
        """
        Método utilitário para calcular entropia (pode ser usado por várias heurísticas)
        """
        if not password:
            return 0.0
        
        entropy = 0.0
        freq = Counter(password)
        for count in freq.values():
            prob = count / len(password)
            entropy -= prob * math.log2(prob)
        
        return entropy
