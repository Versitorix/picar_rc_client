from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep, time

from lib.settings import SETTINGS
from lib.network_objects.cameraCommand import CameraCommand
from lib.network_objects.frontWheelCommand import FrontWheelCommand
from lib.network_objects.backWheelCommand import BackWheelCommand
from lib.ps4Controller import PS4Controller, JOY_RIGHT_X, JOY_RIGHT_Y, JOY_LEFT_X, TRIGGER_RIGHT, TRIGGER_LEFT


last_sent = 0
udp_socket = socket(AF_INET, SOCK_DGRAM)
isMoving = False


def controller_listener(controller_data):
    global last_sent
    global udp_socket
    global isMoving

    now = time()

    if time() - last_sent > 0.1:
        last_sent = now

        tilt = round(controller_data['axis_data'][JOY_RIGHT_Y] * -90 + 90, 2)
        pan = round(controller_data['axis_data'][JOY_RIGHT_X] * -90 + 90, 2)
        front_wheels_angle = round(controller_data['axis_data'][JOY_LEFT_X] * 40 + 90, 2)
        backward_speed = 0
        forward_speed = 0

        if backward_speed <= -1.0 and backward_speed <= 0:
            backward_speed = round(controller_data['axis_data'][TRIGGER_LEFT] * -50, 0)
        else:
            backward_speed = round(controller_data['axis_data'][TRIGGER_LEFT] * 50 + 50, 0)

        if forward_speed <= -1.0 and forward_speed <= 0:
            forward_speed = round(controller_data['axis_data'][TRIGGER_RIGHT] * -50, 0)
        else:
            forward_speed = round(controller_data['axis_data'][TRIGGER_RIGHT] * 50 + 50, 0)

        camera_command = CameraCommand('set_position', (pan, tilt))
        front_wheel_command = FrontWheelCommand('turn', front_wheels_angle)

        udp_socket.sendto(
            bytes(camera_command.to_string(), encoding="utf8"),
            (SETTINGS.server_ip, SETTINGS.commands_port)
        )
        udp_socket.sendto(
            bytes(front_wheel_command.to_string(), encoding="utf8"),
            (SETTINGS.server_ip, SETTINGS.commands_port)
        )

        if forward_speed > 0:
            if not isMoving:
                isMoving = True
                forward_command = BackWheelCommand('forward', forward_speed)
                udp_socket.sendto(
                    bytes(forward_command.to_string(), encoding="utf8"),
                    (SETTINGS.server_ip, SETTINGS.commands_port)
                )
            else:
                set_speed_command = BackWheelCommand('set_speed', forward_speed)
                udp_socket.sendto(
                    bytes(set_speed_command.to_string(), encoding="utf8"),
                    (SETTINGS.server_ip, SETTINGS.commands_port)
                )
        elif backward_speed > 0:
            if not isMoving:
                isMoving = True
                backward_command = BackWheelCommand('backward', backward_speed)
                udp_socket.sendto(
                    bytes(backward_command.to_string(), encoding="utf8"),
                    (SETTINGS.server_ip, SETTINGS.commands_port)
                )
            else:
                set_speed_command = BackWheelCommand('set_speed', backward_speed)
                udp_socket.sendto(
                    bytes(set_speed_command.to_string(), encoding="utf8"),
                    (SETTINGS.server_ip, SETTINGS.commands_port)
                )
        elif isMoving:
            isMoving = False
            stop_command = BackWheelCommand('stop')
            udp_socket.sendto(
                bytes(stop_command.to_string(), encoding="utf8"),
                (SETTINGS.server_ip, SETTINGS.commands_port)
            )


def listen_for_controller():
    controller = PS4Controller()
    controller.init()
    controller.add_listener(controller_listener)
    controller.listen()

listen_for_controller()
