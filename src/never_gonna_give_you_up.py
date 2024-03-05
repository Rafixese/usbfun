from src.utils.InputMonitors import HotkeyMonitor, USBDeviceMonitor, MouseMonitor, BaseMonitor


class MonitorManager:
    def __init__(self):
        self.hotkey_monitor: HotkeyMonitor = None
        self.usb_monitor: USBDeviceMonitor = None
        self.mouse_monitor: MouseMonitor = None

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


monitor_manager = MonitorManager()


def stop_script():
    print("Exiting...")
    monitor_manager.stop_all()


def on_connect(device_id, device_info):
    print("New device detected: ", device_id, device_info)


if __name__ == '__main__':
    monitor_manager.hotkey_monitor = HotkeyMonitor(supress=False)
    monitor_manager.usb_monitor = USBDeviceMonitor(on_connect=on_connect)

    monitor_manager.hotkey_monitor.add_hotkey('<ctrl>+y', stop_script)
    monitor_manager.usb_monitor.on_connect = on_connect

    monitor_manager.hotkey_monitor.start()
    monitor_manager.usb_monitor.start()

    monitor_manager.join_all()
