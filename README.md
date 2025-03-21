Insanity MMORPG Tool

This tool allows you to manage and send input to Insanity MMORPG game windows, making it easier to control multiple clients with automatic keyboard handling.

Features:

Automatic client detection: Identifies open game windows.

Primary and secondary client selection: Choose which client to control.

Automatic key sending to the secondary client: Replicates key presses from the primary client to the secondary one.

Customizable key mapping: Configure function keys (F1-F9) and save settings to a file.

Prerequisites:

To run this script correctly, you need to have the following installed:

Python 3.x: The programming language required to execute the script.

Tkinter: GUI library included by default in Python.

pywin32: Library for interacting with Windows windows.

json: Library for handling configurations (included by default in Python).

Installing Prerequisites:

If you don’t have Python installed, download and install it from https://www.python.org/. Make sure to select the "Add Python to PATH" option during installation.

To install the required libraries, run the following command in the terminal:

pip install pywin32

Usage:

Launch the game and open at least two clients.

Click "Attach Client" to detect open game windows.

Select a client from the list and click "Select Client".

Configure the key mapping if necessary and save the settings.

Press the configured keys in the primary client to send them automatically to the secondary one.

Saving Settings

Key configurations are saved in the keymapping.json file, allowing you to keep your settings even after closing the program.


Troubleshooting:

If the clients are not detected, ensure that the game is running and visible.

If keys are not being sent, check that the secondary client has been selected correctly.

If the script does not start, verify that Python and the required libraries are properly installed.


Notes:

Works only on Windows.

The program must be run with administrative privileges to function correctly.

This tool is designed to facilitate multitasking in game clients and should not be used to violate server rules.

Original Project

This project is based on: GitHub - iT0xic/Python-FTool

Author: Effy.
Version: 1.0

