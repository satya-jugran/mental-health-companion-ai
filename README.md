# Mental Health Support Companion 🧠💙

A compassionate AI-powered mental health support system built with Google's Agent Development Kit (ADK) and Gemini API. This multi-agent system provides mood tracking, pattern analysis, crisis detection, and evidence-based mental health support.

## 🌟 Features

### Core Capabilities
- **🎭 Mood Tracking**: Log daily moods with intensity scores (1-10) and emotions
- **📊 Pattern Analysis**: Identify trends, triggers, and behavioral patterns over time
- **🆘 Crisis Detection**: Automatic detection of crisis indicators with immediate resource provision
- **💬 Support & Advice**: Evidence-based mental health guidance using RAG (Retrieval-Augmented Generation)
- **👤 User Profiles**: Personalized experience with preferences and streak tracking
- **📤 Data Export**: Export mood data in JSON, CSV, or summary report formats

### Multi-Agent Architecture
- **Orchestrator Agent**: Routes requests to specialized agents
- **Mood Tracker Agent**: Handles mood logging and retrieval
- **Pattern Analyzer Agent**: Detects trends and triggers
- **Crisis Monitor Agent**: Assesses crisis levels and provides resources
- **Support Specialist Agent**: Provides evidence-based mental health advice

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Google API Key (for Gemini API)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd mental-health-companion
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
python run.py
```

## 📖 Usage

### Basic Commands

```
Available Commands:
  mood      - Log your current mood
  patterns  - Analyze mood patterns
  support   - Get mental health support
  help      - Show help message
  menu      - Show command menu
  export    - Export your data
  exit      - Exit the application
```

### Example Interactions

#### Logging a Mood
```
You: I'm feeling happy today, intensity 8
Assistant: I'll log your mood. [Logs mood score 8 with emotion "happy"]
```

#### Analyzing Patterns
```
You: patterns
Assistant: [Analyzes recent mood entries and identifies trends]
- Overall trend: Improving
- Common triggers: work stress, social events
- Recommendations: Continue current coping strategies
```

#### Getting Support
```
You: How can I manage anxiety?
Assistant: [Provides evidence-based advice on anxiety management]
- Deep breathing exercises
- Progressive muscle relaxation
- Cognitive restructuring techniques
```

#### Crisis Detection
```
You: I'm feeling hopeless
Assistant: ⚠️ IMMEDIATE SUPPORT NEEDED ⚠️
[Provides crisis resources including hotlines and emergency contacts]
```

## 🏗️ Architecture

### Project Structure
```
mental-health-companion/
├── src/
│   ├── agents/           # Multi-agent system
│   │   ├── orchestrator.py
│   │   ├── mood_agent.py
│   │   ├── pattern_agent.py
│   │   ├── crisis_agent.py
│   │   └── support_agent.py
│   ├── tools/            # Agent tools
│   │   ├── mood_tools.py
│   │   ├── pattern_tools.py
│   │   ├── crisis_tools.py
│   │   └── rag_tools.py
│   ├── utils/            # Utilities
│   │   ├── database.py
│   │   ├── profile_manager.py
│   │   ├── data_export.py
│   │   └── config.py
│   ├── ui/               # User interface
│   │   └── cli.py
│   └── main.py           # Application entry point
├── tests/                # Test suite
├── data/                 # Data storage
├── docs/                 # Documentation
└── requirements.txt      # Dependencies
```

### Technology Stack
- **AI Framework**: Google Agent Development Kit (ADK)
- **LLM**: Google Gemini 2.0 Flash
- **Database**: SQLite
- **Vector Store**: ChromaDB (for RAG)
- **Testing**: pytest

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v

# Run specific test file
pytest tests/test_database.py -v

# Run with coverage
pytest tests/ --cov=src
```

### Test Coverage
- **27 tests** covering all major functionality
- Database operations, tool functions, utilities, and integration
- 100% pass rate

## 📊 Data Management

### Database Schema
- **Users**: User profiles and preferences
- **Mood Entries**: Mood logs with scores, emotions, and notes
- **Conversations**: Chat history
- **Coping Strategies**: Evidence-based mental health resources

### Data Export
Export your data in multiple formats:
```
You: export
Choose format:
1. JSON (complete data)
2. CSV (tabular format)
3. Summary Report (text)
```

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally in SQLite database
- **No Cloud Sync**: Data never leaves your machine (except API calls to Gemini)
- **API Key Security**: API key stored in `.env` file (not committed to git)
- **Data Control**: Full control over your data with export/delete options

## ⚠️ Important Disclaimers

### Not a Replacement for Professional Help
This application is a **supportive tool** and **NOT a substitute** for professional mental health care. If you're experiencing:
- Suicidal thoughts
- Severe depression or anxiety
- Mental health crisis

**Please seek immediate professional help:**
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911 or your local emergency number

### Limitations
- AI-generated advice should not replace professional diagnosis or treatment
- Crisis detection is automated and may not catch all situations
- Always consult qualified mental health professionals for serious concerns

## 🛠️ Development

### Adding New Features

1. **Create a new tool** in `src/tools/`
2. **Add to appropriate agent** in `src/agents/`
3. **Write tests** in `tests/`
4. **Update documentation**

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions focused and testable

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Submit a pull request

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)**: System design and architecture
- **[Testing Guide](docs/TESTING_GUIDE.md)**: How to run and write tests
- **[Manual Testing](docs/MANUAL_TESTING_CHECKLIST.md)**: Manual testing scenarios
- **[Phase Summaries](docs/)**: Development phase documentation

## 🎯 Roadmap

### Completed ✅
- Multi-agent system with Google ADK
- Mood tracking and pattern analysis
- Crisis detection and resource provision
- RAG-based support system
- User profiles and data export
- Comprehensive test suite
- CLI interface

### Future Enhancements
- [ ] Web interface
- [ ] Mobile app
- [ ] Advanced visualizations
- [ ] Personalized recommendations
- [ ] Integration with wearables
- [ ] Multi-language support

## 📄 License

This project is created for educational purposes as part of the Google Agents Intensive Capstone Project.

## 🙏 Acknowledgments

- **Google Agent Development Kit (ADK)** for the multi-agent framework
- **Google Gemini API** for powerful language understanding
- **Mental health professionals** whose research informs our evidence-based content

## 📞 Support

For technical issues or questions:
- Check the [documentation](docs/)
- Review [test examples](tests/)
- Open an issue on GitHub

---

**Remember**: This is a supportive tool. Always prioritize professional mental health care when needed. You're not alone, and help is available. 💙