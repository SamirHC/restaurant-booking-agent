from langchain_openai import ChatOpenAI

from ai.langauge_model import LanguageModel


class OpenAILanguageModel(LanguageModel):
    def __init__(self, model_name="gpt-4o", temperature=0.0):
        self.client = ChatOpenAI(model=model_name, temperature=temperature)
    
    def chat(self, prompt: str) -> str:
        response = self.client.invoke(prompt)
        return response.content
