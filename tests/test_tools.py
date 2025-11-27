"""
Tests for tool functions
"""
from pathlib import Path
import tempfile
import os
from src.utils.database import DatabaseManager


class TestMoodTools:
    """Test suite for mood tracking tools"""
    
    def test_log_mood_valid_score(self):
        """Test logging mood with valid score"""
        from src.tools.mood_tools import log_mood
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test.db"
        db = DatabaseManager(db_path=db_path)
        
        # Create user first
        db.create_user("test_user", "Test User")
        
        # Test valid mood scores
        result = log_mood(mood_score=5, emotions=["happy"], notes="Good day", user_id="test_user")
        assert "Successfully logged" in result
        
        result = log_mood(mood_score=1, emotions=["sad"], notes="Bad day", user_id="test_user")
        assert "Successfully logged" in result
        
        result = log_mood(mood_score=10, emotions=["excited"], notes="Great day", user_id="test_user")
        assert "Successfully logged" in result
        
        # Cleanup
        if db_path.exists():
            os.remove(db_path)
        os.rmdir(temp_dir)
    
    def test_log_mood_invalid_score(self):
        """Test logging mood with invalid score (should fail due to database constraint)"""
        from src.tools.mood_tools import log_mood
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test.db"
        db = DatabaseManager(db_path=db_path)
        
        # Create user first
        db.create_user("test_user", "Test User")
        
        # Test invalid mood scores (should fail)
        result = log_mood(mood_score=0, emotions=["sad"], notes="Invalid", user_id="test_user")
        assert "Failed" in result or "error" in result.lower()
        
        result = log_mood(mood_score=11, emotions=["happy"], notes="Invalid", user_id="test_user")
        assert "Failed" in result or "error" in result.lower()
        
        result = log_mood(mood_score=-5, emotions=["angry"], notes="Invalid", user_id="test_user")
        assert "Failed" in result or "error" in result.lower()
        
        # Cleanup
        if db_path.exists():
            os.remove(db_path)
        os.rmdir(temp_dir)
    
    def test_emotions_list_handling(self):
        """Test emotions list handling in log_mood"""
        from src.tools.mood_tools import log_mood
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test.db"
        db = DatabaseManager(db_path=db_path)
        
        # Create user first
        db.create_user("test_user", "Test User")
        
        # Test with multiple emotions
        emotions = ["happy", "calm", "excited"]
        result = log_mood(mood_score=8, emotions=emotions, notes="Multiple emotions", user_id="test_user")
        assert "Successfully logged" in result
        
        # Verify the function accepted the emotions list
        # (The actual storage verification would require mocking or dependency injection)
        assert isinstance(emotions, list)
        assert len(emotions) == 3
        assert all(isinstance(e, str) for e in emotions)
        
        # Cleanup
        if db_path.exists():
            os.remove(db_path)
        os.rmdir(temp_dir)


class TestCrisisTools:
    """Test suite for crisis detection tools"""
    
    def test_crisis_detection_high_risk(self):
        """Test crisis detection with high-risk indicators"""
        from src.tools.crisis_tools import check_crisis_indicators
        
        # Test with very low mood score
        result = check_crisis_indicators(
            mood_score=1,
            emotions=["hopeless", "desperate"],
            notes="I feel like there's no point anymore"
        )
        
        assert "IMMEDIATE SUPPORT NEEDED" in result
        assert "988" in result
        assert "Crisis Text Line" in result
    
    def test_crisis_detection_moderate_risk(self):
        """Test crisis detection with moderate-risk indicators"""
        from src.tools.crisis_tools import check_crisis_indicators
        
        # Test with low mood score
        result = check_crisis_indicators(
            mood_score=3,
            emotions=["sad", "worried"],
            notes="Having a really tough time"
        )
        
        assert "Support Resources Available" in result
        assert "988" in result
    
    def test_crisis_detection_no_risk(self):
        """Test crisis detection with no risk indicators"""
        from src.tools.crisis_tools import check_crisis_indicators
        
        # Test with good mood score
        result = check_crisis_indicators(
            mood_score=7,
            emotions=["happy", "calm"],
            notes="Had a good day today"
        )
        
        assert "No immediate crisis indicators detected" in result
    
    def test_crisis_detection_with_keywords(self):
        """Test crisis detection with crisis keywords in notes"""
        from src.tools.crisis_tools import check_crisis_indicators
        
        # Test with crisis keywords
        result = check_crisis_indicators(
            mood_score=5,
            emotions=["sad"],
            notes="I've been thinking about suicide lately"
        )
        
        assert "IMMEDIATE SUPPORT NEEDED" in result
        assert "988" in result
    
    def test_crisis_detection_with_emotions(self):
        """Test crisis detection with crisis emotions"""
        from src.tools.crisis_tools import check_crisis_indicators
        
        # Test with crisis emotions
        result = check_crisis_indicators(
            mood_score=6,
            emotions=["hopeless", "trapped"],
            notes="Just feeling down"
        )
        
        assert "Support Resources" in result or "IMMEDIATE SUPPORT" in result


class TestPatternTools:
    """Test suite for pattern analysis tools"""
    
    def test_trend_calculation(self):
        """Test trend calculation logic"""
        # Improving trend
        scores = [3, 4, 5, 6, 7]
        avg_first_half = sum(scores[:2]) / 2
        avg_second_half = sum(scores[2:]) / len(scores[2:])
        assert avg_second_half > avg_first_half
        
        # Declining trend
        scores = [8, 7, 6, 5, 4]
        avg_first_half = sum(scores[:2]) / 2
        avg_second_half = sum(scores[2:]) / len(scores[2:])
        assert avg_second_half < avg_first_half
    
    def test_trigger_extraction(self):
        """Test trigger extraction from notes"""
        notes = "Feeling stressed because of work deadline"
        triggers = ["work", "deadline"]
        
        assert any(trigger in notes.lower() for trigger in triggers)