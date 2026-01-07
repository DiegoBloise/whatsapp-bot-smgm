"""
User interface utilities for WhatsApp Bot SMGM.

This module provides a comprehensive UI management system including screen clearing,
banner display, user input collection, and formatted output. It handles cross-platform
compatibility and provides a consistent user experience across different operating systems.

Author: Diego Bloise
Repository: https://github.com/DiegoBloise/whatsapp-bot-smgm
"""

import os
import sys
from typing import List

from logger import Logger


class UIManager:
    """
    Manages all user interface interactions and displays for the WhatsApp bot.
    
    This class provides static methods for handling various UI tasks including
    screen management, user input collection, message display, and cross-platform
    compatibility. All methods are static to allow easy access without instantiation.
    """

    @staticmethod
    def clear_screen() -> None:
        """
        Clear the terminal screen cross-platform.
        
        Uses 'cls' command for Windows and 'clear' for Unix-like systems
        to provide a clean screen for the application interface.
        """
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix-like systems
            os.system('clear')

    @staticmethod
    def display_banner() -> None:
        """
        Display the application banner with formatted output.
        
        Shows the application title, repository URL, and decorative borders
        using ANSI color codes for visual appeal. Clears the screen first.
        """
        UIManager.clear_screen()
        print("\n{:.^75}".format("\x1b[37;4mhttps://github.com/DiegoBloise\x1b[0m"))
        print("\x1b[1;32m")
        print("-=" * 32)
        print()
        print(f"{'WhatsApp-Bot - Send Message to Group Members':^64}")
        print()
        print("-=" * 32)
        print("\x1b[m")

    @staticmethod
    def get_group_input() -> str:
        """
        Get WhatsApp group name from user input.
        
        Returns:
            str: The group name in lowercase for consistent matching
        """
        return input("\nEnter the group name to search \x1b[1;32m~>>\x1b[m ").lower()

    @staticmethod
    def get_exclusion_input() -> List[str]:
        """
        Get phone number suffixes to exclude from messaging.
        
        Prompts user for the last 4 digits of phone numbers to exclude,
        allowing multiple exclusions separated by spaces.
        
        Returns:
            List[str]: List of phone number suffixes to exclude
        """
        exclusion_text = input(
            "\nEnter the 4 final numbers of all phones\n"
            "you want to exclude separated by spaces\n"
            "Ex: XXXX XXXX XXXX\n\x1b[1;32m~>>\x1b[m "
        )
        return exclusion_text.split(" ") if exclusion_text.strip() else []

    @staticmethod
    def get_message_input() -> str:
        """
        Get message text from user input with newline support.
        
        Allows users to specify line breaks using "\\n" in their input
        for multi-line messages.
        
        Returns:
            str: The complete message text with newline markers
        """
        return input(
            "\nEnter text message (use \"\\n\" to write in another line)\n"
            "Ex: First Line\\nSecond Line\n\x1b[1;32m~>>\x1b[m "
        )

    @staticmethod
    def confirm_message(message_text: str) -> bool:
        """
        Display message confirmation and get user approval.
        
        Shows the formatted message with proper line breaks and prompts
        the user for confirmation before sending.
        
        Args:
            message_text (str): The message to be confirmed
            
        Returns:
            bool: True if user confirms, False otherwise
        """
        print("\x1b[1;33m")
        print("-=" * 32)
        print("\x1b[m")
        Logger.error("Are you sure you want to send\n    the following message?:\n")
        print(message_text.replace("\\n", "\n"))
        print("\x1b[1;33m")
        print("-=" * 32)
        print("\x1b[m")

        response = input("\x1b[1m[Y/N] \x1b[1;32m~>> \x1b[m").lower()
        return response in 'y'

    @staticmethod
    def display_phones(phones: List[str]) -> None:
        """
        Display the extracted phone numbers with count.
        
        Shows the total count of members and lists each phone number
        for user verification before sending messages.
        
        Args:
            phones (List[str]): List of extracted phone numbers
        """
        Logger.info(f"Total members found: {len(phones)}")
        for phone in phones:
            print(phone)

    @staticmethod
    def display_separator() -> None:
        """
        Display a decorative separator line.
        
        Shows a green colored separator line for visual separation
        between different sections of the user interface.
        """
        print("\x1b[1;32m")
        print("-=" * 32)
        print("\x1b[m")

    @staticmethod
    def wait_for_exit() -> None:
        """
        Wait for user input before exiting the application.
        
        Provides cross-platform exit behavior - uses 'pause' command
        on Windows and standard input prompt on Unix-like systems.
        """
        if os.name == 'nt':  # Windows
            os.system('pause')
        else:  # Unix-like systems
            input("Press Enter to continue...")