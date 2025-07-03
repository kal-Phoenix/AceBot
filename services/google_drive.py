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

    def _authenticate(self):
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            self._service = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive service authenticated successfully.")
        except Exception as e:
            logger.error(f"Error authenticating Google Drive service: {e}")
            self._service = None
            raise

    @property
    def service(self):
        if self._service is None:
            self._authenticate()
        return self._service

    def list_files(self, folder_id):
        if not self.service:
            logger.error("Google Drive service not available.")
            return []
        try:
            query = f"'{folder_id}' in parents and trashed = false"
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, webViewLink)",
                pageSize=1000 # Increased page size for more files if needed
            ).execute()
            items = results.get('files', [])
            logger.info(f"Listed {len(items)} files from folder ID: {folder_id}")
            return items
        except HttpError as error:
            logger.error(f"An error occurred while listing files from Google Drive: {error}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred in list_files: {e}")
            return []