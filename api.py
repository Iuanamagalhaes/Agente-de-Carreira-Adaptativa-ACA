import os
import google.generativeai as genai
from dotenv import load_dotenv

# carregar chave
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    raise ValueError("Coloque sua chave GEMINI_API_KEY no arquivo .env")

genai.configure(api_key=GEMINI_KEY)

def call_llm(prompt: str, system: str = None, model: str = "gemini-2.5-flash", temperature: float = 0.4):
    try:
        full_prompt = f"{system or ''}\n\n{prompt}"
        response = genai.GenerativeModel(model).generate_content(full_prompt)
        return {"text": response.text}
    except Exception as e:
        return {"text": f"Erro ao conectar à API Gemini: {str(e)}"}