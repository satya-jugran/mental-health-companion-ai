import uuid
from typing import List
from google.adk.tools import FunctionTool
from ..utils.database import DatabaseManager

def log_mood(user_id: str, mood_score: int, emotions: List[str], notes: str = "") -> str:
    """
    Logs the user's mood score, emotions, and notes into the database.
    
    Args:
        user_id: The ID of the user.
        mood_score: An integer from 1 to 10 representing the mood (1=worst, 10=best).
        emotions: A list of strings describing the emotions felt (e.g., ["happy", "anxious"]).
        notes: Optional notes or context about the mood.
        
    Returns:
        A confirmation message indicating success or failure.
    """
    db = DatabaseManager()
    entry_id = str(uuid.uuid4())
    # Triggers and conversation_summary are optional/empty for now
    success = db.add_mood_entry(
        entry_id=entry_id,
        user_id=user_id,
        mood_score=mood_score,
        emotions=emotions,
        triggers=[],
        notes=notes
    )
    
    if success:
        return f"Successfully logged mood score {mood_score} for user {user_id}."
    else:
        return "Failed to log mood entry due to a database error."

# Create the ADK FunctionTool
log_mood_tool = FunctionTool(log_mood)