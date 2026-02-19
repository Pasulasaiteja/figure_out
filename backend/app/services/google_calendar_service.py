"""
Google Calendar Integration Service
"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional, List, Dict

class GoogleCalendarService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scopes = ['https://www.googleapis.com/auth/calendar']
    
    def get_authorization_url(self) -> str:
        """
        Generate Google OAuth authorization URL
        """
        if not self.client_id or not self.client_secret:
            return ""
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            return auth_url
        except Exception as e:
            print(f"Google Calendar Auth Error: {e}")
            return ""
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """
        Exchange authorization code for access token
        """
        if not self.client_id or not self.client_secret:
            return None
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes,
                redirect_uri=self.redirect_uri
            )
            
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            return {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token
            }
        except Exception as e:
            print(f"Google Calendar Token Error: {e}")
            return None
    
    def create_event(
        self,
        token: str,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime
    ) -> Optional[str]:
        """
        Create a calendar event
        Returns event ID
        """
        if not token:
            return None
        
        try:
            credentials = Credentials(token=token)
            service = build('calendar', 'v3', credentials=credentials)
            
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            event_result = service.events().insert(calendarId='primary', body=event).execute()
            return event_result.get('id')
        except Exception as e:
            print(f"Google Calendar Create Event Error: {e}")
            return None
    
    def update_event(
        self,
        token: str,
        event_id: str,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """
        Update an existing calendar event
        """
        if not token or not event_id:
            return False
        
        try:
            credentials = Credentials(token=token)
            service = build('calendar', 'v3', credentials=credentials)
            
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return True
        except Exception as e:
            print(f"Google Calendar Update Event Error: {e}")
            return False
    
    def delete_event(self, token: str, event_id: str) -> bool:
        """
        Delete a calendar event
        """
        if not token or not event_id:
            return False
        
        try:
            credentials = Credentials(token=token)
            service = build('calendar', 'v3', credentials=credentials)
            
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            return True
        except Exception as e:
            print(f"Google Calendar Delete Event Error: {e}")
            return False

# Singleton instance
google_calendar_service = GoogleCalendarService()
