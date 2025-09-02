# services/google_drive.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self, credentials_path='credentials.json'):
        self.credentials_path = credentials_path
        self._service = None

    @property
    def service(self):
        if self._service is None:
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/drive.readonly']
                )
                self._service = build('drive', 'v3', credentials=credentials)
                logger.info("Google Drive service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Drive service: {e}")
                return None
        return self._service

    def list_files(self, folder_id: str, is_premium_content: bool = False) -> list:
        """
        List files in a Google Drive folder.
        
        Args:
            folder_id: Google Drive folder ID
            is_premium_content: Whether this is premium content (affects URL generation)
            
        Returns:
            List of file dictionaries with name, id, and appropriate URLs
        """
        if not self.service:
            logger.error("Google Drive service not available.")
            return []
        
        try:
            # Query to get files from the folder
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, webViewLink, webContentLink)"
            ).execute()
            
            items = results.get('files', [])
            
            # Process each file to add appropriate URLs
            processed_items = []
            for item in items:
                file_info = {
                    'id': item['id'],
                    'name': item['name'],
                    'mimeType': item.get('mimeType', ''),
                    'view_only_url': item.get('webViewLink', ''),
                    'download_url': item.get('webContentLink', '') if not is_premium_content else None
                }
                processed_items.append(file_info)
            
            logger.info(f"Listed {len(items)} files from folder ID: {folder_id}")
            return processed_items
        except HttpError as error:
            logger.error(f"An error occurred while listing files from Google Drive: {error}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred in list_files: {e}")
            return []