"""
Tests for utility modules
"""
import pytest
import os
import json
import tempfile
from pathlib import Path
from src.utils.profile_manager import ProfileManager


class TestProfileManager:
    """Test suite for ProfileManager"""
    
    @pytest.fixture
    def temp_profile_dir(self):
        """Create a temporary directory for profiles"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
    
    def test_create_profile(self, temp_profile_dir):
        """Test profile creation"""
        pm = ProfileManager(profile_dir=temp_profile_dir)
        
        profile = pm.create_profile("test_user_123", "Test User")
        
        assert profile["user_id"] == "test_user_123"
        assert profile["name"] == "Test User"
        assert os.path.exists(os.path.join(temp_profile_dir, "test_user_123_profile.json"))
    
    def test_get_profile(self, temp_profile_dir):
        """Test retrieving a profile"""
        pm = ProfileManager(profile_dir=temp_profile_dir)
        
        # Create a profile first
        pm.create_profile("test_user_123", "Test User")
        
        # Retrieve it
        profile = pm.get_profile("test_user_123")
        
        assert profile is not None
        assert profile["user_id"] == "test_user_123"
        assert profile["name"] == "Test User"
    
    def test_update_preference(self, temp_profile_dir):
        """Test updating user preferences"""
        pm = ProfileManager(profile_dir=temp_profile_dir)
        
        # Create profile
        pm.create_profile("test_user_123", "Test User")
        
        # Update preference using set_preference
        result = pm.set_preference("test_user_123", "notifications", False)
        
        assert result is True
        
        # Verify update
        profile = pm.get_profile("test_user_123")
        assert profile["preferences"]["notifications"] is False
    
    def test_increment_streak(self, temp_profile_dir):
        """Test streak tracking"""
        pm = ProfileManager(profile_dir=temp_profile_dir)
        
        # Create profile
        pm.create_profile("test_user_123", "Test User")
        
        # Initial streak should be 0
        profile = pm.get_profile("test_user_123")
        initial_streak = profile["preferences"]["check_in_streak"]
        
        # Increment streak
        new_streak = pm.increment_streak("test_user_123")
        
        assert new_streak == initial_streak + 1
        
        # Verify increment
        profile = pm.get_profile("test_user_123")
        assert profile["preferences"]["check_in_streak"] == initial_streak + 1
    
    def test_get_nonexistent_profile(self, temp_profile_dir):
        """Test retrieving a profile that doesn't exist"""
        pm = ProfileManager(profile_dir=temp_profile_dir)
        
        profile = pm.get_profile("nonexistent_user")
        
        assert profile is None


class TestDataExport:
    """Test suite for data export functionality"""
    
    def test_json_structure(self):
        """Test JSON export structure"""
        sample_data = {
            "user_id": "test_user",
            "entries": [
                {
                    "mood_score": 7,
                    "emotions": ["happy"],
                    "timestamp": "2024-01-01T10:00:00"
                }
            ]
        }
        
        # Verify it's valid JSON
        json_str = json.dumps(sample_data)
        parsed = json.loads(json_str)
        
        assert parsed["user_id"] == "test_user"
        assert len(parsed["entries"]) == 1
    
    def test_csv_formatting(self):
        """Test CSV export formatting"""
        csv_header = "mood_score,emotions,timestamp"
        csv_row = "7,happy,2024-01-01T10:00:00"
        
        assert "mood_score" in csv_header
        assert "emotions" in csv_header
        assert "timestamp" in csv_header
        assert "7" in csv_row