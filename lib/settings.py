from json import loads


class Settings(object):
    def __init__(self, commands_port, connectivity_port, server_ip):
        """
        Instantiate a new Settings object.

        @param commands_port: number
        @param connectivity_port: number
        @param server_ip: string
        """

        self.commands_port = commands_port
        self.connectivity_port = connectivity_port
        self.server_ip = server_ip

    @staticmethod
    def from_string(json_string):
        """
        Instantiate a new Settings object from a json string.

        @param json_string: string
        @return: Settings
        """

        json_dict = loads(json_string)
        commands_port = json_dict['commands_port']
        connectivity_port = json_dict['connectivity_port']
        server_ip = json_dict['server_ip']

        return Settings(commands_port, connectivity_port, server_ip)


file = open('./settings/dev.json', 'r').read()

SETTINGS = Settings.from_string(file)

