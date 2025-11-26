from typing import List
from google.adk.tools import FunctionTool
import re

def check_crisis_indicators(mood_score: int, emotions: List[str], notes: str = "") -> str:
    """
    Checks for crisis indicators based on user input and provides appropriate resources.
    
    Args:
        mood_score: Current mood score (1-10)
        emotions: List of emotions the user is experiencing
        notes: Optional notes about the user's state
        
    Returns:
        Crisis assessment and resource information if needed.
    """
    # Define crisis keywords
    crisis_keywords = [
        'suicide', 'suicidal', 'kill myself', 'end it all', 
        'hopeless', 'no point', 'better off dead', 'harm myself'
    ]
    
    crisis_emotions = ['hopeless', 'desperate', 'trapped', 'worthless']
    
    # Check for crisis indicators
    is_crisis = False
    crisis_level = "none"
    
    # Check mood score
    if mood_score <= 2:
        crisis_level = "high"
        is_crisis = True
    elif mood_score <= 4:
        crisis_level = "moderate"
        is_crisis = True
    
    # Check for crisis emotions
    for emotion in emotions:
        if emotion.lower() in crisis_emotions:
            is_crisis = True
            if crisis_level == "none":
                crisis_level = "moderate"
    
    # Check notes for crisis keywords
    notes_lower = notes.lower()
    for keyword in crisis_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', notes_lower):
            is_crisis = True
            crisis_level = "high"
            break
    
    if not is_crisis:
        return "No immediate crisis indicators detected. Continue monitoring."
    
    # Provide appropriate response based on crisis level
    if crisis_level == "high":
        return """
⚠️ IMMEDIATE SUPPORT NEEDED ⚠️

I'm concerned about what you're experiencing. Your safety is the top priority.

🆘 **Crisis Resources (24/7):**
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

📞 **Please reach out immediately to:**
- Call 988 or your local emergency number
- Go to your nearest emergency room
- Contact a trusted friend or family member
- Reach out to a mental health professional

💙 Remember: You don't have to face this alone. Help is available, and things can get better.
"""
    else:  # moderate
        return """
🤝 Support Resources Available

I notice you're going through a difficult time. It's important to reach out for support.

💬 **Recommended Actions:**
- Talk to a trusted friend or family member
- Contact your therapist or healthcare provider
- Use a crisis support line if you need immediate help

📞 **Support Lines:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741

🌟 **Self-Care Reminders:**
- You're taking a brave step by expressing how you feel
- Difficult emotions are temporary
- Professional support can make a real difference

Would you like to talk about what's troubling you?
"""

# Create the ADK FunctionTool
check_crisis_tool = FunctionTool(check_crisis_indicators)