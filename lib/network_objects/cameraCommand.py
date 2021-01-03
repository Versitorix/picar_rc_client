from json import loads, dumps

from lib.network_objects.defaultCommand import DefaultCommand


class CameraCommand(DefaultCommand):
    type = 'CameraCommand'

    def __init__(self, movement_type, movement_value=None):
        """
        Initialize a new CameraCommand object.

        @type movement_type: string
        @type movement_value:
        """
        self.movement_type = movement_type
        self.movement_value = movement_value

    @staticmethod
    def from_string(json_string):
        json_dict = loads(json_string)

        movement_type = json_dict['movement_type']
        movement_value = json_dict['movement_value']

        return CameraCommand(movement_type, movement_value)

    def to_string(self):
        return dumps({
            "type": CameraCommand.type,
            "movement_type": self.movement_type,
            "movement_value": self.movement_value,
        })
