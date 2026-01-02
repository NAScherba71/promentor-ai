from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class AIProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self, 
        user_message: str, 
        context: Dict, 
        personality: str = 'encouraging'
    ) -> Dict:
        """
        Generate AI tutor response based on user input and context.
        Returns a dictionary with 'message', 'suggestions', 'resources', and 'model_used'.
        """
        pass

    @abstractmethod
    def analyze_code(
        self, 
        code: str, 
        language: str
    ) -> Dict:
        """
        Analyze code and provide suggestions for improvement.
        Returns a dictionary with 'ai_analysis', 'confidence', and 'model_used'.
        """
        pass
