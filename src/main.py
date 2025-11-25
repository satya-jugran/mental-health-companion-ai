import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import orchestrator_agent
from agents.mood_agent import mood_tracker_agent
from agents.support_agent import support_agent
from utils.database import DatabaseManager

def main():
    load_dotenv()
    
    # Initialize DB
    db = DatabaseManager()
    
    # Create a default user for testing
    user_id = "test_user_001"
    if not db.get_user(user_id):
        db.create_user(user_id, "Test User")
        print(f"Created test user: {user_id}")
    
    print("Mental Health Support Companion (ADK Powered)")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # 1. Orchestrator decides which agent to use
        # Note: In a real ADK app, this might be a single run() call on a RouterAgent.
        # Here we simulate the routing for clarity and control.
        routing_decision = orchestrator_agent.query(user_input)
        target_agent_name = routing_decision.strip().replace('"', '').replace("'", "")
        
        print(f"[System] Routing to: {target_agent_name}")
        
        if "MoodTrackerAgent" in target_agent_name:
            response = mood_tracker_agent.query(user_input)
        elif "SupportAgent" in target_agent_name:
            response = support_agent.query(user_input)
        else:
            # Fallback or direct response from orchestrator
            response = routing_decision
            
        print(f"Companion: {response}")

if __name__ == "__main__":
    main()