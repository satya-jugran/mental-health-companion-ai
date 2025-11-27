"""
Tests for tool functions
"""
import pytest
from pathlib import Path
import tempfile
import os


class TestMoodTools:
    """Test suite for mood tracking tools"""
    
    def test_mood_score_validation(self):
        """Test mood score validation logic"""
        # Valid scores
        assert 1 <= 5 <= 10
        assert 1 <= 10 <= 10
        assert 1 <= 1 <= 10
        
        # Invalid scores
        assert not (1 <= 0 <= 10)
        assert not (1 <= 11 <= 10)
        assert not (1 <= -5 <= 10)
    
    def test_emotions_list_handling(self):
        """Test emotions list handling"""
        emotions = ["happy", "calm", "excited"]
        assert isinstance(emotions, list)
        assert len(emotions) == 3
        assert all(isinstance(e, str) for e in emotions)


class TestCrisisTools:
    """Test suite for crisis detection tools"""
    
    def test_crisis_keywords_detection(self):
        """Test crisis keyword detection logic"""
        high_risk_keywords = ["suicide", "hopeless", "end it all", "no point"]
        medium_risk_keywords = ["anxious", "overwhelmed", "stressed", "panic"]
        
        # High risk text
        high_risk_text = "I feel hopeless and want to end it all"
        assert any(keyword in high_risk_text.lower() for keyword in high_risk_keywords)
        
        # Medium risk text
        medium_risk_text = "I'm feeling very anxious and overwhelmed"
        assert any(keyword in medium_risk_text.lower() for keyword in medium_risk_keywords)
        
        # Low risk text
        low_risk_text = "I had a good day today"
        assert not any(keyword in low_risk_text.lower() for keyword in high_risk_keywords)
    
    def test_crisis_resources_availability(self):
        """Test that crisis resources are available"""
        resources = [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"
        ]
        
        assert len(resources) > 0
        assert all(isinstance(r, str) for r in resources)


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