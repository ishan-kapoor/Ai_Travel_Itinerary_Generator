# ai_orchestrator.py
import os
from dotenv import load_dotenv
from groq import Groq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from backend.prompts import SYSTEM_PROMPT, USER_PROMPT_REFINEMENT, ACTIVITY_SUGGESTIONS_PROMPT, ITINERARY_GENERATION_PROMPT

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_llm_response(prompt,chat_history=None, **kwargs):
    if chat_history and prompt in chat_history:
        return "You've already answered this. Let's proceed."

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "system", "content": prompt.format(**kwargs)}],
        temperature=0.7,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

def refine_user_input(destination, dates, budget, preferences):
    return get_llm_response(USER_PROMPT_REFINEMENT, destination=destination, dates=dates, budget=budget, preferences=preferences)

def get_activity_suggestions(destination, budget, preferences, walking_tolerance, dietary_preferences):
    return get_llm_response(ACTIVITY_SUGGESTIONS_PROMPT, destination=destination, budget=budget, preferences=preferences, walking_tolerance=walking_tolerance, dietary_preferences=dietary_preferences)

def generate_itinerary(num_days, destination, dates, budget, preferences, accommodation, walking_tolerance):
    return get_llm_response(ITINERARY_GENERATION_PROMPT, num_days=num_days, destination=destination, dates=dates, budget=budget, preferences=preferences, accommodation=accommodation, walking_tolerance=walking_tolerance)
