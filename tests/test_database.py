"""
Tests for database operations
"""
import pytest
from pathlib import Path
import tempfile
import os
from src.utils.database import DatabaseManager


@pytest.fixture
def db():
    """Create a test database instance"""
    # Create a temporary database file
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"
    test_db = DatabaseManager(db_path=db_path)
    yield test_db
    # Cleanup
    if db_path.exists():
        os.remove(db_path)
    os.rmdir(temp_dir)


class TestDatabase:
    """Test suite for DatabaseManager class"""
    
    def test_database_initialization(self, db):
        """Test that database tables are created correctly"""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert "mood_entries" in tables
        assert "users" in tables
        assert "conversations" in tables
    
    def test_create_and_get_user(self, db):
        """Test creating and retrieving a user"""
        user_id = "test_user_001"
        name = "Test User"
        
        # Create user
        result = db.create_user(user_id, name)
        assert result is True
        
        # Retrieve user
        user = db.get_user(user_id)
        assert user is not None
        assert user["user_id"] == user_id
        assert user["name"] == name
    
    def test_add_and_get_mood_entry(self, db):
        """Test adding and retrieving mood entries"""
        # First create a user
        user_id = "test_user_001"
        db.create_user(user_id, "Test User")
        
        # Add mood entry
        entry_id = "entry_001"
        mood_score = 7
        emotions = ["happy", "calm"]
        triggers = ["good_weather"]
        notes = "Had a great day"
        
        result = db.add_mood_entry(
            entry_id, user_id, mood_score, emotions, triggers, notes
        )
        assert result is True
        
        # Retrieve mood history
        history = db.get_mood_history(user_id, days=7)
        assert len(history) == 1
        assert history[0]["mood_score"] == mood_score
    
    def test_duplicate_user_creation(self, db):
        """Test that duplicate user creation fails"""
        user_id = "test_user_001"
        
        # Create user first time
        result1 = db.create_user(user_id, "Test User")
        assert result1 is True
        
        # Try to create same user again
        result2 = db.create_user(user_id, "Test User")
        assert result2 is False
    
    def test_get_nonexistent_user(self, db):
        """Test retrieving a user that doesn't exist"""
        user = db.get_user("nonexistent_user")
        assert user is None
    
    def test_mood_history_empty(self, db):
        """Test retrieving mood history for user with no entries"""
        # Create user but don't add any mood entries
        user_id = "test_user_001"
        db.create_user(user_id, "Test User")
        
        history = db.get_mood_history(user_id)
        assert len(history) == 0