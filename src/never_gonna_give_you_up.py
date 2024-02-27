from typing import Callable, Union

from pynput import keyboard
from pynput.keyboard import HotKey
from pynput.keyboard._base import Listener, KeyCode, Key


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


def handle_ending_shorcut(hm: HotkeyMonitor):
    print("Exiting...")
    hm.stop()


if __name__ == '__main__':
    hm: HotkeyMonitor = HotkeyMonitor()
    hm.add_hotkey('<ctrl>+y', lambda: handle_ending_shorcut(hm))
    hm.start()
    hm.join()
