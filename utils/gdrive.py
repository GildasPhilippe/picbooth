import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_file_to_drive(fpath):
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("SERVICE_ACCOUNT_KEY_PATH"),
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    service = build('drive', 'v3', credentials=credentials)
    _upload_file(os.path.basename(fpath), os.getenv("DRIVE_FOLDER_ID"), fpath, service)


def _upload_file(file_name, folder_id, local_file_path, service):
    try:
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(local_file_path, mimetype='image/jpeg')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File uploaded: {file_name} ({file.get("id")})')
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None
    return file


if __name__ == '__main__':
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())
    upload_file_to_drive("pictures/test.jpg")
