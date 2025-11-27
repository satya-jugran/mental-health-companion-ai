# Demo Scenarios - Mental Health Support Companion

This document provides step-by-step demo scenarios to showcase the application's capabilities.

## Setup

Before running demos:
```bash
# Install dependencies
pip install -r requirements.txt

# Set up API key in .env
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run the application
python run.py
```

---

## Scenario 1: Daily Mood Tracking

**Objective**: Demonstrate basic mood logging functionality

### Steps:

1. **Start the application**
```
$ python run.py
```

2. **Log a positive mood**
```
You: I'm feeling happy today, intensity 8
Assistant: [Logs mood score 8 with emotion "happy"]
✓ Successfully logged mood entry
```

3. **Log another mood with details**
```
You: mood
You: I'm feeling calm and content, intensity 7. Had a productive day at work.
Assistant: [Logs mood with emotions and notes]
✓ Mood logged with context
```

4. **View mood history**
```
You: Show me my recent moods
Assistant: [Displays recent mood entries with timestamps]
- Today: Happy (8/10)
- Today: Calm (7/10)
```

**Expected Outcome**: User can easily log moods and view history

---

## Scenario 2: Pattern Analysis

**Objective**: Show how the system identifies trends and triggers

### Steps:

1. **Log multiple moods over "time"** (simulate different days)
```
You: I felt stressed yesterday, intensity 4. Work deadline.
You: Two days ago I was happy, intensity 8. Weekend relaxing.
You: Three days ago I was anxious, intensity 3. Presentation coming up.
```

2. **Request pattern analysis**
```
You: patterns
Assistant: [Analyzes mood data]

📊 Mood Pattern Analysis:
- Overall Trend: Variable
- Average Mood: 5.0/10
- Common Triggers: work stress, deadlines
- Patterns Detected:
  * Lower mood on weekdays
  * Higher mood on weekends
  * Work-related stress is recurring

💡 Insights:
- Consider stress management techniques for work
- Weekend activities seem beneficial
- May benefit from work-life balance strategies
```

**Expected Outcome**: System identifies meaningful patterns and provides insights

---

## Scenario 3: Crisis Detection & Support

**Objective**: Demonstrate automatic crisis detection and resource provision

### Steps:

1. **Express concerning thoughts** (simulated for demo)
```
You: I'm feeling really hopeless lately
```

2. **System detects crisis indicators**
```
Assistant: ⚠️ IMMEDIATE SUPPORT NEEDED ⚠️

I'm concerned about what you're experiencing. Your safety is the top priority.

🆘 Crisis Resources (24/7):
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International: https://www.iasp.info/resources/Crisis_Centres/

📞 Please reach out immediately to:
- Call 988 or your local emergency number
- Go to your nearest emergency room
- Contact a trusted friend or family member

💙 Remember: You don't have to face this alone. Help is available.
```

3. **Follow-up support**
```
You: Thank you, I'll reach out for help
Assistant: I'm glad you're taking that step. Would you like to talk about what's troubling you, or would you prefer resources for coping strategies?
```

**Expected Outcome**: System detects crisis, provides immediate resources, maintains supportive tone

---

## Scenario 4: Evidence-Based Support

**Objective**: Show RAG-based mental health advice

### Steps:

1. **Ask for coping strategies**
```
You: support
You: How can I manage anxiety?
```

2. **Receive evidence-based advice**
```
Assistant: Here are evidence-based strategies for managing anxiety:

🧘 Breathing Techniques:
- 4-7-8 breathing: Inhale 4 counts, hold 7, exhale 8
- Box breathing: 4 counts each for inhale, hold, exhale, hold

💪 Physical Strategies:
- Progressive muscle relaxation
- Regular exercise (30 min/day)
- Adequate sleep (7-9 hours)

🧠 Cognitive Techniques:
- Challenge anxious thoughts
- Practice mindfulness meditation
- Keep a worry journal

📚 Professional Resources:
- Consider cognitive-behavioral therapy (CBT)
- Consult with a mental health professional
- Explore anxiety support groups

Would you like more details on any of these strategies?
```

**Expected Outcome**: Contextual, evidence-based advice with actionable steps

---

## Scenario 5: Profile & Data Management

**Objective**: Demonstrate user profile and data export features

### Steps:

1. **Check profile**
```
You: Show my profile
Assistant: 
👤 User Profile:
- User ID: user_001
- Name: Demo User
- Check-in Streak: 3 days
- Total Mood Entries: 5
- Member Since: 2024-01-15
```

2. **Export data**
```
You: export
Assistant: Choose export format:
1. JSON (complete data)
2. CSV (tabular format)
3. Summary Report (text)

You: 3
Assistant: ✓ Summary report generated: data/exports/summary_2024-01-15.txt

📊 Summary Report Generated:
- Total Entries: 5
- Average Mood: 6.2/10
- Most Common Emotion: Happy
- Identified Triggers: work stress, social events
```

3. **View exported file**
```
$ cat data/exports/summary_2024-01-15.txt
[Shows formatted summary with statistics and insights]
```

**Expected Outcome**: User can manage profile and export data in multiple formats

---

## Scenario 6: Multi-Agent Coordination

**Objective**: Show how multiple agents work together

### Steps:

1. **Complex request requiring multiple agents**
```
You: Log my mood as anxious 4, then analyze my patterns and give me advice
```

2. **Orchestrator coordinates agents**
```
Assistant: [Orchestrator routes to multiple agents]

1. Mood Tracker: ✓ Logged mood (anxious, 4/10)
2. Pattern Analyzer: Analyzing recent trends...
   - Anxiety appears 3 times this week
   - Often linked to work situations
3. Support Specialist: Based on your anxiety pattern...
   [Provides targeted coping strategies]
```

**Expected Outcome**: Seamless multi-agent collaboration for complex requests

---

## Scenario 7: Command Shortcuts

**Objective**: Demonstrate CLI efficiency features

### Steps:

1. **Use menu command**
```
You: menu
Assistant: 
📋 Available Commands:
  mood      - Log your current mood
  patterns  - Analyze mood patterns
  support   - Get mental health support
  help      - Show help message
  export    - Export your data
  clear     - Clear screen
  exit      - Exit application
```

2. **Use shortcuts**
```
You: mood
[Quick mood logging interface]

You: patterns
[Quick pattern analysis]

You: support
[Quick support access]
```

**Expected Outcome**: Efficient navigation with shortcuts and clear commands

---

## Scenario 8: Error Handling

**Objective**: Show graceful error handling

### Steps:

1. **Invalid mood score**
```
You: I'm feeling happy, intensity 15
Assistant: ❌ Error: Mood intensity must be between 1 and 10.
Please try again with a valid intensity.
```

2. **Unclear request**
```
You: asdfghjkl
Assistant: I didn't quite understand that. Here are some things I can help with:
- Log your mood (try: "I'm feeling happy, intensity 7")
- Analyze patterns (try: "patterns")
- Get support (try: "support")
- Type "help" for more options
```

3. **Database error recovery**
```
[If database error occurs]
Assistant: ⚠️ A temporary error occurred. Your data is safe.
Please try again. If the problem persists, type "help" for support.
```

**Expected Outcome**: Clear error messages with helpful guidance

---

## Demo Tips

### For Live Demonstrations

1. **Prepare Test Data**: Pre-populate some mood entries for pattern analysis
2. **Highlight Safety**: Emphasize crisis detection and resource provision
3. **Show Privacy**: Demonstrate local data storage
4. **Test Coverage**: Mention 27 passing tests for reliability
5. **Real-World Use**: Explain practical applications

### Key Points to Emphasize

- ✅ **Multi-agent architecture** for specialized responses
- ✅ **Automatic crisis detection** for user safety
- ✅ **Evidence-based advice** via RAG
- ✅ **Privacy-first design** with local storage
- ✅ **Comprehensive testing** (100% pass rate)
- ✅ **User-friendly CLI** with shortcuts

### Common Questions & Answers

**Q: Is this a replacement for therapy?**  
A: No, it's a supportive tool that complements professional care.

**Q: How is data stored?**  
A: Locally in SQLite database - never sent to cloud.

**Q: How accurate is crisis detection?**  
A: Multi-factor assessment (mood + keywords + emotions) with high sensitivity.

**Q: Can I export my data?**  
A: Yes, in JSON, CSV, or summary report formats.

**Q: Is it tested?**  
A: Yes, 27 comprehensive tests with 100% pass rate.

---

## Video Demo Script

### Introduction (30 seconds)
"Hi, I'm demonstrating the Mental Health Support Companion - an AI-powered mental health support system built with Google's ADK and Gemini API."

### Core Features (1 minute)
1. Show mood logging
2. Demonstrate pattern analysis
3. Trigger crisis detection
4. Get support advice

### Technical Highlights (30 seconds)
- Multi-agent architecture
- Automatic crisis detection
- Evidence-based RAG system
- 27 passing tests

### Conclusion (30 seconds)
"This demonstrates how AI agents can provide accessible, private, and evidence-based mental health support while always encouraging professional care when needed."

**Total Time**: ~2.5 minutes

---

## Testing the Demo

Before presenting:
```bash
# Run tests to ensure everything works
python run_tests.py

# Test each scenario manually
# Verify crisis detection triggers correctly
# Check data export functionality
# Confirm all commands work
```

---

**Remember**: Always emphasize that this is a supportive tool, not a replacement for professional mental health care. 💙