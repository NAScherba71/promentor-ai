import os
import requests
import logging
from typing import Dict, List, Optional
from .base import AIProvider

logger = logging.getLogger(__name__)

class OpenRouterAIProvider(AIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model_name = os.getenv("OPENROUTER_MODEL_NAME", "google/gemini-pro-1.5")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set.")

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
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": f"{system_prompt}\n{context_str}"},
                    {"role": "user", "content": user_message}
                ]
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content']

            return {
                'message': response_text,
                'suggestions': self._extract_suggestions(response_text),
                'resources': self._recommend_resources(user_message, context),
                'model_used': f"openrouter:{self.model_name}"
            }
        except Exception as e:
            logger.error(f"OpenRouter AI chat error: {e}")
            return {
                'message': "I apologize, but I'm having trouble processing your request right now via OpenRouter.",
                'suggestions': [],
                'resources': [],
                'model_used': 'error'
            }

    def analyze_code(self, code: str, language: str) -> Dict:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": f"You are a code analysis expert. Analyze the provided {language} code."},
                    {"role": "user", "content": f"Analyze this {language} code and provide suggestions for improvement:\n\n{code}\n\nSuggestions:"}
                ]
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            response_data = response.json()
            analysis = response_data['choices'][0]['message']['content']

            return {
                'ai_analysis': analysis,
                'confidence': 0.90,
                'model_used': f"openrouter:{self.model_name}"
            }
        except Exception as e:
            logger.error(f"OpenRouter code analysis error: {e}")
            return {
                'ai_analysis': 'Unable to perform AI analysis at this time.',
                'confidence': 0.0,
                'model_used': 'error'
            }

    def _extract_suggestions(self, response_text: str) -> List[str]:
        suggestions = []
        response_lower = response_text.lower()
        if 'loop' in response_lower: suggestions.append("Consider using appropriate loop structures")
        if 'function' in response_lower: suggestions.append("Break down the problem into smaller functions")
        if 'variable' in response_lower: suggestions.append("Use descriptive variable names")
        return suggestions[:3]

    def _recommend_resources(self, user_message: str, context: Dict) -> List[Dict]:
        resources = []
        message_lower = user_message.lower()
        if any(word in message_lower for word in ['loop', 'for', 'while']):
            resources.append({'title': 'Mastering Loops', 'url': '/learn/concepts/loops', 'type': 'tutorial'})
        return resources
