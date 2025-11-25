# Mental Health Support Companion - System Architecture

## Overview

The Mental Health Support Companion is a multi-agent AI system designed to provide empathetic emotional support, mood tracking, and evidence-based coping strategies. It leverages the **Google Agent Development Kit (ADK)** to orchestrate specialized agents, manage state, and integrate tools.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  CLI         │  │  Rich Console│  │  Interactive │          │
│  │  Interface   │  │  Output      │  │  Menus       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer (ADK)                     │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Main Orchestrator (ADK Router Agent)            │  │
│  │  - Uses ADK routing to delegate tasks                     │  │
│  │  - Manages shared Session State                           │  │
│  │  - Handles global error recovery                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  Mood Tracker    │ │   Support    │ │  Crisis Monitor  │
│  Agent (ADK)     │ │  Agent (ADK) │ │   Agent (ADK)    │
│                  │ │              │ │                  │
│ - Daily check-in │ │ - Empathetic │ │ - Detect crisis  │
│ - Extract mood   │ │   responses  │ │   indicators     │
│ - Log emotions   │ │ - RAG Tools  │ │ - Provide        │
│ - DB Tools       │ │              │ │   resources      │
└──────────────────┘ └──────────────┘ └──────────────────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AI/ML & Tool Layer                           │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  Gemini 2.0      │  │  Pattern         │                    │
│  │  Flash           │  │  Analyzer        │                    │
│  │                  │  │  Agent (ADK)     │                    │
│  │ - Text gen       │  │                  │                    │
│  │ - Structured out │  │ - Mood trends    │                    │
│  │ - Reasoning      │  │ - Trigger ID     │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ADK Tools & RAG System                      │  │
│  │  - FunctionTool: Database interactions                   │  │
│  │  - FunctionTool: RAG (ChromaDB) retrieval                │  │
│  │  - FunctionTool: Crisis resource lookup                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
│                                                                   │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │  SQLite Database   │  │  ADK Session State │                │
│  │                    │  │                    │                │
│  │ - Users            │  │ - Short-term       │                │
│  │ - Mood entries     │  │   (session)        │                │
│  │ - Conversations    │  │ - User Context     │                │
│  │ - Messages         │  │   (in-memory)      │                │
│  │ - Strategies       │  │                    │                │
│  │ - Usage tracking   │  │                    │                │
│  └────────────────────┘  └────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer
- **CLI Interface**: Command-line interaction using Click
- **Rich Console**: Beautiful formatted output with Rich library
- **Interactive Menus**: User-friendly navigation and options

### 2. Orchestration Layer (ADK)
**Main Orchestrator (Router Agent)**
- **Type**: ADK `RouterAgent` or `SequentialAgent`
- **Role**: Central coordinator that routes user input to the appropriate specialized agent based on intent.
- **State Management**: Uses ADK's `SessionState` to maintain conversation context across different agents.
- **Error Handling**: Implements ADK error handlers to gracefully manage failures.

### 3. Specialized Agents (ADK Agents)

#### Mood Tracker Agent
**Type**: ADK `Agent`
**Purpose**: Track and record user's emotional state.
**Tools**:
- `log_mood_tool`: A `FunctionTool` that writes mood data to SQLite.
**Key Features**:
- Conducts daily mood check-ins.
- Uses Gemini to extract structured mood data (score 1-10, emotions).
- Generates empathetic acknowledgment.

#### Support Agent
**Type**: ADK `Agent`
**Purpose**: Provide empathetic support and coping strategies.
**Tools**:
- `retrieve_strategy_tool`: A `FunctionTool` wrapping the RAG pipeline (ChromaDB) to find relevant coping strategies.
**Key Features**:
- Empathetic conversational responses.
- Context-aware support using session history.
- Evidence-based interventions via RAG.

#### Crisis Monitor Agent
**Type**: ADK `Agent` (High Priority)
**Purpose**: Detect crisis situations and provide immediate help.
**Tools**:
- `get_crisis_resources_tool`: A `FunctionTool` to fetch emergency contacts.
**Key Features**:
- Real-time crisis detection using semantic analysis.
- Immediate resource provision.
- Can interrupt other agents if a crisis is detected.

#### Pattern Analyzer Agent
**Type**: ADK `Agent`
**Purpose**: Analyze mood trends and provide insights.
**Tools**:
- `fetch_mood_history_tool`: A `FunctionTool` to query SQLite for historical data.
**Key Features**:
- Historical mood analysis.
- Trigger identification and pattern recognition.
- Personalized insights.

### 4. AI/ML & Tool Layer

#### Gemini Integration
- **Model**: gemini-2.0-flash-exp
- **Usage**: Powered by Google GenAI SDK, integrated into ADK Agents.

#### ADK Tools & RAG
- **FunctionTools**: All external interactions (Database, Vector DB) are encapsulated as ADK `FunctionTool`s.
- **RAG System**:
    - **Vector DB**: ChromaDB
    - **Embeddings**: Google GenAI Embeddings
    - **Integration**: Exposed as a tool to the Support Agent.

### 5. Data Layer

#### SQLite Database Schema
*(Schema remains unchanged from previous version)*
```
users
├── user_id (PK)
├── name
├── timezone
├── created_at
└── preferences (JSON)

mood_entries
├── entry_id (PK)
├── user_id (FK)
├── timestamp
├── mood_score (1-10)
├── emotions (JSON)
├── triggers (JSON)
├── notes
└── conversation_summary

conversations
├── conversation_id (PK)
├── user_id (FK)
├── started_at
├── ended_at
├── message_count
└── summary

messages
├── message_id (PK)
├── conversation_id (FK)
├── user_id (FK)
├── role (user/assistant)
├── content
└── timestamp

coping_strategies
├── strategy_id (PK)
├── name
├── category
├── description
├── steps (JSON)
├── evidence_link
├── usage_count
└── created_at

strategy_usage
├── usage_id (PK)
├── user_id (FK)
├── strategy_id (FK)
├── used_at
├── helpful (boolean)
└── feedback
```

#### ADK Session State
- **Session Context**: Stores active conversation data, current user ID, and temporary flags.
- **Memory**: ADK's memory module manages the conversation history window for the LLM.

## Data Flow

### 1. Mood Check-in Flow
```
User Input → Orchestrator (Router) → Mood Tracker Agent
                ↓
         Gemini (extract mood)
                ↓
         Tool: log_mood_tool (Write to DB)
                ↓
         Empathetic response → User
```

### 2. Support Request Flow
```
User Input → Orchestrator (Router) → Support Agent
                ↓
         Tool: retrieve_strategy_tool (RAG Search)
                ↓
         Gemini (Generate response with strategy)
                ↓
         Combined response → User
```

### 3. Pattern Analysis Flow
```
User Request → Orchestrator (Router) → Pattern Analyzer Agent
                ↓
         Tool: fetch_mood_history_tool (Query DB)
                ↓
         Gemini (Analyze patterns)
                ↓
         Insights → User
```

## Key Design Principles
1.  **Safety First**: Crisis detection is paramount.
2.  **Privacy**: Local data storage (SQLite).
3.  **Empathy**: Warm, non-judgmental tone.
4.  **Modularity**: Agents are loosely coupled via ADK.

## Technology Stack
- **Language**: Python 3.10+
- **Framework**: **Google Agent Development Kit (ADK)**
- **AI/ML**: Google GenAI SDK (Gemini API)
- **Vector DB**: ChromaDB
- **Database**: SQLite3
- **CLI**: Click, Rich
- **Validation**: Pydantic
- **Environment**: python-dotenv