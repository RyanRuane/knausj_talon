import time

from talon import Module
from talon_plugins import eye_mouse, eye_zoom_mouse


mouse_zoom_hack_enabled = True
tracker_initialize_time = 0.1

mod = Module()


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
