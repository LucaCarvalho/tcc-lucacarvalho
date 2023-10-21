from boto3 import resource
from .storage import Storage
from subprocess import run, CompletedProcess

class RemoteStorage(Storage):
    def __init__(self, bucket: str) -> None:
        self.bucket_name = bucket
        self._bucket = resource('s3').Bucket(self.bucket_name)

    def list_files(self) -> list:
        s3_files = []
        for file in self._bucket.objects.all():
            s3_files.append(file.key)

        return s3_files
    
    def get_base_path(self) -> str:
        return f's3://{self.bucket_name}'
    
    def update_file(self, source: str, destination: str) -> None:
        self._bucket.upload_file(source, destination)

    def delete_file(self, filename: str) -> None:
        self._bucket.delete_objects(Delete={'Objects': [{'Key': filename}]})

    def sync_down(self, local_storage: Storage) -> CompletedProcess:
        # Download modified files
        return run(["aws", "s3", "sync", "--delete", self.get_base_path(), local_storage.get_base_path()], capture_output=True, text=True)
        