import re
from do_abs import Worker

class ProxyBinder:
    __config_file = "etc/nginx/conf.d/default.conf"
    __worker : Worker = None
    __clear_config = "server {\n\tlisten       #{port};\n\tserver_name  {host};\n\n%(__bind_probe)\n\t}\n}"
    __current_config = ""
    __bind_probe = "#@bind@"
    __bind_probe_regex = re.compile(__bind_probe, re.IGNORECASE)
    __bind_regex = "#@{service}@[ \w\n]*#@end_{service}@\n"
    __bind_template = "#@{location}\n\t@location /{location}/ {\n\t\t proxy_pass {service_uri};\n\t\tproxy_redirect off;\n\t}#@end_{location}@\n%(__bind_probe)"

    def __set_config(self, config_text):
        self.__current_config = config_text
        self.__worker.exec(f'echo "%(__config_text)" > {self.__config_file}', "nginx")
        self.__worker.exec('nginx -s reload', "nginx")

    def __init__(self, worker : Worker, host, port):
        self.__worker = worker
        reset(host, port)

    def add_bind(self, location, service_url):
        self.__set_config(
            
            self.__bind_probe_regex.sub(
                self.__bind_template.format(location = location, service_url = service_url),
                self.__current_config
            )
        )

    def remove_bind(self, location):
        regex = re.compile(self.__bind_regex.format(service = location), re.IGNORECASE)

        self.__set_config(regex.sub("", self.__current_config))

    def update_bind(self, old_location, location, service_url):
        remove_bind(old_location)
        add_bind(location, service_url)

    def reset(self, host, port):
        self.__set_config(self.__clear_config.format(host = host, port = port))