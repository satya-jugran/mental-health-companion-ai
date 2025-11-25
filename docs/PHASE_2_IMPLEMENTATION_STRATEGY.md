# Phase 2: Core Agent Implementation Strategy (Google ADK)

This document outlines the technical strategy for implementing the core agents of the Mental Health Support Companion using the Google Agent Development Kit (ADK).

## 1. Core Components

### 1.1. Agent Definitions
We will define three primary agents using the `Agent` class from `google.labs.adk`.

*   **`MoodTrackerAgent`**:
    *   **Role**: Collects and logs user mood data.
    *   **Instructions**: "You are a compassionate mood tracking assistant. Your goal is to gently ask the user about their day, extract their mood score (1-10) and emotions, and log this information. Be empathetic and brief."
    *   **Tools**: `log_mood_tool`
    *   **Model**: `gemini-2.0-flash-exp`

*   **`SupportAgent`**:
    *   **Role**: Provides emotional support and coping strategies.
    *   **Instructions**: "You are a supportive mental health companion. Listen to the user's concerns, validate their feelings, and provide evidence-based coping strategies. Use the `retrieve_strategy_tool` to find relevant exercises."
    *   **Tools**: `retrieve_strategy_tool`
    *   **Model**: `gemini-2.0-flash-exp`

*   **`MainOrchestrator` (Router)**:
    *   **Role**: Routes user input to the correct agent.
    *   **Implementation**: We will use a `RouterAgent` (or a custom routing logic using a lightweight `Agent`) to classify the user's intent (e.g., "log_mood", "get_support", "crisis") and delegate execution.

### 1.2. Tool Implementation (`FunctionTool`)
All external interactions will be wrapped as `FunctionTool`s.

*   **`log_mood_tool`**:
    *   **Function**: `log_mood(user_id: str, mood_score: int, emotions: List[str], notes: str)`
    *   **Description**: "Logs the user's mood score, emotions, and notes into the database."
    *   **Implementation**: Wraps the SQLite `insert_mood_entry` function.

*   **`retrieve_strategy_tool`**:
    *   **Function**: `retrieve_strategy(emotion: str, intensity: int)`
    *   **Description**: "Searches the knowledge base for coping strategies relevant to the user's current emotion."
    *   **Implementation**: Wraps the ChromaDB query logic.

### 1.3. State Management (`SessionState`)
We will use ADK's `SessionState` to maintain context across the multi-agent workflow.

*   **Shared State**:
    *   `user_id`: ID of the current user.
    *   `current_mood`: The most recently logged mood (for the Support Agent to reference).
    *   `conversation_history`: Managed by ADK's memory module.

## 2. Implementation Steps

### Step 1: Tool Creation
1.  Create `src/tools/mood_tools.py`: Implement `log_mood` function and wrap it with `FunctionTool`.
2.  Create `src/tools/rag_tools.py`: Implement `retrieve_strategy` function and wrap it with `FunctionTool`.

### Step 2: Agent Configuration
1.  Create `src/agents/mood_agent.py`: Initialize `MoodTrackerAgent` with instructions and `mood_tools`.
2.  Create `src/agents/support_agent.py`: Initialize `SupportAgent` with instructions and `rag_tools`.

### Step 3: Orchestration Logic
1.  Create `src/agents/orchestrator.py`: Implement the routing logic.
    *   *Input*: User message.
    *   *Process*: Classify intent -> Select Agent -> Run Agent.
    *   *Output*: Agent response.

### Step 4: Integration & Testing
1.  Create a `main.py` script to initialize the system and run a CLI loop.
2.  Test the flow:
    *   User: "I feel sad."
    *   Orchestrator -> MoodTrackerAgent
    *   MoodTrackerAgent: "I'm sorry to hear that. On a scale of 1-10...?"
    *   User: "3"
    *   MoodTrackerAgent -> `log_mood_tool` -> DB
    *   Orchestrator -> SupportAgent (optional handoff)
    *   SupportAgent -> `retrieve_strategy_tool` -> "Here is a breathing exercise..."

## 3. Directory Structure Update
```
mental-health-companion/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── mood_agent.py
│   │   ├── support_agent.py
│   │   └── orchestrator.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── mood_tools.py
│   │   └── rag_tools.py
│   └── ...