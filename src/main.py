import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import InMemoryRunner
from google.genai import types
from agents.orchestrator import orchestrator_agent
from agents.mood_agent import mood_tracker_agent
from agents.support_agent import support_agent
from agents.pattern_agent import pattern_analyzer_agent
from agents.crisis_agent import crisis_monitor_agent
from utils.database import DatabaseManager

APP_NAME = "MentalHealthCompanion"
USER_ID = "test_user_001"

async def run_agent_async():
    """Async function to handle agent runs with proper session management"""
    load_dotenv()
    
    # Initialize DB
    db = DatabaseManager()
    
    # Create a default user for testing
    if not db.get_user(USER_ID):
        db.create_user(USER_ID, "Test User")
        print(f"Created test user: {USER_ID}")
    
    print("Mental Health Support Companion (ADK Powered)")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    # Create InMemoryRunners for each agent (includes session service)
    orchestrator_runner = InMemoryRunner(agent=orchestrator_agent, app_name=APP_NAME)
    mood_runner = InMemoryRunner(agent=mood_tracker_agent, app_name=APP_NAME)
    support_runner = InMemoryRunner(agent=support_agent, app_name=APP_NAME)
    pattern_runner = InMemoryRunner(agent=pattern_analyzer_agent, app_name=APP_NAME)
    crisis_runner = InMemoryRunner(agent=crisis_monitor_agent, app_name=APP_NAME)
    
    # Create sessions for each runner (await async calls)
    orchestrator_session = await orchestrator_runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    mood_session = await mood_runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    support_session = await support_runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    pattern_session = await pattern_runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    crisis_session = await crisis_runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # Create Content object for the message
        content = types.Content(role="user", parts=[types.Part(text=user_input)])
        
        # 1. Use orchestrator to decide which agent to route to
        events = orchestrator_runner.run(
            user_id=USER_ID,
            session_id=orchestrator_session.id,
            new_message=content
        )
        
        # Collect response from events
        routing_decision = ""
        for event in events:
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        if part.text != None:
                            routing_decision += part.text
        
        target_agent_name = routing_decision.strip().replace('"', '').replace("'", "")
        print(f"[System] Routing to: {target_agent_name}")
        
        # 2. Route to the appropriate agent based on the decision
        response = ""
        if "MoodTrackerAgent" in target_agent_name:
            events = mood_runner.run(
                user_id=USER_ID,
                session_id=mood_session.id,
                new_message=content
            )
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            if part.text != None:
                                response += part.text
        elif "SupportAgent" in target_agent_name:
            events = support_runner.run(
                user_id=USER_ID,
                session_id=support_session.id,
                new_message=content
            )
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            if part.text != None:
                                response += part.text
        elif "PatternAnalyzerAgent" in target_agent_name:
            events = pattern_runner.run(
                user_id=USER_ID,
                session_id=pattern_session.id,
                new_message=content
            )
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            if part.text != None:
                                response += part.text
        elif "CrisisMonitorAgent" in target_agent_name:
            events = crisis_runner.run(
                user_id=USER_ID,
                session_id=crisis_session.id,
                new_message=content
            )
            for event in events:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            if part.text != None:
                                response += part.text
        else:
            # Fallback - use the orchestrator's response directly
            response = routing_decision
            
        print(f"Companion: {response}")

def main():
    """Main entry point that runs the async function"""
    asyncio.run(run_agent_async())

if __name__ == "__main__":
    main()