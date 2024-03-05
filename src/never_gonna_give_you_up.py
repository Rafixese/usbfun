from src.utils.InputMonitors import HotkeyMonitor


def handle_ending_shorcut(hm: HotkeyMonitor):
    print("Exiting...")
    hm.stop()


if __name__ == '__main__':
    hm: HotkeyMonitor = HotkeyMonitor()
    hm.add_hotkey('<ctrl>+y', lambda: handle_ending_shorcut(hm))
    hm.start()
    hm.join()
