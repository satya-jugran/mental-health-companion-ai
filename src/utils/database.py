"""Database schema and initialization for Mental Health Support Companion"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
from .config import DATABASE_PATH


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database manager
        
        Args:
            db_path: Path to database file. If None, uses config default.
        """
        self.db_path = db_path or DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            timezone TEXT DEFAULT 'UTC',
            created_at TEXT NOT NULL,
            preferences TEXT,
            UNIQUE(user_id)
        )
        """)
        
        # Mood entries table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            entry_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            mood_score INTEGER NOT NULL CHECK(mood_score >= 1 AND mood_score <= 10),
            emotions TEXT,
            triggers TEXT,
            notes TEXT,
            conversation_summary TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)
        
        # Conversations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            message_count INTEGER DEFAULT 0,
            summary TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)
        
        # Messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)
        
        # Coping strategies table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS coping_strategies (
            strategy_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            steps TEXT NOT NULL,
            evidence_link TEXT,
            usage_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
        """)
        
        # Strategy usage tracking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS strategy_usage (
            usage_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            strategy_id TEXT NOT NULL,
            used_at TEXT NOT NULL,
            helpful BOOLEAN,
            feedback TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (strategy_id) REFERENCES coping_strategies(strategy_id)
        )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_mood_entries_user_timestamp 
        ON mood_entries(user_id, timestamp DESC)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_messages_conversation 
        ON messages(conversation_id, timestamp)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_strategy_usage_user 
        ON strategy_usage(user_id, used_at DESC)
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, user_id: str, name: str, timezone: str = "UTC", 
                    preferences: Optional[Dict] = None) -> bool:
        """Create a new user
        
        Args:
            user_id: Unique user identifier
            name: User's name
            timezone: User's timezone
            preferences: User preferences dict
            
        Returns:
            True if user created successfully
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO users (user_id, name, timezone, created_at, preferences)
            VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                name,
                timezone,
                datetime.utcnow().isoformat(),
                json.dumps(preferences) if preferences else None
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID
        
        Args:
            user_id: User identifier
            
        Returns:
            User data dict or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_dict = dict(row)
            if user_dict.get('preferences'):
                user_dict['preferences'] = json.loads(user_dict['preferences'])
            return user_dict
        return None
    
    def add_mood_entry(self, entry_id: str, user_id: str, mood_score: int,
                      emotions: List[str], triggers: List[str], notes: str,
                      conversation_summary: str = "") -> bool:
        """Add a mood entry
        
        Args:
            entry_id: Unique entry identifier
            user_id: User identifier
            mood_score: Mood score (1-10)
            emotions: List of emotions
            triggers: List of triggers
            notes: User notes
            conversation_summary: Summary of the conversation
            
        Returns:
            True if entry added successfully
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO mood_entries 
            (entry_id, user_id, timestamp, mood_score, emotions, triggers, notes, conversation_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                user_id,
                datetime.utcnow().isoformat(),
                mood_score,
                json.dumps(emotions),
                json.dumps(triggers),
                notes,
                conversation_summary
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding mood entry: {e}")
            return False
        finally:
            conn.close()
    
    def get_mood_history(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get mood history for a user
        
        Args:
            user_id: User identifier
            days: Number of days to retrieve
            
        Returns:
            List of mood entries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM mood_entries 
        WHERE user_id = ? 
        AND timestamp >= datetime('now', '-' || ? || ' days')
        ORDER BY timestamp DESC
        """, (user_id, days))
        
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entry = dict(row)
            entry['emotions'] = json.loads(entry['emotions']) if entry.get('emotions') else []
            entry['triggers'] = json.loads(entry['triggers']) if entry.get('triggers') else []
            entries.append(entry)
        
        return entries
    
    def add_coping_strategy(self, strategy_id: str, name: str, category: str,
                           description: str, steps: List[str], 
                           evidence_link: str = "") -> bool:
        """Add a coping strategy
        
        Args:
            strategy_id: Unique strategy identifier
            name: Strategy name
            category: Strategy category
            description: Strategy description
            steps: List of steps
            evidence_link: Link to evidence/research
            
        Returns:
            True if strategy added successfully
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO coping_strategies 
            (strategy_id, name, category, description, steps, evidence_link, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                strategy_id,
                name,
                category,
                description,
                json.dumps(steps),
                evidence_link,
                datetime.utcnow().isoformat()
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding coping strategy: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_strategies(self) -> List[Dict[str, Any]]:
        """Get all coping strategies
        
        Returns:
            List of all coping strategies
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM coping_strategies")
        rows = cursor.fetchall()
        conn.close()
        
        strategies = []
        for row in rows:
            strategy = dict(row)
            strategy['steps'] = json.loads(strategy['steps']) if strategy.get('steps') else []
            strategies.append(strategy)
        
        return strategies