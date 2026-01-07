# WhatsApp Bot SMGM - Agent Guidelines

## Project Overview

This is a refactored WhatsApp bot with a modular architecture. The project follows clean code principles with proper separation of concerns, type hints, and comprehensive documentation.

## Entry Points

- **Primary**: `python main.py` - Modern refactored version
- **Legacy**: `whatsapp-bot-smgm.py` - Original monolithic version (removed)

## Build/Test Commands
- **Run application**: `python main.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Syntax checking**: `python -m py_compile *.py`
- **Test imports**: `python -c "import config, logger, ui, whatsapp_bot"`

## Code Architecture

### Core Modules
1. **`main.py`** - Application entry point and workflow orchestration
2. **`whatsapp_bot.py`** - Core WhatsApp automation class
3. **`config.py`** - Constants, timeouts, and XPath selectors
4. **`logger.py`** - Colored logging system with multiple levels
5. **`ui.py`** - User interface management and cross-platform utilities

### Module Dependencies
```
main.py
├── config.py
├── logger.py  
├── ui.py
└── whatsapp_bot.py
    ├── config.py
    └── logger.py
```

## Code Style Guidelines

### Type Hints
- **Required**: All functions must have type hints
- **Use**: `from typing import List, Optional, Dict, Any`
- **Format**: `def function_name(param: str) -> bool:`

### Docstrings
- **Format**: Google-style docstrings
- **Module headers**: Include author, repository URL, purpose
- **Function docs**: Args, Returns, Raises sections where applicable
- **Class docs**: Purpose description and Attributes section

### Import Organization
```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports  
import pyautogui
from selenium import webdriver

# Local imports
from config import IS_DEBUG
from logger import Logger
```

### Naming Conventions
- **Functions**: snake_case (`extract_phone_numbers`, `display_banner`)
- **Variables**: snake_case (`group_name`, `phones_to_exclude`)  
- **Constants**: UPPER_SNAKE_CASE (`QR_CODE_TIMEOUT`, `SEND_BUTTON_XPATH`)
- **Classes**: PascalCase (`WhatsAppBot`, `UIManager`, `LogLevel`)
- **Boolean flags**: `is_debug` prefix

### Error Handling
- **Specific exceptions**: Catch `NoSuchElementException`, `TimeoutException`
- **Logging**: Use `Logger.error()` for errors, `Logger.warn()` for warnings
- **Graceful exits**: Clean up browser resources with `bot.cleanup()`
- **User feedback**: Provide clear error messages to users

### Selenium Patterns
- **WebDriverWait**: Always use explicit waits over `sleep()`
- **Constants**: Import XPath selectors from config module
- **Business accounts**: Handle multiple XPath attempts systematically
- **Resource cleanup**: Always quit browser in finally blocks

### UI/Console Patterns
- **Colors**: Use ANSI escape codes from logger module
- **Cross-platform**: Handle Windows/Unix differences in ui.py
- **User prompts**: Clear, formatted prompts with color coding
- **Progress indicators**: Show step-by-step progress to users

## Testing and Validation

### Manual Testing
```bash
# Test each module individually
python -c "import config; print('Config OK')"
python -c "import logger; Logger.info('Test message')"
python -c "import ui; UIManager.display_banner()"
python -c "import whatsapp_bot; print('Bot module OK')"
```

### Integration Testing
```bash
python main.py
# Follow through the workflow without actually sending messages
```

## Development Guidelines

### Adding New Features
1. Add new constants to `config.py`
2. Update relevant class in `whatsapp_bot.py`
3. Add UI methods to `ui.py` if needed
4. Update workflow in `main.py`
5. Update README.md if user-facing

### Fixing XPath Issues
1. Update selectors in `config.py`
2. Test with `python -m py_compile config.py`
3. Verify with manual WhatsApp Web inspection
4. Update setup/ directory with new screenshots if needed

### Debug Mode
- Set `IS_DEBUG = True` in config.py for development
- This enables visible browser mode and verbose logging
- Remember to set back to `False` for production

## Project Quality Standards

- ✅ **Type coverage**: 100% type hints on all functions
- ✅ **Documentation**: Complete docstrings on all modules
- ✅ **Error handling**: Robust exception handling throughout  
- ✅ **Code style**: Consistent formatting and naming
- ✅ **Modularity**: Clear separation of concerns
- ✅ **Testability**: Each module can be tested independently

## Common Pitfalls to Avoid

- ❌ Hardcoding XPath strings (use config.py)
- ❌ Using `time.sleep()` instead of WebDriverWait
- ❌ Missing resource cleanup (call `bot.cleanup()`)
- ❌ Ignoring type hints
- ❌ Not handling business account XPaths
- ❌ Forgetting cross-platform compatibility in UI

## Agent Instructions

When working on this codebase:
1. **Always** add type hints to new functions
2. **Always** include comprehensive docstrings
3. **Always** use constants from config.py
4. **Always** handle errors gracefully
5. **Always** test with `python -m py_compile`
6. **Never** commit without updating documentation
7. **Never** break the modular architecture
8. **Never** ignore cross-platform considerations