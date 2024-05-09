from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class Drive:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.port_number = os.getenv("PORT_NUBER", 3010)
        self.drive = None
        
    def authorize(self):
        self.gauth.LocalWebserverAuth(port_numbers=[self.port_number])
        self.drive = GoogleDrive(self.gauth)

    def get_folder_id(self, path):
        folder_path = path.split("/")
        folder_id = None
        
        for name in folder_path:
            query = f"mimeType = 'application/vnd.google-apps.folder' and title = '{name}'"
            if folder_id:
                query += f" and '{folder_id}' in parents"
            else: 
                query += " and 'root' in parents"

            try:
                folders = self.drive.ListFile({"q": query}).GetList()
            except:
                print(f"Error looking for folder {name}")
                exit()

            if len(folders) == 0:
                print(f"Folder {name} not found")
                exit()

            folder_id = folders[0]["id"]
            
        return folder_id
        
    def get_content(self, path, mime_type=None):
        folder_id = self.get_folder_id(path)

        query = f"'{folder_id}' in parents"
        if mime_type:
            query += f" and mimeType contains '{mime_type}'"

        return self.drive.ListFile({'q': query}).GetList()
        
