# backend.py (FastAPI server)

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from fastapi import FastAPI
from backend.ai_orchestrator import refine_user_input, get_activity_suggestions, generate_itinerary

app = FastAPI()

@app.get("/refine")
def refine(destination: str, dates: str, budget: str, preferences: str):
    return {"response": refine_user_input(destination, dates, budget, preferences)}

@app.get("/activities")
def activities(destination: str, budget: str, preferences: str, walking_tolerance: str, dietary_preferences: str):
    return {"response": get_activity_suggestions(destination, budget, preferences, walking_tolerance, dietary_preferences)}

@app.get("/itinerary")
def itinerary(num_days: int, destination: str, dates: str, budget: str, preferences: str, accommodation: str, walking_tolerance: str):
    return {"response": generate_itinerary(num_days, destination, dates, budget, preferences, accommodation, walking_tolerance)}
