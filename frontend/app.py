import sys
import os
# Ensure the backend module is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.ai_orchestrator import refine_user_input, get_activity_suggestions, generate_itinerary


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for user inputs
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {
        "destination": None,
        "dates": None,
        "budget": None,
        "preferences": None,
        "walking_tolerance": None,
        "dietary_preferences": None,
        "accommodation": None
    }

st.title("🗺️ AI Travel Itinerary Generator")
st.markdown("Welcome! This is a prototype of a smart AI travel planner that helps you create the perfect itinerary for your journey.")
st.markdown(" Where are you traveling to? or Planning to travel to?")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Step 1: Ask for the destination
if not st.session_state.user_inputs["destination"]:
    user_input = st.chat_input("Hello! I'm your AI travel assistant. Where are you traveling to?")
    if user_input:
        st.session_state.user_inputs["destination"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "Great! What are your travel dates? (e.g., 2025-01-25 to 2025-02-01)"})
        st.rerun()

# Step 2: Ask for travel dates
elif not st.session_state.user_inputs["dates"]:
    user_input = st.chat_input("What are your travel dates? (e.g., 2025-01-25 to 2025-02-01)")
    if user_input:
        st.session_state.user_inputs["dates"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "What is your budget? (Low, Medium, or High)"})
        st.rerun()

# Step 3: Ask for budget
elif not st.session_state.user_inputs["budget"]:
    user_input = st.chat_input("What is your budget? (Low, Medium, or High)")
    if user_input:
        st.session_state.user_inputs["budget"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "Do you have any specific interests? (e.g., nature, adventure, history)"})
        st.rerun()

# Step 4: Ask for preferences
elif not st.session_state.user_inputs["preferences"]:
    user_input = st.chat_input("Do you have any specific interests? (e.g., nature, adventure, history)")
    if user_input:
        st.session_state.user_inputs["preferences"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "Do you have any dietary preferences? (Vegetarian, Vegan, Gluten-free, etc.)"})
        st.rerun()

# Step 5: Ask for dietary preferences
elif not st.session_state.user_inputs["dietary_preferences"]:
    user_input = st.chat_input("Do you have any dietary preferences? (Vegetarian, Vegan, Gluten-free, etc.)")
    if user_input:
        st.session_state.user_inputs["dietary_preferences"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "What type of accommodation do you prefer? (Hotel, Hostel, Airbnb, Camping)"})
        st.rerun()

# Step 6: Ask for accommodation type
elif not st.session_state.user_inputs["accommodation"]:
    user_input = st.chat_input("What type of accommodation do you prefer? (Hotel, Hostel, Airbnb, Camping)")
    if user_input:
        st.session_state.user_inputs["accommodation"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": "How much walking are you comfortable with? (Low, Moderate, High)"})
        st.rerun()

# Step 7: Ask for walking tolerance
elif not st.session_state.user_inputs["walking_tolerance"]:
    user_input = st.chat_input("How much walking are you comfortable with? (Low, Moderate, High)")
    if user_input:
        st.session_state.user_inputs["walking_tolerance"] = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Input Refinement
        refined_inputs = refine_user_input(
            st.session_state.user_inputs["destination"],
            st.session_state.user_inputs["dates"],
            st.session_state.user_inputs["budget"],
            st.session_state.user_inputs["preferences"]
        )
        st.session_state.messages.append({"role": "assistant", "content": f"Refined your inputs: {refined_inputs}"})

        # Next step: Activity Suggestions
        st.session_state.messages.append({"role": "assistant", "content": "Now, let me find some activities for you..."})
        st.rerun()

# Step 8: Fetch Activity Suggestions
elif "activities" not in st.session_state:
    activities = get_activity_suggestions(
        st.session_state.user_inputs["destination"],
        st.session_state.user_inputs["budget"],
        st.session_state.user_inputs["preferences"],
        st.session_state.user_inputs["walking_tolerance"],
        st.session_state.user_inputs["dietary_preferences"]
    )
    st.session_state.activities = activities
    st.session_state.messages.append({"role": "assistant", "content": f"Here are some suggested activities:\n\n{activities}"})
    st.session_state.messages.append({"role": "assistant", "content": "Are you happy with these activities? Type 'yes' to proceed to itinerary generation."})
    st.rerun()

# Step 9: Generate Itinerary
elif "itinerary" not in st.session_state:
    user_input = st.chat_input("Are you happy with these activities? Type 'yes' to proceed.")
    if user_input and user_input.lower() == "yes":
        itinerary = generate_itinerary(
            5,  # Change as per user input
            st.session_state.user_inputs["destination"],
            st.session_state.user_inputs["dates"],
            st.session_state.user_inputs["budget"],
            st.session_state.user_inputs["preferences"],
            st.session_state.user_inputs["accommodation"],
            st.session_state.user_inputs["walking_tolerance"]
        )
        st.session_state.itinerary = itinerary
        st.session_state.messages.append({"role": "assistant", "content": f"Here is your itinerary:\n\n{itinerary}"})
        st.rerun()
