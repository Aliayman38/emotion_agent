import re
import time
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import Config
from app.schemas import LLMEmotionOutput
from app.prompts import SYSTEM_PROMPT
from app.logger import logger

def normalize_arabic_text(text: str) -> str:
    """
    Cleans and normalizes Arabic input text variants, reducing repetitive 
    characters and removing computational noise.
    """
    # 1. Remove Arabic Harakat (Tashkeel)
    harakat_pattern = re.compile(r'[\u064B-\u0652]')
    text = re.sub(harakat_pattern, '', text)
    
    # 2. Remove Tatweel (Kashida)
    text = re.sub(r'\u0640', '', text)
    
    # 3. Normalize Alef variants to bare Alef
    text = re.sub(r'[أإآ]', 'ا', text)
    
    # 4. Normalize Taa Marbuta to Haa (common in informal text)
    text = re.sub(r'ة', 'ه', text)
    
    # 5. Collapse repeated characters (more than 2 identical sequential chars down to 1)
    text = re.sub(r'(.)\1+', r'\1', text)
    
    # 6. Strip unnecessary punctuation and excess whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def call_emotion_classifier_llm(text: str) -> Dict[str, Any]:
    """
    Invokes the cloud LLM via LangChain using structured output compilation 
    to retrieve strict JSON classification parameters.
    """
    start_time = time.time()
    logger.info(f"Executing EmotionClassifierTool with input: '{text}'")
    
    try:
        # Initialize LangChain Google GenAI Model
        llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.0
        )
        
        # Enforce structured output schema
        structured_llm = llm.with_structured_output(LLMEmotionOutput)
        
        messages = [
            ("system", SYSTEM_PROMPT),
            ("user", f"Classify this input text: '{text}'")
        ]
        
        response: LLMEmotionOutput = structured_llm.invoke(messages)
        execution_time = time.time() - start_time
        logger.info(f"LLM Classification executed in {execution_time:.4f}s")
        
        return {
            "emotion": response.emotion,
            "confidence": response.confidence,
            "error": None
        }
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"LLM Classification failed after {execution_time:.4f}s with error: {str(e)}")
        return {
            "emotion": "neutral",
            "confidence": 0.0,
            "error": str(e)
        }