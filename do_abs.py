from abc import ABC, abstractclassmethod

class Worker(ABC):

    @abstractclassmethod
    def exec(self, cmd, exec_name):
        pass

class ResourceMananager(ABC):

    @abstractclassmethod
    def create_resource(self, name, **kwargs):
        pass

    @abstractclassmethod
    def remove_resource(self, name):
        pass

    @abstractclassmethod
    def update_resource(self, name, **kwargs):
        pass
