import time

from pynput import keyboard
from talon import Module
from talon_plugins import eye_zoom_mouse
from talon_plugins.eye_mouse import actions

control_mouse_in_use = False
mouse_zoom_hack_enabled = True
tracker_initialize_time = 0.1

mod = Module()


def mouse_toggle_control_mouse_legacy_hack(enabled: bool = None):
    global control_mouse_in_use
    control_mouse_in_use = not control_mouse_in_use
    actions.tracking.control1_toggle(control_mouse_in_use)


def build_keyboard_listener():
    # def on_activate():
    #     mouse_toggle_control_mouse_legacy_hack()

    def on_press(key):
        if key == keyboard.Key.num_lock:
            mouse_toggle_control_mouse_legacy_hack()

    # def for_canonical(hotkey):
    #     '''Removes any modifier state from the key events
    #     and normalises modifiers with more than one physical button'''
    #     return lambda k: hotkey(keyboard.Listener.canonical(k))

    # hotkey = keyboard.HotKey(
    #     keyboard.HotKey.parse('<ctrl>+<alt>+h'),
    #     on_activate,
    # )

    listener = keyboard.Listener(
        on_press=on_press,
        # on_press=for_canonical(hotkey.press),
        # on_release=for_canonical(hotkey.release),
    )
    return listener


listener = build_keyboard_listener()
listener.start()


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
