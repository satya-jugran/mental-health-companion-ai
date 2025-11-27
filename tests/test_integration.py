"""
Integration tests for the application
"""
import pytest


class TestBasicIntegration:
    """Basic integration tests"""
    
    def test_imports(self):
        """Test that all main modules can be imported"""
        try:
            from src.utils.database import DatabaseManager
            from src.utils.profile_manager import ProfileManager
            from src.utils.data_export import DataExporter
            assert True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
    
    def test_database_and_profile_integration(self):
        """Test database and profile manager work together"""
        from src.utils.database import DatabaseManager
        from src.utils.profile_manager import ProfileManager
        import tempfile
        from pathlib import Path
        
        # Create temporary directories
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test.db"
        profile_dir = temp_dir
        
        # Initialize both
        db = DatabaseManager(db_path=db_path)
        pm = ProfileManager(profile_dir=profile_dir)
        
        # Create user in both systems
        user_id = "test_user"
        db.create_user(user_id, "Test User")
        pm.create_profile(user_id, "Test User")
        
        # Verify both exist
        db_user = db.get_user(user_id)
        profile = pm.get_profile(user_id)
        
        assert db_user is not None
        assert profile is not None
        assert db_user["user_id"] == profile["user_id"]
        
        # Cleanup
        import os
        if db_path.exists():
            os.remove(db_path)
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(temp_dir)


class TestWorkflows:
    """Test complete workflows"""
    
    def test_mood_tracking_workflow(self):
        """Test complete mood tracking workflow"""
        from src.utils.database import DatabaseManager
        import tempfile
        from pathlib import Path
        
        # Setup
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test.db"
        db = DatabaseManager(db_path=db_path)
        
        # Create user
        user_id = "test_user"
        db.create_user(user_id, "Test User")
        
        # Add mood entries
        for i in range(3):
            entry_id = f"entry_{i}"
            db.add_mood_entry(
                entry_id, user_id, 5 + i, 
                ["happy"], ["work"], f"Day {i}"
            )
        
        # Retrieve history
        history = db.get_mood_history(user_id)
        
        assert len(history) == 3
        
        # Cleanup
        import os
        if db_path.exists():
            os.remove(db_path)
        os.rmdir(temp_dir)
    
    def test_profile_workflow(self):
        """Test profile management workflow"""
        from src.utils.profile_manager import ProfileManager
        import tempfile
        
        # Setup
        temp_dir = tempfile.mkdtemp()
        pm = ProfileManager(profile_dir=temp_dir)
        
        # Create profile
        user_id = "test_user"
        pm.create_profile(user_id, "Test User")
        
        # Update preferences
        pm.set_preference(user_id, "notifications", False)
        
        # Increment streak
        new_streak = pm.increment_streak(user_id)
        
        # Verify all changes
        profile = pm.get_profile(user_id)
        assert profile["preferences"]["notifications"] is False
        assert profile["preferences"]["check_in_streak"] == 1
        assert new_streak == 1
        
        # Cleanup
        import os
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)