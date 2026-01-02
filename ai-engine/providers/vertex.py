import os
import logging
from typing import Dict, List, Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from .base import AIProvider

logger = logging.getLogger(__name__)

class VertexAIProvider(AIProvider):
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            logger.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI might fail if ADC is not configured properly.")
        
        vertexai.init(project=project_id, location=location)
        self.model_name = os.getenv("VERTEX_MODEL_NAME", "gemini-1.5-pro")
        self.model = GenerativeModel(self.model_name)
        
        self.personality_prompts = {
            'encouraging': "You are an encouraging and supportive programming tutor. Always stay positive and help students build confidence.",
            'analytical': "You are a precise and analytical programming tutor. Focus on logical problem-solving and detailed explanations.",
            'creative': "You are a creative and innovative programming tutor. Encourage out-of-the-box thinking and creative solutions.",
            'practical': "You are a practical and results-oriented programming tutor. Focus on real-world applications and industry best practices."
        }

    def generate_chat_response(
        self, 
        user_message: str, 
        context: Dict, 
        personality: str = 'encouraging'
    ) -> Dict:
        try:
            system_prompt = self.personality_prompts.get(personality, self.personality_prompts['encouraging'])
            context_str = f"Context: {context.get('current_topic', 'general programming')}"
            
            prompt = f"{system_prompt}\n{context_str}\n\nUser: {user_message}\nAssistant:"
            
            response = self.model.generate_content(prompt)
            response_text = response.text

            return {
                'message': response_text,
                'suggestions': self._extract_suggestions(response_text),
                'resources': self._recommend_resources(user_message, context),
                'model_used': self.model_name
            }
        except Exception as e:
            logger.error(f"Vertex AI chat error: {e}")
            return {
                'message': "I apologize, but I'm having trouble processing your request right now.",
                'suggestions': [],
                'resources': [],
                'model_used': 'error'
            }

    def analyze_code(self, code: str, language: str) -> Dict:
        try:
            prompt = f"Analyze this {language} code and provide suggestions for improvement:\n\n{code}\n\nSuggestions:"
            
            response = self.model.generate_content(prompt)
            analysis = response.text

            return {
                'ai_analysis': analysis,
                'confidence': 0.95,
                'model_used': self.model_name
            }
        except Exception as e:
            logger.error(f"Vertex AI code analysis error: {e}")
            return {
                'ai_analysis': 'Unable to perform AI analysis at this time.',
                'confidence': 0.0,
                'model_used': 'error'
            }

    def _extract_suggestions(self, response_text: str) -> List[str]:
        # Simple extraction logic similar to models.py
        suggestions = []
        response_lower = response_text.lower()
        if 'loop' in response_lower: suggestions.append("Consider using appropriate loop structures")
        if 'function' in response_lower: suggestions.append("Break down the problem into smaller functions")
        if 'variable' in response_lower: suggestions.append("Use descriptive variable names")
        return suggestions[:3]

    def _recommend_resources(self, user_message: str, context: Dict) -> List[Dict]:
        # Simple recommendation logic similar to models.py
        resources = []
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['loop', 'for', 'while']):
            resources.append({'title': 'Mastering Loops', 'url': '/learn/concepts/loops', 'type': 'tutorial'})
        return resources
