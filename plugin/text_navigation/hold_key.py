from typing import Callable

from talon import Module, actions, cron

hold_job = None


def hold_helper(key: str) -> Callable[[], None]:
    def inner():
        actions.key(key)

    return inner


def start_hold(key: str):
    global hold_job
    hold_job = cron.interval('100ms', hold_helper(key))


def stop_hold():
    global hold_job
    if hold_job:
        cron.cancel(hold_job)

    hold_job = None


mod = Module()


@mod.action_class
class Actions:

    def hold(key: str):
        """Starts holding"""
        if hold_job is None:
            start_hold(key)

    def stop_hold():
        """Stops holding"""
        stop_hold()
