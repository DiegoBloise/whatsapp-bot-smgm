# WhatsApp Bot SMGM - Send Messages to Group Members

A modern, modular Python application that uses Selenium WebDriver to extract phone numbers from WhatsApp groups and send bulk messages. The application features a clean architecture with comprehensive error handling and user-friendly interface.

## 🚀 Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **Type Safety**: Full type hints throughout the codebase
- **Error Handling**: Comprehensive error handling and logging
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **User-Friendly**: Colored console output and clear user prompts
- **Phone Extraction**: Extract numbers from both regular contacts and business accounts
- **Message Filtering**: Exclude specific phone numbers from messaging

## 📋 Requirements

- Python 3.7+
- Mozilla Firefox (latest version)
- Python packages (see Installation)

## 🛠️ Installation

### From Source

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/DiegoBloise/whatsapp-bot-smgm.git
   cd whatsapp-bot-smgm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Manual Installation

```bash
pip install selenium==4.15.2 pyautogui==0.9.54 pyperclip==1.8.2
```

**Note**: Please ensure you have the latest version of [Firefox](https://www.mozilla.org/en-US/firefox/new/) installed on your system.

## 🎯 Usage

### Running the Application

```bash
python main.py
```

### Workflow

1. **Launch the application** using `python main.py`
2. **Enter the group name** you want to extract members from
3. **Specify exclusions** (optional) - Enter last 4 digits of phones to exclude
4. **Compose your message** - Use `\\n` for line breaks
5. **Scan QR code** when prompted to authenticate with WhatsApp Web
6. **Review extracted phone numbers** displayed in console
7. **Confirm message sending** when prompted
8. **Monitor progress** as messages are sent

### Example Usage

```
Enter the group name to search ~>> Family Group
Enter the 4 final numbers of all phones you want to exclude separated by spaces
Ex: XXXX XXXX XXXX
~>> 1234 5678
Enter text message (use "\n" to write in another line)
Ex: First Line\nSecond Line
~>> Hello everyone!\nThis is a test message.
```

## 📁 Project Structure

```
whatsapp-bot-smgm/
├── main.py              # Main entry point
├── config.py            # Configuration constants
├── logger.py            # Logging utilities
├── ui.py                # User interface management
├── whatsapp_bot.py      # Core WhatsApp bot functionality
├── requirements.txt     # Python dependencies
├── setup/              # XPath reference images
└── README.md           # This file
```

## 🔧 Configuration

The application can be configured by modifying `config.py`:

- **Debug Mode**: Set `IS_DEBUG = False` for headless operation
- **Timeouts**: Adjust various timeout values for different operations
- **Window Size**: Modify browser window dimensions
- **XPath Selectors**: Update WhatsApp Web element selectors if needed

## 🐛 Troubleshooting

### Common Issues

1. **Firefox not found**: Ensure Firefox is installed and in system PATH
2. **QR code not loading**: Check internet connection and try again
3. **Element not found**: WhatsApp Web interface may have changed
4. **Permission denied**: Ensure no other browser instances are running

### Debug Mode

Enable debug mode in `config.py`:
```python
IS_DEBUG = True
```

This will:
- Run browser in visible mode (not headless)
- Provide additional logging output
- Keep browser open after execution

## ⚠️ Caution

**Educational Purpose Only**: This script is intended for educational purposes and legitimate use only.

**Legal Compliance**: 
- Always comply with WhatsApp's Terms of Service
- Respect privacy and consent of recipients
- Follow local regulations regarding automated messaging
- Do not use for spam or unsolicited communications

**Use at Your Own Risk**: The authors are not responsible for any misuse of this software or any resulting legal consequences.

## 📝 Development

### Code Style

This project follows Python best practices:
- **Type Hints**: All functions include proper type annotations
- **Docstrings**: Comprehensive documentation using Google-style format
- **Error Handling**: Robust exception handling throughout
- **Modular Design**: Clear separation of concerns

### Running Tests

```bash
python -m py_compile *.py  # Syntax checking
python main.py             # Manual testing
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the terms specified in the `license` file.

## 👤 Author

**Diego Bloise**
- GitHub: [DiegoBloise](https://github.com/DiegoBloise)
- Repository: [whatsapp-bot-smgm](https://github.com/DiegoBloise/whatsapp-bot-smgm)

---

**Disclaimer**: This tool should be used responsibly and in compliance with all applicable laws and platform terms of service.