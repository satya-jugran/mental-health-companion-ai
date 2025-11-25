from google.adk import Agent
from google.adk.models import Model
from .mood_agent import mood_tracker_agent
from .support_agent import support_agent

# Define the Orchestrator Agent
# This agent analyzes the user's intent and routes to the appropriate specialist.
orchestrator_agent = Agent(
    model=Model(model_name="gemini-2.0-flash"),
    # We provide the other agents as tools/delegates
    # Note: In a full ADK implementation, we might use a specific Router class,
    # but for this MVP, we'll use a standard agent that can call others.
    # For simplicity in this phase, we will implement a basic routing logic in the main loop
    # or use this agent to decide which agent to call next.
    instruction="""
    You are the main orchestrator for a Mental Health Support Companion.
    Your job is to analyze the user's input and decide which specialized agent should handle it.
    
    - If the user wants to log their mood, talk about their day, or check in, route to the 'MoodTrackerAgent'.
    - If the user is asking for help, advice, coping strategies, or expressing distress, route to the 'SupportAgent'.
    - If the input is a greeting or unclear, ask for clarification or guide them to one of the above options.
    
    Output the name of the agent to route to: "MoodTrackerAgent" or "SupportAgent".
    """
)