"""
Data Export Utility
Exports user data in various formats for backup and analysis
"""
import json
import csv
from datetime import datetime
from typing import Dict
from .database import DatabaseManager

class DataExporter:
    """Handles data export functionality"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def export_mood_data_json(self, user_id: str, output_file: str) -> bool:
        """
        Export mood data to JSON format
        
        Args:
            user_id: User identifier
            output_file: Path to output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all mood entries
            entries = self.db.get_mood_history(user_id=user_id)
            
            export_data = {
                "user_id": user_id,
                "export_date": datetime.now().isoformat(),
                "total_entries": len(entries),
                "mood_entries": entries
            }
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False
    
    def export_mood_data_csv(self, user_id: str, output_file: str) -> bool:
        """
        Export mood data to CSV format
        
        Args:
            user_id: User identifier
            output_file: Path to output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            entries = self.db.get_mood_entries(user_id=user_id)
            
            if not entries:
                return False
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                # Define CSV fields
                fieldnames = ['entry_id', 'timestamp', 'mood_score', 'emotions', 'triggers', 'notes']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for entry in entries:
                    # Convert lists to strings for CSV
                    row = {
                        'entry_id': entry['entry_id'],
                        'timestamp': entry['timestamp'],
                        'mood_score': entry['mood_score'],
                        'emotions': ', '.join(entry.get('emotions', [])),
                        'triggers': ', '.join(entry.get('triggers', [])),
                        'notes': entry.get('notes', '')
                    }
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"Error exporting CSV for user {user_id} to {output_file}: {e}")
            return False
    
    def generate_summary_report(self, user_id: str) -> Dict:
        """
        Generate a comprehensive summary report
        
        Args:
            user_id: User identifier
            
        Returns:
            dict: If data is available, returns a dictionary containing summary statistics:
                {
                    "user_id": str,
                    "report_generated": str (ISO datetime),
                   "statistics": {
                       "total_entries": int,
                       "average_mood": float,
                       "highest_mood": int,
                       "lowest_mood": int,
                       "unique_emotions": int,
                       "total_emotions_logged": int
                   },
                   "top_emotions": List[Dict[str, int]],
                   "date_range": {
                       "first_entry": str,
                       "last_entry": str
                   }
               }
                If no data is available, returns:
                {
                    "error": "No data available",
                    "total_entries": 0
                }
            
        """
        entries = self.db.get_mood_history(user_id=user_id)
        
        if not entries:
            return {
                "error": "No data available",
                "total_entries": 0
            }
        
        # Calculate statistics
        mood_scores = [e['mood_score'] for e in entries]
        all_emotions = []
        for entry in entries:
            all_emotions.extend(entry.get('emotions', []))
        
        # Count emotion frequencies
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Sort emotions by frequency
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        summary = {
            "user_id": user_id,
            "report_generated": datetime.now().isoformat(),
            "statistics": {
                "total_entries": len(entries),
                "average_mood": sum(mood_scores) / len(mood_scores) if mood_scores else 0,
                "highest_mood": max(mood_scores) if mood_scores else 0,
                "lowest_mood": min(mood_scores) if mood_scores else 0,
                "unique_emotions": len(emotion_counts),
                "total_emotions_logged": len(all_emotions)
            },
            "top_emotions": [
                {"emotion": emotion, "count": count} 
                for emotion, count in top_emotions
            ],
            "date_range": {
                "first_entry": entries[0]['timestamp'] if entries else None,
                "last_entry": entries[-1]['timestamp'] if entries else None
            }
        }
        
        return summary
    
    def export_summary_report(self, user_id: str, output_file: str) -> bool:
        """
        Export summary report to JSON file
        
        Args:
            user_id: User identifier
            output_file: Path to output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            summary = self.generate_summary_report(user_id)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting summary: {e}")
            return False