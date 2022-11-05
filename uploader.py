import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class Uploader:
  def __init__(self, category:int, title:str, description:str, tags:list[str], status:str):
    self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    upload_date_time = datetime.datetime(2022, 11, 6, 12, 30, 0).isoformat() + '.000Z'
    self.request_body = {
    'snippet': {
        'categoryI': category,
        'title': title,
        'description': description,
        'tags': tags
        },
        'status': {
            'privacyStatus': status, # private, public
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }
    self.upload()
  
  def upload(self):
    mediaFile = MediaFileUpload('output.mp4')
    response_upload = self.service.videos().insert(
    part='snippet,status',
    body=self.request_body,
    media_body=mediaFile
    ).execute()

class Login:
  def __init__(self) -> None:
    self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  
