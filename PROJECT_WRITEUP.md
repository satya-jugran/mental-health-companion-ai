# Mental Health Support Companion - Project Writeup

**Kaggle Agents Intensive Capstone Project**

## Executive Summary

The Mental Health Support Companion is an AI-powered mental health support system built using Google's Agent Development Kit (ADK) and Gemini API. It provides compassionate, evidence-based mental health support through a multi-agent architecture that handles mood tracking, pattern analysis, crisis detection, and personalized guidance.

**Key Achievement**: A production-ready application with 27 passing tests, comprehensive documentation, and real-world applicability in mental health support.

## Problem Statement

Mental health challenges affect millions globally, yet many face barriers to accessing professional support:
- **Accessibility**: Limited access to mental health professionals
- **Cost**: High cost of therapy and counseling
- **Stigma**: Fear of judgment prevents seeking help
- **Availability**: 24/7 support needs vs. limited professional hours

**Solution**: An AI companion that provides immediate, judgment-free support while encouraging professional help when needed.

## Technical Architecture

### Multi-Agent System Design

The application uses a **specialized multi-agent architecture** where each agent has a specific role:

1. **Orchestrator Agent** (`orchestrator.py`)
   - Routes user requests to appropriate specialist agents
   - Coordinates multi-agent workflows
   - Ensures coherent responses across agents

2. **Mood Tracker Agent** (`mood_agent.py`)
   - Logs mood entries with scores (1-10) and emotions
   - Retrieves mood history
   - Monitors for crisis indicators during mood logging

3. **Pattern Analyzer Agent** (`pattern_agent.py`)
   - Analyzes mood trends over time
   - Identifies triggers and behavioral patterns
   - Provides insights for self-awareness

4. **Crisis Monitor Agent** (`crisis_agent.py`)
   - Assesses crisis levels (low/moderate/high)
   - Provides immediate crisis resources
   - Ensures user safety is prioritized

5. **Support Specialist Agent** (`support_agent.py`)
   - Delivers evidence-based mental health advice
   - Uses RAG for contextual responses
   - Provides coping strategies and resources

### Technology Stack

- **AI Framework**: Google Agent Development Kit (ADK)
- **LLM**: Gemini 2.0 Flash (fast, efficient, cost-effective)
- **Database**: SQLite (local, private, portable)
- **Vector Store**: ChromaDB (for RAG-based support)
- **Testing**: pytest (27 tests, 100% pass rate)
- **Language**: Python 3.10+

### Key Technical Features

#### 1. Function Tools (ADK)
Each agent has specialized tools implemented as ADK `FunctionTool`:
```python
from google.adk.tools import FunctionTool

def log_mood(mood_score: int, emotions: List[str], notes: str) -> str:
    """Logs mood with validation and crisis checking"""
    # Implementation
    
log_mood_tool = FunctionTool(log_mood)
```

#### 2. Database Schema
Comprehensive SQLite schema with constraints:
```sql
CREATE TABLE mood_entries (
    entry_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    mood_score INTEGER CHECK(mood_score >= 1 AND mood_score <= 10),
    emotions TEXT,
    notes TEXT,
    timestamp TEXT NOT NULL
)
```

#### 3. Crisis Detection Algorithm
Multi-factor crisis assessment:
- Mood score thresholds (≤2 = high risk, 3-4 = moderate)
- Crisis keyword detection (regex-based)
- Crisis emotion identification
- Immediate resource provision

#### 4. RAG Implementation
Evidence-based support using ChromaDB:
- Mental health resources embedded as vectors
- Semantic search for relevant advice
- Context-aware responses

## Implementation Highlights

### Phase 1: Planning & Setup
- Defined multi-agent architecture
- Set up project structure
- Configured Google ADK and Gemini API

### Phase 2: Core Agent Implementation
- Built 5 specialized agents
- Implemented 6 function tools
- Established agent communication patterns

### Phase 3: Advanced Features
- Added pattern analysis with trend detection
- Implemented automatic crisis monitoring
- Built RAG system for evidence-based support

### Phase 4: User Interface
- Created enhanced CLI with colored output
- Added profile management and streak tracking
- Implemented data export (JSON/CSV/reports)

### Phase 5: Testing & Refinement
- Wrote 27 comprehensive tests
- Achieved 100% test pass rate
- Tests call actual functions (not mocks)
- Fixed import issues and validated constraints

### Phase 6: Documentation & Demo
- Comprehensive README
- API documentation
- Testing guides
- Demo scenarios

## Unique Features

### 1. Automatic Crisis Detection
Unlike basic chatbots, the system **automatically monitors** every interaction for crisis indicators and provides immediate resources when needed.

### 2. Multi-Agent Specialization
Each agent is an expert in its domain, providing more accurate and contextual responses than a single general-purpose agent.

### 3. Privacy-First Design
All data stored locally with no cloud sync, giving users complete control over their sensitive mental health data.

### 4. Evidence-Based Support
RAG system ensures advice is grounded in mental health research, not just LLM hallucinations.

### 5. Comprehensive Testing
27 tests covering database, tools, utilities, and integration - ensuring reliability for sensitive mental health applications.

## Challenges & Solutions

### Challenge 1: Import Path Issues
**Problem**: Relative imports caused test failures  
**Solution**: Converted to absolute imports (`from src.utils.database import DatabaseManager`)

### Challenge 2: Crisis Detection Accuracy
**Problem**: Need to balance sensitivity vs. false positives  
**Solution**: Multi-factor assessment (mood score + keywords + emotions)

### Challenge 3: Database Constraints
**Problem**: Ensuring data integrity for mood scores  
**Solution**: SQLite CHECK constraints + application-level validation

### Challenge 4: Agent Coordination
**Problem**: Multiple agents need to work together seamlessly  
**Solution**: Orchestrator pattern with clear routing logic

## Results & Impact

### Quantitative Metrics
- **27/27 tests passing** (100% success rate)
- **2.34 seconds** test execution time
- **5 specialized agents** working in harmony
- **6 function tools** for comprehensive functionality
- **280+ lines** of comprehensive documentation

### Qualitative Benefits
- **Immediate Support**: 24/7 availability for mental health guidance
- **Privacy**: Local data storage protects sensitive information
- **Accessibility**: Free, judgment-free support for anyone
- **Safety**: Automatic crisis detection and resource provision
- **Empowerment**: Pattern insights help users understand themselves

## Real-World Applicability

### Use Cases
1. **Daily Check-ins**: Track mood and emotions regularly
2. **Crisis Support**: Immediate resources during difficult times
3. **Self-Awareness**: Understand patterns and triggers
4. **Coping Strategies**: Learn evidence-based techniques
5. **Professional Complement**: Supplement therapy with daily support

### Limitations & Disclaimers
- **Not a replacement** for professional mental health care
- **AI limitations**: May not understand complex situations
- **Crisis detection**: Automated, may miss some cases
- **Always recommend** professional help for serious concerns

## Future Enhancements

### Short-term
- Web interface for better accessibility
- Enhanced visualizations for mood trends
- More sophisticated pattern analysis

### Long-term
- Mobile app with push notifications
- Integration with wearables (heart rate, sleep)
- Multi-language support
- Personalized AI models per user

## Lessons Learned

### Technical
1. **ADK Best Practices**: Proper agent initialization and tool usage
2. **Testing Importance**: Real function calls > mocks for reliability
3. **Import Management**: Absolute imports prevent test issues
4. **Database Design**: Constraints enforce data integrity

### Product
1. **Privacy Matters**: Users need control over mental health data
2. **Crisis Safety**: Automatic detection is crucial for safety
3. **Evidence-Based**: RAG ensures quality advice
4. **User Experience**: Clear commands and helpful feedback

## Conclusion

The Mental Health Support Companion demonstrates how Google's ADK and Gemini API can be used to build a **production-ready, socially impactful application**. By combining multi-agent architecture, crisis detection, pattern analysis, and evidence-based support, it provides a comprehensive mental health support system that is:

- **Accessible**: Available 24/7 to anyone
- **Private**: Local data storage
- **Safe**: Automatic crisis detection
- **Effective**: Evidence-based advice
- **Tested**: 100% test pass rate

This project showcases the potential of AI agents to address real-world challenges in mental health support while maintaining ethical considerations around privacy, safety, and professional care.

---

**Project Repository**: [GitHub Link]  
**Demo Video**: [YouTube Link]  
**Documentation**: See `docs/` directory  
**Tests**: Run `python run_tests.py`

**Built with ❤️ using Google Agent Development Kit and Gemini API**