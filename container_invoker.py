import docker
from do_abs import Worker, ResourceMananager
from docker.models.containers import Container

class DockerWorker(Worker, ResourceMananager):

    __client : docker.DockerClient = None

    def __init__(self):
        self.__client = docker.from_env()

    def exec(self, cmd, exec_name):
        container : Container = self.__client.containers.get(exec_name)
        container.exec_run(cmd)

    def create_resource(self, name, **kwargs):
        self.__client.containers.run(name, kwargs=**kwargs)
    
    def remove_resource(self, name):
        container: Container = self.__client.containers.get(name)
        container.remove(force = True)
    
    def update_resource(self, name, **kwargs):
        self.remove_resource(name)
        self.create_resource(name, kwargs=**kwargs)


class ContainerInvoker:
    
    __worker : ResourceMananager = None

    def __init__(self, worker: ResourceMananager):
        self.__worker = worker

    def run_container(self, name, image, port_binding, network = None, restart="unleass-stopped", **kwargs):
        
        args = {}

        for key, value in kwargs:
            args[key] = value
        
        args["name"] = name
        
        if port_binding != None:
            args["ports"] = port_binding
        
        if network != None:
            args["network"] = network
        
        args["restart"] = restart

        self.__worker.create_resource(image, **args)

    
    def remove_container(self, name):
        self.__worker.remove_resource(name)

