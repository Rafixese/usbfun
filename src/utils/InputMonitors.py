from usbmonitor import USBMonitor
from typing import Callable, Union

from pynput import keyboard
from pynput.keyboard import HotKey
from pynput.keyboard._base import Listener, KeyCode, Key


class SysMonitor:
    def __init__(self):
        self.hotkey_monitor: HotkeyMonitor = HotkeyMonitor()
        self.usb_monitor: USBDeviceMonitor = USBDeviceMonitor()

    def start(self):
        self.usb_monitor.start()
        self.hotkey_monitor.start()

    def stop(self):
        self.usb_monitor.stop()
        self.hotkey_monitor.stop()

    def join(self):
        self.hotkey_monitor.join()


class USBDeviceMonitor:
    def __init__(self, on_connect: Callable | None = None, on_disconnect: Callable | None = None):
        self.usb_monitor: USBMonitor = USBMonitor()
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

    def start(self):
        self.usb_monitor.start_monitoring(on_connect=self.on_connect, on_disconnect=self.on_disconnect)

    def stop(self):
        self.usb_monitor.stop_monitoring()


class HotkeyMonitor:
    def __init__(self):
        self.__hotkeys: list[HotKey] = []
        self.__listener: Listener = keyboard.Listener(
            on_press=self.__handle_press,
            on_release=self.__handle_release
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
