"""
Logging utilities for WhatsApp Bot SMGM.

This module provides a comprehensive logging system with colored console output
for different log levels. It includes both a class-based approach for new code
and legacy function compatibility.

Author: Diego Bloise
Repository: https://github.com/DiegoBloise/whatsapp-bot-smgm
"""

import sys
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """
    Enumeration of available log levels for the application.
    
    Each level corresponds to a specific color and prefix in the console output:
    - INFO: Yellow color, [*] prefix
    - SUCCESS: Bold green color, [+] prefix  
    - WARN: Bold yellow color, [+] prefix
    - ERROR: Bold red color, [!] prefix
    """
    INFO = "info"
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


class Logger:
    """
    Custom logger with colored console output.
    
    This class provides static methods for logging messages at different levels
    with appropriate colors and formatting. It uses ANSI escape sequences for
    terminal colors and supports different log levels with distinct visual styles.
    
    Attributes:
        COLORS (dict): Mapping of log levels to ANSI color codes
        RESET (str): ANSI escape code to reset formatting
        BOLD (str): ANSI escape code for bold text
    """

    # ANSI color codes for different log levels
    COLORS = {
        LogLevel.INFO: "\x1b[33m",      # Yellow
        LogLevel.SUCCESS: "\x1b[1;32m", # Bold Green
        LogLevel.WARN: "\x1b[1;33m",    # Bold Yellow
        LogLevel.ERROR: "\x1b[1;31m",   # Bold Red
    }

    # ANSI escape codes for text formatting
    RESET = "\x1b[m"
    BOLD = "\x1b[1m"

    @classmethod
    def log(cls, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """
        Log a message with the specified level and formatting.
        
        Args:
            message (str): The message to log
            level (LogLevel): The log level (defaults to INFO)
        """
        prefix = ""
        color = cls.COLORS.get(level, "")

        if level == LogLevel.INFO:
            prefix = f"{cls.BOLD}[*]{cls.RESET} "
        elif level in (LogLevel.SUCCESS, LogLevel.WARN):
            prefix = f"{cls.BOLD}[+]{cls.RESET} "
        elif level == LogLevel.ERROR:
            prefix = f"{cls.BOLD}[!]{cls.RESET} "

        print(f"{prefix}{color}{message}{cls.RESET}")

    @classmethod
    def info(cls, message: str) -> None:
        """Log an info message."""
        cls.log(message, LogLevel.INFO)

    @classmethod
    def success(cls, message: str) -> None:
        """Log a success message."""
        cls.log(message, LogLevel.SUCCESS)

    @classmethod
    def warn(cls, message: str) -> None:
        """Log a warning message."""
        cls.log(message, LogLevel.WARN)

    @classmethod
    def error(cls, message: str) -> None:
        """Log an error message."""
        cls.log(message, LogLevel.ERROR)


# =============================================================================
# Legacy Compatibility Functions
# =============================================================================

def message(text: str, severity: str = 'info') -> None:
    """
    Legacy message function for backward compatibility.
    
    This function provides compatibility with the original codebase's
    message() function while internally using the new Logger class.
    
    Args:
        text (str): The message to display
        severity (str): The severity level ('info', 'success', 'warn', 'error')
    """
    level_map = {
        'info': LogLevel.INFO,
        'success': LogLevel.SUCCESS,
        'warn': LogLevel.WARN,
        'error': LogLevel.ERROR,
    }
    level = level_map.get(severity, LogLevel.INFO)
    Logger.log(text, level)