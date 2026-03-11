import os
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()

IS_LITE_LLM = os.getenv("IS_LITE_LLM")
LITE_LLM_MODEL_NAME = os.getenv("LITE_LLM_MODEL_NAME")
LITE_LLM_API_KEY = os.getenv("LITE_LLM_API_KEY")
GOOGLE_MODEL_NAME = os.getenv("GOOGLE_MODEL_NAME")

def get_model():
    if IS_LITE_LLM:
        return LiteLlm(
            model=LITE_LLM_MODEL_NAME,
            api_key=LITE_LLM_API_KEY,
            temperature=0.2,
            top_p=0.5,
        )
    else:
        return GOOGLE_MODEL_NAME
