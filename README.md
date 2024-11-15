# Discord Token Onliner

A simple and efficient tool for automating the management of Discord accounts with custom statuses. This project allows you to login to multiple Discord accounts (using tokens), set dynamic activity statuses (e.g., playing, watching, listening, streaming), and monitor these accounts concurrently.

## Features

- **Login with Discord tokens**: Validate and authenticate using user-provided Discord tokens.
- **Random Activity Generator**: Set dynamic activity statuses like "Playing", "Watching", "Listening", and "Streaming".
- **Concurrent Bot Management**: Support for managing multiple Discord accounts simultaneously.
- **User-Friendly Interface**: Print login and status updates to the console with detailed logs.
- **Input Monitoring**: Stop the program by pressing 's' anytime.

## Requirements

- Python 3.x
- `discord.py`: For interacting with Discord's API.
- `requests`: For token validation.
- `pystyle`: For styled output in the terminal.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AxZeRxD/Discord-Token-Onliner.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Discord-Token-Onliner
   ```
3. Create Python Venv:
   ```bash
   python -m venv aizer
   ```
4. Activate venv
   ```bash
   aizer\Scripts\activate
   ```
5. Install Required Module
   ```bash
   pip install discord requests pystyle discord.py-self
   ```

## Usage

1. **Prepare your tokens**: Create a file named `tokens.txt` in the `data` directory and list each Discord token on a new line.
2. **Prepare your activity data**: Create a `data.json` file with predefined activities (e.g., `Playing`, `Watching`) and corresponding status messages.
3. Run the program:
   ```bash
   python main.py
   ```

## Contributing

If you want to contribute to the project, feel free to fork this repository, make improvements, and create a pull request. All contributions are welcome!

## Disclaimer

This tool is for educational purposes only. Using it to spam or misuse Discord's API can lead to account bans. Please use responsibly and in accordance with Discord's Terms of Service.
