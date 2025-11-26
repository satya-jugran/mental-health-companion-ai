from google.adk.tools import FunctionTool
from utils.database import DatabaseManager

def analyze_mood_patterns(user_id: str = "default_user", days: int = 7) -> str:
    """
    Analyzes mood patterns over the specified number of days.
    
    Args:
        user_id: The ID of the user to analyze.
        days: Number of days to look back (default: 7).
        
    Returns:
        A summary of mood patterns and insights.
    """
    db = DatabaseManager()
    
    # Get mood entries for the period
    entries = db.get_mood_history(
        user_id=user_id,
        days=days
    )
    
    if not entries:
        return f"No mood data found for the last {days} days. Start logging your mood to see patterns!"
    
    # Calculate statistics
    mood_scores = [entry['mood_score'] for entry in entries]
    avg_mood = sum(mood_scores) / len(mood_scores)
    
    # Collect all emotions
    all_emotions = []
    for entry in entries:
        all_emotions.extend(entry.get('emotions', []))
    
    # Count emotion frequencies
    emotion_counts = {}
    for emotion in all_emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Get top 3 emotions
    top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Identify trend
    if len(mood_scores) >= 4:
        recent_avg = sum(mood_scores[-3:]) / 3
        older_avg = sum(mood_scores[:3]) / 3
        if recent_avg > older_avg + 1:
            trend = "improving"
        elif recent_avg < older_avg - 1:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient data"
    
    # Format insights
    insights = f"""
Mood Pattern Analysis (Last {days} days):

📊 Statistics:
- Total check-ins: {len(entries)}
- Average mood score: {avg_mood:.1f}/10
- Trend: {trend}

😊 Most Common Emotions:
"""
    for emotion, count in top_emotions:
        insights += f"- {emotion}: {count} times\n"
    
    insights += f"\n💡 Insight: "
    if avg_mood >= 7:
        insights += "You've been doing great overall! Keep up the positive momentum."
    elif avg_mood >= 5:
        insights += "Your mood has been moderate. Consider what activities bring you joy."
    else:
        insights += "Your mood has been lower than usual. It might help to reach out for support."
    
    return insights

# Create the ADK FunctionTool
analyze_patterns_tool = FunctionTool(analyze_mood_patterns)