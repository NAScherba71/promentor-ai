import logging
from typing import Dict, List, Optional
from .base import AIProvider
from models import get_custom_tutor, get_custom_analyzer


logger = logging.getLogger(__name__)

class LocalAIProvider(AIProvider):
    def __init__(self):
        self.tutor = get_custom_tutor()
        self.analyzer = get_custom_analyzer()

    def generate_chat_response(
        self, 
        user_message: str, 
        context: Dict, 
        personality: str = 'encouraging'
    ) -> Dict:
        try:
            # Re-using the logic from CustomAITutor in models.py
            return self.tutor.generate_response(user_message, context, personality)
        except Exception as e:
            logger.error(f"Local AI tutor error: {e}")
            return {
                'message': "I apologize, but I'm having trouble processing your request with the local model.",
                'suggestions': [],
                'resources': [],
                'model_used': 'error'
            }

    def analyze_code(self, code: str, language: str) -> Dict:
        try:
            # Re-using the logic from CustomCodeAnalyzer in models.py
            return self.analyzer.analyze_with_ai(code, language)
        except Exception as e:
            logger.error(f"Local AI code analysis error: {e}")
            return {
                'ai_analysis': 'Unable to perform local AI analysis at this time.',
                'confidence': 0.0,
                'model_used': 'error'
            }
