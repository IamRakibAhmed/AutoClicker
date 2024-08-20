import pyautogui
import threading
import logging
import signal
import sys
import yaml
import os
import keyboard

class AutoClicker:
    def __init__(self, interval, click_function=None):
        """
        Initializes the AutoClicker with a given interval.
        """
        self.interval = interval
        self.timer = None
        self.click_function = click_function if click_function else pyautogui.click
        self.stopped = False

    def start(self):
        """Starts the auto-clicking process."""
        logging.info("Auto clicker started.")
        self.stopped = False
        self.schedule_next_click()

    def schedule_next_click(self):
        """Schedules the next click after the specified interval."""
        if not self.stopped:
            try:
                self.click_function()
                logging.info("Mouse clicked.")
                self.timer = threading.Timer(self.interval, self.schedule_next_click)
                self.timer.daemon = True  # Set the timer thread as a daemon
                self.timer.start()
            except Exception as e:
                logging.error(f"An error occurred while clicking: {e}")
                self.stop()

    def stop(self):
        """Stops the auto-clicking process."""
        if not self.stopped:
            self.stopped = True
            if self.timer:
                self.timer.cancel()
            logging.info("Auto clicker stopped.")

    def restart(self):
        """Restarts the auto-clicking process."""
        logging.info("Auto clicker restarting.")
        self.stop()
        self.start()

def load_config(config_file="config.yaml"):
    """
    Loads configuration from the specified YAML file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    config_path = os.path.join(script_dir, config_file)

    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        sys.exit(1)

def setup_logging(log_level):
    """Sets up the logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()), 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def handle_exit(clicker):
    """Handles graceful shutdown on exit hotkey."""
    logging.info("Exit signal received. Shutting down.")
    clicker.stop()
    sys.exit(0)  # Direct exit

def setup_hotkeys(clicker, exit_flag):
    """Configures the hotkeys for stop, restart, and exit."""
    keyboard.add_hotkey('ctrl+alt+s', clicker.stop)
    keyboard.add_hotkey('ctrl+alt+r', clicker.restart)
    keyboard.add_hotkey('ctrl+alt+q', lambda: exit_flag.set())  # Set exit flag
    logging.info("Hotkeys configured: Stop (Ctrl+Alt+S), Restart (Ctrl+Alt+R), Exit (Ctrl+Alt+Q)")

def main():
    config = load_config()
    interval = config.get("interval", 30)
    log_level = config.get("log_level", "INFO")

    setup_logging(log_level)

    clicker = AutoClicker(interval=interval)
    exit_flag = threading.Event()  # Exit flag for controlling the main loop
    
    signal.signal(signal.SIGINT, lambda s, f: exit_flag.set())  # Exit on Ctrl+C
    signal.signal(signal.SIGTERM, lambda s, f: exit_flag.set())  # Exit on SIGTERM

    setup_hotkeys(clicker, exit_flag)

    try:
        clicker.start()
        while not exit_flag.is_set():
            pass  # Keep the program running, check the exit flag
        handle_exit(clicker)
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        clicker.stop()
        sys.exit(1)
