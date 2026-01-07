"""
Main entry point for WhatsApp Bot SMGM.

This script serves as the primary entry point for the WhatsApp bot application.
It orchestrates the entire workflow from user input collection through
WhatsApp Web automation, phone number extraction, and message sending.

Author: Diego Bloise
Repository: https://github.com/DiegoBloise/whatsapp-bot-smgm

Usage:
    python main.py
"""

from typing import List

from config import IS_DEBUG
from logger import Logger
from ui import UIManager
from whatsapp_bot import WhatsAppBot


def filter_phones(phones: List[str], exclude_suffixes: List[str]) -> List[str]:
    """
    Filter out phones based on their suffixes.
    
    Removes phone numbers whose last 4 digits match any of the provided
    exclusion suffixes, allowing users to exclude specific numbers from messaging.
    
    Args:
        phones (List[str]): List of phone numbers to filter
        exclude_suffixes (List[str]): List of 4-digit suffixes to exclude
        
    Returns:
        List[str]: Filtered list of phone numbers
    """
    if not exclude_suffixes:
        return phones
    
    filtered = []
    for phone in phones:
        # Get last 4 digits for comparison
        phone_suffix = phone[-4:] if len(phone) >= 4 else phone
        if phone_suffix not in exclude_suffixes:
            filtered.append(phone)

    return filtered


def main() -> None:
    """
    Main application function that orchestrates the entire workflow.
    
    This function handles the complete application flow:
    1. Display user interface and collect inputs
    2. Initialize WhatsApp bot with appropriate settings
    3. Authenticate with WhatsApp Web
    4. Navigate to specified group and extract phone numbers
    5. Display results and confirm with user
    6. Send messages to filtered list of recipients
    7. Handle errors and cleanup resources
    
    The function includes comprehensive error handling for various failure scenarios
    and ensures proper cleanup of browser resources.
    """
    # Display banner
    UIManager.display_banner()

    # Get user inputs
    group_name = UIManager.get_group_input()
    phones_to_exclude = UIManager.get_exclusion_input()
    message_text = UIManager.get_message_input()

    UIManager.display_separator()

    # Initialize bot
    bot = WhatsAppBot(headless=not IS_DEBUG)

    try:
        # Start WhatsApp and handle authentication
        bot.start_whatsapp()

        # Find the group
        bot.find_group(group_name)

        # Extract phone numbers
        phones = bot.get_group_phones()

        # Display results
        UIManager.display_phones(phones)

        # Confirm message sending
        if UIManager.confirm_message(message_text):
            # Filter phones if exclusions specified
            filtered_phones = filter_phones(phones, phones_to_exclude)

            print("\n\n")
            # Send messages
            for i, phone in enumerate(filtered_phones):
                Logger.warn(f"Sending message {i+1} to: {phone}")
                bot.send_message(phone, message_text)
        else:
            Logger.error("Operation aborted by user.")

    except KeyboardInterrupt:
        Logger.error("Operation interrupted by user.")
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
    finally:
        # Clean up
        bot.cleanup()
        UIManager.wait_for_exit()
        Logger.success("All done!")


if __name__ == "__main__":
    main()