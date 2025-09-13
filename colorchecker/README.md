# ColorChecker Project

## Overview
ColorChecker is a project aimed at reliably detecting colors and matching them with data from JSON databases. The system utilizes a camera for live color capture, an OLED display for status updates, and buttons for user interaction.

## Features
- **Color Detection**: Capture and identify colors using a camera.
- **Web UI**: A lightweight web interface for remote access and configuration.
- **OLED Display**: Displays current status and color results.
- **User Interaction**: Buttons for capturing colors, navigating results, and confirming selections.

## Project Structure
```
colorchecker
├── src
│   ├── camera               # Camera capture functionalities
│   ├── ui_web               # Web UI components
│   ├── oled                 # OLED display control
│   ├── buttons              # Button handling
│   ├── leds                 # LED control
│   ├── processing           # Image processing and color matching
│   ├── db                   # Database handling
│   ├── config               # Configuration settings
│   └── __init__.py          # Package initialization
├── tests                    # Unit tests
├── docs                     # Documentation
├── data                     # Data files
├── .vscode                  # VS Code configurations
├── pyproject.toml           # Project configuration
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image instructions
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd colorchecker
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
- Start the web server:
  ```
  python src/ui_web/server.py
  ```
- Access the web interface via your browser at `http://localhost:8000`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.