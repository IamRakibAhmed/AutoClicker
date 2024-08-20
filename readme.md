# AutoClicker

AutoClicker is a simple yet powerful tool that automates mouse clicks at a configurable interval. It is designed for users who need repetitive clicking functionality for tasks like automated testing, gaming, or any repetitive operations. The tool is built using Python and leverages `pyautogui` for simulating mouse clicks, with a focus on simplicity, flexibility, and ease of use.

## Features

- **Configurable Clicking Interval:** Set the interval between clicks via a configuration file (`config.yaml`).
- **Keyboard Hotkeys:** Control the auto-clicker with keyboard shortcuts:
  - `Ctrl + Alt + S`: Stop the auto-clicker
  - `Ctrl + Alt + R`: Restart the auto-clicker
  - `Ctrl + Alt + Q`: Exit the program
- **Graceful Shutdown:** Supports clean exit using keyboard hotkeys, ensuring all resources are released properly.
- **Custom Click Functionality:** The click function can be customized to extend the tool for different kinds of interactions.
- **Logging:** Detailed logging with configurable log levels, aiding in debugging and monitoring.
- **Cross-Platform Compatibility:** Works on Windows, macOS, and Linux, using the cross-platform `pyautogui` library.

## Installation

### Prerequisites
- Python 3.6 or higher
- Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Requirements File
Create a `requirements.txt` file containing the following dependencies:

```txt
pyautogui
pyyaml
keyboard
```

## Usage

1. **Configuration:**
   - The tool reads its configuration from a YAML file (`config.yaml`).
   - Sample configuration:

     ```yaml
     interval: 30  # Interval in seconds between clicks
     log_level: INFO  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
     ```

2. **Running the Application:**
   - To start the auto-clicker, simply run the following command:

     ```bash
     python -m auto_clicker
     ```

3. **Stopping and Restarting:**
   - Use the following keyboard shortcuts to control the auto-clicker:
     - **Stop:** `Ctrl + Alt + S`
     - **Restart:** `Ctrl + Alt + R`
     - **Exit:** `Ctrl + Alt + Q`

4. **Exiting the Application:**
   - When you press `Ctrl + Alt + Q`, the application will stop the auto-clicker, clean up resources, and exit.

## Customization

The `AutoClicker` class allows customization of the click behavior. You can pass your own function to handle the click event. By default, it uses `pyautogui.click()` to simulate a standard mouse click.

Example usage with a custom click function:

```python
def custom_click():
    # Custom logic for clicking or interacting
    print("Custom click performed!")

clicker = AutoClicker(interval=30, click_function=custom_click)
clicker.start()
```

## Logging

The logging level can be adjusted via the `config.yaml` file. Available levels include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. Logs provide insight into when clicks occur and when any errors arise.

## Error Handling

The application is designed to handle common exceptions gracefully, logging errors and stopping the clicker in case of issues. If an unhandled exception occurs, the application will stop automatically and log the error for further debugging.

## Configuration File

The `config.yaml` file should be placed in the same directory as the script. The configuration options include:

- **`interval:`** Time in seconds between each click.
- **`log_level:`** The verbosity of logs. Options are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

## Contribution

Contributions are welcome! Please fork this repository and submit a pull request for any features, improvements, or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or support, please reach out to [Rakib Ahmed](mailto:rakibofficial@gmail.com).

---

Thank you for using AutoClicker! Happy clicking!
