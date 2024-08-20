import pyautogui
import threading
import logging
import signal
import sys
import yaml
import os

class AutoClicker:
    def __init__(self, interval, click_function=None):
        """
        Initializes the AutoClicker with a given interval.

        :param interval: Time in seconds between each click.
        :param click_function: The function to perform the click. Defaults to pyautogui.click.
        """
        self.interval = interval
        self.timer = None
        self.click_function = click_function if click_function else pyautogui.click
        self.stopped = False

    def start(self):
        """Starts the auto-clicking process."""
        logging.info("Auto clicker started. Press Ctrl+C to stop.")
        self.schedule_next_click()

    def schedule_next_click(self):
        """Schedules the next click after the specified interval."""
        if not self.stopped:
            try:
                self.click_function()
                logging.info("Mouse clicked.")
                self.timer = threading.Timer(self.interval, self.schedule_next_click)
                self.timer.start()
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                self.stop()

    def stop(self):
        """Stops the auto-clicking process."""
        self.stopped = True
        if self.timer:
            self.timer.cancel()
        logging.info("Auto clicker stopped.")

def load_config(config_file="config.yaml"):
    """
    Loads configuration from the specified YAML file.
    Looks for the file relative to the script's directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    config_path = os.path.join(script_dir, config_file)  # Full path to config.yaml

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        sys.exit(1)

def handle_exit(signal_received, frame, clicker):
    """Handles graceful shutdown on SIGINT or SIGTERM."""
    logging.info("Exit signal received.")
    clicker.stop()
    threading.Timer(1.0, sys.exit, [0]).start()

def main():
    config = load_config()
    interval = config.get("interval", 30)
    log_level = config.get("log_level", "INFO")

    logging.basicConfig(level=getattr(logging, log_level.upper()), 
                        format='%(asctime)s - %(levelname)s - %(message)s')

    clicker = AutoClicker(interval=interval)

    signal.signal(signal.SIGINT, lambda s, f: handle_exit(s, f, clicker))
    signal.signal(signal.SIGTERM, lambda s, f: handle_exit(s, f, clicker))

    try:
        clicker.start()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        clicker.stop()
        sys.exit(1)
