import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.genai import types
from agents.orchestrator import orchestrator_agent
from agents.mood_agent import mood_tracker_agent
from agents.support_agent import support_agent
from agents.pattern_agent import pattern_analyzer_agent
from agents.crisis_agent import crisis_monitor_agent
from utils.database import DatabaseManager
from utils.profile_manager import ProfileManager
from utils.data_export import DataExporter
from ui.cli import CLI
from utils.config import DATABASE_PATH

APP_NAME = "MentalHealthCompanion"
USER_ID = "test_user_001"

async def run_agent_async():
    """Async function to handle agent runs with proper session management"""
    load_dotenv()
    
    # Initialize managers
    db = DatabaseManager()
    profile_mgr = ProfileManager()
    data_exporter = DataExporter(db)
    
    # Clear screen and show header
    CLI.clear_screen()
    CLI.print_header()
    
    # Create/load user profile
    profile = profile_mgr.get_profile(USER_ID)
    if not profile:
        profile = profile_mgr.create_profile(USER_ID, "Test User")
        db.create_user(USER_ID, "Test User")
        CLI.print_success("Welcome! Your profile has been created.")
    else:
        profile_mgr.update_last_active(USER_ID)
    
    # Show welcome message
    CLI.print_welcome(profile['name'])
    CLI.print_menu()
    CLI.show_quick_tips()
    CLI.print_divider()

    session_service_orchestrator = InMemorySessionService()
    session_service = SqliteSessionService(db_path=DATABASE_PATH) 
    
    # Create InMemoryRunners for each agent (includes session service)
    orchestrator_runner = Runner(agent=orchestrator_agent, app_name=APP_NAME, session_service=session_service_orchestrator)
    mood_runner = Runner(agent=mood_tracker_agent, app_name=APP_NAME, session_service=session_service)
    support_runner = Runner(agent=support_agent, app_name=APP_NAME, session_service=session_service)
    pattern_runner = Runner(agent=pattern_analyzer_agent, app_name=APP_NAME, session_service=session_service)
    crisis_runner = Runner(agent=crisis_monitor_agent, app_name=APP_NAME, session_service=session_service)
    
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
        user_input = CLI.get_input()
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit']:
            if CLI.confirm_exit():
                CLI.print_goodbye()
                break
            else:
                continue
        
        if user_input.lower() == 'menu':
            CLI.print_menu()
            continue
        
        if user_input.lower() == 'clear':
            CLI.clear_screen()
            CLI.print_header()
            CLI.print_menu()
            continue
        
        if user_input.lower().startswith('export'):
            # Handle data export
            parts = user_input.split()
            format_type = parts[1] if len(parts) > 1 else 'json'
            filename = f"mood_export_{USER_ID}_{datetime.now().strftime('%Y%m%d')}.{format_type}"
            
            if format_type == 'json':
                success = data_exporter.export_mood_data_json(USER_ID, filename)
            elif format_type == 'csv':
                success = data_exporter.export_mood_data_csv(USER_ID, filename)
            else:
                CLI.print_error(f"Unknown export format: {format_type}")
                continue
            
            if success:
                CLI.print_success(f"Data exported to {filename}")
            else:
                CLI.print_error("Export failed. No data available.")
            continue
        
        if not user_input.strip():
            continue
        
        # Map command shortcuts to natural language
        command_map = {
            'mood': "I want to log my mood",
            'patterns': "Show me my mood patterns",
            'support': "I need some support and advice",
            'help': "I need help"
        }
        
        # Check if input is a command shortcut
        processed_input = command_map.get(user_input.lower(), user_input)
        
        # Create Content object for the message
        content = types.Content(role="user", parts=[types.Part(text=processed_input)])
        
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
                        if part.text is not None:
                            routing_decision += part.text
        
        target_agent_name = routing_decision.strip().replace('"', '').replace("'", "")
        
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
                            if part.text is not None:
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
                            if part.text is not None:
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
                            if part.text is not None:
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
                            if part.text is not None:
                                response += part.text
        else:
            # Fallback - use the orchestrator's response directly
            response = routing_decision
            target_agent_name = "OrchestratorAgent"
        
        # Format and print the response using CLI
        formatted_response = CLI.format_agent_response(target_agent_name, response)
        print(formatted_response)
        
        # Update user activity
        profile_mgr.update_last_active(USER_ID)

def main():
    """Main entry point that runs the async function"""
    asyncio.run(run_agent_async())

if __name__ == "__main__":
    main()