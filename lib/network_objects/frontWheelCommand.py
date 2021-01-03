from json import loads, dumps

from lib.network_objects.defaultCommand import DefaultCommand


class FrontWheelCommand(DefaultCommand):
    type = 'FrontWheelCommand'

    def __init__(self, action, action_value=None):
        """
        Initialize a new FrontWheelCommand object.

        @type action: string
        @type action_value:
        """
        self.action = action
        self.action_value = action_value

    @staticmethod
    def from_string(json_string):
        json_dict = loads(json_string)

        action = json_dict['action']
        action_value = json_dict['action_value']

        return FrontWheelCommand(action, action_value)

    def to_string(self):
        return dumps({
            "type": FrontWheelCommand.type,
            "action": self.action,
            "action_value": self.action_value,
        })
