from typing import List, Dict, Any
from google.adk.tools import FunctionTool
from utils.database import DatabaseManager

def retrieve_strategy(emotion: str, intensity: int = 5) -> str:
    """
    Retrieves a coping strategy relevant to the user's emotion.
    
    Args:
        emotion: The primary emotion the user is feeling (e.g., "anxious", "sad").
        intensity: The intensity of the emotion (1-10).
        
    Returns:
        A string containing the name, description, and steps of a recommended strategy.
    """
    db = DatabaseManager()
    strategies = db.get_all_strategies()
    
    # Simple keyword matching for now (MVP)
    # In a full RAG system, this would use vector similarity
    relevant_strategies = []
    for strategy in strategies:
        # Check if emotion matches category or description
        if (emotion.lower() in strategy['category'].lower() or 
            emotion.lower() in strategy['description'].lower()):
            relevant_strategies.append(strategy)
            
    if not relevant_strategies:
        # Fallback to general strategies if no specific match
        relevant_strategies = [s for s in strategies if s['category'].lower() == 'general']
        
    if not relevant_strategies:
        return "I couldn't find a specific strategy for that, but deep breathing is always a good start."

    # Return the first match for simplicity
    selected = relevant_strategies[0]
    steps_str = "\n".join([f"{i+1}. {step}" for i, step in enumerate(selected['steps'])])
    
    return f"Strategy: {selected['name']}\n\n{selected['description']}\n\nSteps:\n{steps_str}"

# Create the ADK FunctionTool
retrieve_strategy_tool = FunctionTool(retrieve_strategy)