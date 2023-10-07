from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def list_files(self) -> list:
        pass

    @abstractmethod
    def get_base_path(self) -> str:
        pass

    @abstractmethod
    def update_file(self, source:str, destination:str) -> None:
        pass
    
    @abstractmethod
    def delete_file(self, filename:str) -> None:
        pass