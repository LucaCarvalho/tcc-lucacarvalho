from os import listdir
from subprocess import run, CompletedProcess
from .storage import Storage

class LocalStorage(Storage):
    def __init__(self, path: str) -> None:
        self.path = path

    def list_files(self) -> list:
        local_files = []
        
        for file in listdir(self.path):
            local_files.append(file)
        
        return local_files
    
    def get_base_path(self) -> str:
        return self.path
    
    def sync_up(self, remote_storage: Storage) -> CompletedProcess:
        # Uploads modified files
        return run(["aws", "s3", "sync", "--delete", self.get_base_path(), remote_storage.get_base_path()], capture_output=True, text=True)
    
    def update_file(self, source: str, destination: str) -> None:
        pass

    def delete_file(self, filename: str) -> None:
        pass
