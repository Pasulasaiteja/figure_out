"""
YouTube Data API Service
"""
import requests
from app.core.config import settings
from typing import List, Dict, Optional

class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_exercise_video(self, exercise_name: str, duration: str = "medium") -> Optional[str]:
        """
        Search for exercise tutorial video
        Returns video ID
        """
        if not self.api_key:
            return None
        
        try:
            query = f"{exercise_name} exercise tutorial how to"
            
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "videoDuration": duration,  # short, medium, long
                "videoDefinition": "high",
                "maxResults": 1,
                "key": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("items"):
                video_id = data["items"][0]["id"]["videoId"]
                return video_id
            
            return None
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return None
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """Get detailed information about a video"""
        if not self.api_key or not video_id:
            return None
        
        try:
            params = {
                "part": "snippet,contentDetails,statistics",
                "id": video_id,
                "key": self.api_key
            }
            
            response = requests.get(f"{self.base_url}/videos", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("items"):
                item = data["items"][0]
                return {
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                    "duration": item["contentDetails"]["duration"],
                    "view_count": item["statistics"].get("viewCount", 0)
                }
            
            return None
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return None

# Singleton instance
youtube_service = YouTubeService()
