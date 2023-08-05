import logging
import socket
import subprocess
import threading
import time

from pynput import keyboard
from talon import Module, actions as talon_actions
from talon_plugins import eye_zoom_mouse
from talon_plugins.eye_mouse import actions as eye_mouse_actions

command_mode_in_use = False
dictation_mode_in_use = False
sleep_mode_in_use = False

control_mouse_in_use = False
mouse_zoom_hack_enabled = True
tracker_initialize_time = 0.1

mod = Module()


def switch_command_and_dictation_mode():
    global dictation_mode_in_use
    if dictation_mode_in_use:
        enable_command_mode()
    else:
        enable_dictation_mode()


def switch_command_and_sleep_mode():
    global sleep_mode_in_use
    if sleep_mode_in_use:
        enable_command_mode()
    else:
        enable_sleep_mode()


def switch_dictation_and_sleep_mode():
    global sleep_mode_in_use
    if sleep_mode_in_use:
        enable_dictation_mode()
    else:
        enable_sleep_mode()


def enable_command_mode():
    global sleep_mode_in_use
    global dictation_mode_in_use
    global command_mode_in_use
    if not command_mode_in_use:
        talon_actions.mode.disable("sleep")
        talon_actions.mode.disable("dictation")
        talon_actions.mode.enable("command")
        sleep_mode_in_use = False
        dictation_mode_in_use = False
        command_mode_in_use = True


def enable_dictation_mode():
    global sleep_mode_in_use
    global command_mode_in_use
    global dictation_mode_in_use
    if not dictation_mode_in_use:
        talon_actions.mode.disable("sleep")
        talon_actions.mode.disable("command")
        talon_actions.mode.enable("dictation")
        talon_actions.user.code_clear_language_mode()
        talon_actions.mode.disable("user.gdb")
        sleep_mode_in_use = False
        command_mode_in_use = False
        dictation_mode_in_use = True


def enable_sleep_mode():
    global dictation_mode_in_use
    global command_mode_in_use
    global sleep_mode_in_use
    if not sleep_mode_in_use:
        talon_actions.mode.disable("dictation")
        talon_actions.mode.disable("command")
        talon_actions.mode.enable("sleep")
        dictation_mode_in_use = False
        command_mode_in_use = False
        sleep_mode_in_use = True


def mouse_toggle_control_mouse_legacy_hack(enabled: bool = None):
    global control_mouse_in_use
    control_mouse_in_use = not control_mouse_in_use
    eye_mouse_actions.tracking.control1_toggle(control_mouse_in_use)


def build_keyboard_listener():
    def on_press(key):
        if key == keyboard.Key.num_lock:
            mouse_toggle_control_mouse_legacy_hack()
        elif key == keyboard.Key.scroll_lock:
            switch_command_and_dictation_mode()

    listener = keyboard.Listener(
        on_press=on_press,
        # on_release=on_release,
    )
    return listener


def build_hotkey_listener():
    hotkeys = keyboard.GlobalHotKeys({
        '<cmd>+e': enable_command_mode,
        '<cmd>+u': enable_dictation_mode,
        '<cmd>+i': enable_sleep_mode,
    })
    return hotkeys


def start_keyboard_listeners():
    keyboard_listener = build_keyboard_listener()
    hotkey_listener = build_hotkey_listener()
    keyboard_listener.start()
    hotkey_listener.start()


def send_gnome_msg(title: str, msg: str, timeout_sec: int):
    subprocess.call(['strace', '-e', 'open', 'notify-send', title, msg])
    time.sleep(timeout_sec)
    subprocess.call(['killall', 'notify-osd'])


def listen_for_commands(server_socket):
    while True:
        time.sleep(1)
        connection, address = server_socket.accept()
        data = connection.recv(512)
        # send_gnome_msg_title = 'Talon Mode'
        # timeout_sec = 1
        if len(data) > 0:
            if data == b'c':
                logging.info(f'Received {data}. Command mode')
                enable_command_mode()
                # send_gnome_msg(send_gnome_msg_title, 'Command', timeout_sec)
            elif data == b'd':
                logging.info(f'Received {data}. Dictation mode')
                enable_dictation_mode()
                # send_gnome_msg(send_gnome_msg_title, 'Dictation', timeout_sec)
            elif data == b's':
                logging.info(f'Received {data}. Sleep mode')
                enable_sleep_mode()
                # send_gnome_msg(send_gnome_msg_title, 'Sleep', timeout_sec)
            else:
                logging.info(f"Received unknown command: {data}")


class CommandListener(threading.Thread):
    def __init__(self, hostname: str, port: int):
        threading.Thread.__init__(self)
        self.name = 'TalonCommandListener'
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((hostname, port))
        self.server_socket.listen(1)  # become a server socket, maximum 5 connections

    # helper function to execute the threads
    def run(self):
        listen_for_commands(self.server_socket)

    # Deleting (Calling destructor)
    def __del__(self):
        self.server_socket.close()
        logging.info(f"Closed {self.name}")


command_listener_host = ''
command_listener_port = 5000
thread = CommandListener(command_listener_host, command_listener_port)
thread.start()


@mod.action_class
class Actions:
    def mouse_trigger_zoom_hack_mouse():
        """Trigger tracker toggling zoom mouse if enabled"""
        if mouse_zoom_hack_enabled:
            if eye_zoom_mouse.zoom_mouse.enabled:
                eye_zoom_mouse.zoom_mouse.on_pop(
                    eye_zoom_mouse.zoom_mouse.state)
                eye_zoom_mouse.toggle_zoom_mouse(
                    not eye_zoom_mouse.zoom_mouse.enabled)
            else:
                eye_zoom_mouse.toggle_zoom_mouse(
                    not eye_zoom_mouse.zoom_mouse.enabled)
                time.sleep(tracker_initialize_time)
                eye_zoom_mouse.zoom_mouse.on_pop(
                    eye_zoom_mouse.zoom_mouse.state)

    def mouse_toggle_zoom_hack_mouse():
        """Enable the mouse zoom hack"""
        global mouse_zoom_hack_enabled
        mouse_zoom_hack_enabled = not mouse_zoom_hack_enabled

    def mouse_toggle_control_mouse_legacy_hack(enabled: bool = None):
        """Toggles control mouse. Pass in a bool to enable it, otherwise toggle the current state"""
        mouse_toggle_control_mouse_legacy_hack(enabled)
