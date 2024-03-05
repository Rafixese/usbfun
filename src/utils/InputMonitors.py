from abc import ABC
from typing import Callable, Union

from pynput import keyboard, mouse
from pynput.keyboard import HotKey
from pynput.keyboard._base import Listener, KeyCode, Key
from pynput.mouse import Button
from usbmonitor import USBMonitor


class MonitorManager:
    def __init__(self):
        self.hotkey_monitor: HotkeyMonitor | None = None
        self.usb_monitor: USBDeviceMonitor | None = None
        self.mouse_monitor: MouseMonitor | None = None

    def __monitor_list(self):
        return [self.hotkey_monitor, self.usb_monitor, self.mouse_monitor]

    def stop_all(self):
        for monitor in self.__monitor_list():
            try:
                monitor.stop()
            except Exception as e:
                print(str(e))

    def join_all(self):
        for monitor in self.__monitor_list():
            try:
                monitor.join()
            except Exception as e:
                print(str(e))


class BaseMonitor(ABC):

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()


class MouseMonitor(BaseMonitor):
    def __init__(self, on_move: Callable[[int, int], bool] | None = None,
                 on_click: Callable[[int, int, Button, bool], bool] | None = None,
                 on_scroll: Callable[[int, int, int, int], bool] | None = None,
                 suppress: bool = False):
        self.__listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=suppress)


class USBDeviceMonitor(BaseMonitor):
    def __init__(self, on_connect: Callable | None = None, on_disconnect: Callable | None = None):
        self.usb_monitor: USBMonitor = USBMonitor()
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

    def start(self):
        self.usb_monitor.start_monitoring(on_connect=self.on_connect, on_disconnect=self.on_disconnect)

    def stop(self):
        self.usb_monitor.stop_monitoring()

    def join(self):
        pass


class HotkeyMonitor(BaseMonitor):
    def __init__(self, supress: bool = False):
        self.__hotkeys: list[HotKey] = []
        self.__listener: Listener = keyboard.Listener(
            on_press=self.__handle_press,
            on_release=self.__handle_release,
            supress=supress
        )

    def add_hotkey(self, shortcut: str, handler: Callable[[KeyCode], None]):
        self.__hotkeys.append(
            keyboard.HotKey(
                keyboard.HotKey.parse(shortcut),
                handler)
        )

    def __handle_press(self, key: Union[KeyCode, Key]):
        for hk in self.__hotkeys:
            hk.press(self.__listener.canonical(key))

    def __handle_release(self, key: Union[KeyCode, Key]):
        for hk in self.__hotkeys:
            hk.release(self.__listener.canonical(key))

    def start(self):
        self.__listener.start()

    def stop(self):
        self.__listener.stop()

    def join(self):
        self.__listener.join()
