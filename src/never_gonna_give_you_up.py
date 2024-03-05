from src.utils.InputMonitors import SysMonitor

from src.utils.InputMonitors import HotkeyMonitor


def handle_ending_shorcut(sys_monitor: SysMonitor):
    print("Exiting...")
    sys_monitor.stop()


def on_connect(device_id, device_info):
    print("New device detected: ", device_id, device_info)


if __name__ == '__main__':
    sys_monitor: SysMonitor = SysMonitor()
    sys_monitor.hotkey_monitor.add_hotkey('<ctrl>+y', lambda: handle_ending_shorcut(sys_monitor))

    sys_monitor.usb_monitor.on_connect = on_connect

    sys_monitor.start()

    sys_monitor.join()
