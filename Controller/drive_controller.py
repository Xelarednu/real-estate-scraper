from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.exceptions import RefreshError
import os.path
from pathlib import Path

class DriveController():
    SCOPES = [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ]

    CLIENT_ACCOUNT_FILE = 'secrets/client_secret.json'

    def __init__(self):
        self.creds = None
        self.__authorize()

    def __authorize(self) -> any:
        if (os.path.exists("secrets/token.json")):
            self.creds = Credentials.from_authorized_user_file("secrets/token.json", self.SCOPES)
        if (not self.creds or not self.creds.valid):
            if (self.creds and self.creds.expired and self.creds.refresh_token):
                try:
                    self.creds.refresh(Request())
                except RefreshError:
                    self.creds = None
            if (not self.creds or not self.creds.valid):
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_ACCOUNT_FILE, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open("secrets/token.json", "w") as token:
                token.write(self.creds.to_json())
        return self.creds

    def __build_service(self) -> any:
        service = build('drive', 'v3', credentials=self.creds)
        return service

    def upload_file(self, file_path: str) -> str:
        path = Path(file_path)

        file_metadata = {"name": path.name, "parents": ['1gprJ8O0QnESnZ0UJ5dNCToVXQ01orhIh']} # My folder: 1Nvl341DQGPjjl2lxEgL-h3hBYZoi9seK
        media = MediaFileUpload(str(path), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", resumable=True)
        try:
            service = self.__build_service()
            file = (service.files().create(body=file_metadata, media_body=media, fields="id").execute())
            return file.get("id")
        except HttpError as err:
            print(err)
            return None
