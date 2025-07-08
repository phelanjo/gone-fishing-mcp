import openai
from ..core.config import OPENAI_API_KEY, OPENAI_MODEL

class LLMService:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI()
        self.model = OPENAI_MODEL

    def ask_mr_robot(self, role_messages: list) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=role_messages,
                temperature=0.7,
                max_completion_tokens=500
            )
        except Exception as e:
            return {"error": str(e)}
        
        return response.choices[0].message.content
        
    
try:
    llm_service = LLMService()
except Exception:
    llm_service = None
