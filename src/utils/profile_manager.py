"""
User Profile Manager
Handles user preferences and profile information
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime

class ProfileManager:
    """Manages user profiles and preferences"""
    
    def __init__(self, profile_dir: str = "data/profiles"):
        self.profile_dir = profile_dir
        self._ensure_profile_dir()
    
    def _ensure_profile_dir(self):
        """Create profile directory if it doesn't exist"""
        os.makedirs(self.profile_dir, exist_ok=True)
    
    def _get_profile_path(self, user_id: str) -> str:
        """Get the file path for a user's profile"""
        return os.path.join(self.profile_dir, f"{user_id}_profile.json")
    
    def create_profile(self, user_id: str, name: str, **kwargs) -> Dict:
        """
        Create a new user profile
        
        Args:
            user_id: Unique user identifier
            name: User's display name
            **kwargs: Additional profile fields
            
        Returns:
            The created profile dictionary
        """
        profile = {
            "user_id": user_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "preferences": {
                "reminder_enabled": False,
                "reminder_time": "20:00",
                "check_in_streak": 0,
                "show_tips": True
            },
            **kwargs
        }
        
        self._save_profile(user_id, profile)
        return profile
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get a user's profile
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Profile dictionary or None if not found
        """
        profile_path = self._get_profile_path(user_id)
        
        if not os.path.exists(profile_path):
            return None
        
        try:
            with open(profile_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def update_profile(self, user_id: str, updates: Dict) -> bool:
        """
        Update a user's profile
        
        Args:
            user_id: Unique user identifier
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        profile = self.get_profile(user_id)
        
        if not profile:
            return False
        
        # Update fields
        profile.update(updates)
        profile["last_active"] = datetime.now().isoformat()
        
        return self._save_profile(user_id, profile)
    
    def update_last_active(self, user_id: str) -> bool:
        """Update the user's last active timestamp"""
        return self.update_profile(user_id, {})
    
    def increment_streak(self, user_id: str) -> int:
        """
        Increment the user's check-in streak
        
        Returns:
            The new streak count
        """
        profile = self.get_profile(user_id)
        if not profile:
            return 0
        
        current_streak = profile.get("preferences", {}).get("check_in_streak", 0)
        new_streak = current_streak + 1
        
        profile.setdefault("preferences", {})["check_in_streak"] = new_streak
        self._save_profile(user_id, profile)
        
        return new_streak
    
    def get_preference(self, user_id: str, key: str, default=None):
        """Get a specific user preference"""
        profile = self.get_profile(user_id)
        if not profile:
            return default
        
        return profile.get("preferences", {}).get(key, default)
    
    def set_preference(self, user_id: str, key: str, value) -> bool:
        """Set a specific user preference"""
        profile = self.get_profile(user_id)
        if not profile:
            return False
        
        profile.setdefault("preferences", {})[key] = value
        return self._save_profile(user_id, profile)
    
    def _save_profile(self, user_id: str, profile: Dict) -> bool:
        """Save profile to file"""
        profile_path = self._get_profile_path(user_id)
        
        try:
            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete a user's profile"""
        profile_path = self._get_profile_path(user_id)
        
        try:
            if os.path.exists(profile_path):
                os.remove(profile_path)
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False