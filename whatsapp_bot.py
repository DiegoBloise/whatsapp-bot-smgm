"""
WhatsApp Bot SMGM - Core functionality.

This module contains the main WhatsAppBot class that handles all interactions
with WhatsApp Web, including authentication, group navigation, phone number
extraction, and message sending. It uses Selenium WebDriver for browser automation
and provides a clean, object-oriented interface for WhatsApp operations.

Author: Diego Bloise
Repository: https://github.com/DiegoBloise/whatsapp-bot-smgm
"""

import os
import sys
from typing import List, Optional
from time import sleep

import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config import (
    QR_CODE_BOX_XPATH, QR_CODE_XPATH, MESSAGES_XPATH, STATUS_XPATH,
    GROUP_MEMBERS_XPATH, CONTACT_INFO_XPATH, CONTACT_PHONE_XPATH,
    BUSINESS_PHONE_XPATHS, SEND_BUTTON_XPATH, INITIAL_STARTUP_ID,
    PANE_SIDE_ID, QR_CODE_TIMEOUT, ELEMENT_WAIT_TIMEOUT,
    SHORT_WAIT_TIMEOUT, DEFAULT_SLEEP, DEFAULT_WINDOW_SIZE,
    QR_CODE_IMAGE_PATH, IS_DEBUG
)
from logger import Logger


class WhatsAppBot:
    """
    Main WhatsApp bot class for group member extraction and messaging.
    
    This class provides a high-level interface for interacting with WhatsApp Web
    through Selenium WebDriver. It handles authentication, group navigation,
    phone number extraction from both regular contacts and business accounts,
    and bulk message sending with proper error handling and logging.
    
    Attributes:
        browser (Optional[webdriver.Firefox]): The Firefox WebDriver instance
        headless (bool): Whether to run in headless mode (except in debug)
    """

    def __init__(self, headless: bool = False) -> None:
        """
        Initialize the WhatsApp bot with WebDriver configuration.
        
        Args:
            headless (bool): Whether to run in headless mode. Ignored if
                           IS_DEBUG is True to allow visual debugging.
        """
        self.browser: Optional[webdriver.Firefox] = None
        self.headless = headless and not IS_DEBUG
        self._setup_driver()

    def _setup_driver(self) -> None:
        """Setup Firefox WebDriver with appropriate options."""
        try:
            options = Options()
            options.add_argument(f"window-size={DEFAULT_WINDOW_SIZE}")
            if self.headless:
                options.add_argument("--headless")

            self.browser = webdriver.Firefox(options=options)
            Logger.success("WebDriver started successfully")
        except Exception as e:
            Logger.error(f"Could not start WebDriver: {e}")
            sys.exit(1)

    def start_whatsapp(self) -> None:
        """Start WhatsApp Web and handle QR code authentication."""
        if not self.browser:
            Logger.error("Browser not initialized")
            return

        try:
            Logger.info("Accessing WhatsApp Web...")
            self.browser.get("https://web.whatsapp.com/")

            # Wait for initial startup
            wait = WebDriverWait(self.browser, QR_CODE_TIMEOUT)
            wait.until(EC.visibility_of_element_located((By.ID, INITIAL_STARTUP_ID)))

            # Handle QR code
            self._handle_qr_code()

            # Wait for main interface to load
            Logger.info("Loading main interface...")
            wait.until(EC.visibility_of_element_located((By.ID, PANE_SIDE_ID)))
            Logger.success("WhatsApp Web ready!")
            sleep(DEFAULT_SLEEP * 2)

        except Exception as e:
            Logger.error(f"Could not access WhatsApp Web: {e}")
            self.cleanup()
            sys.exit(1)

    def _handle_qr_code(self) -> None:
        """Handle QR code scanning process."""
        if not self.browser:
            return

        try:
            Logger.info("Loading QR Code...")
            wait = WebDriverWait(self.browser, ELEMENT_WAIT_TIMEOUT)
            wait.until(EC.visibility_of_element_located((By.XPATH, QR_CODE_XPATH)))

            # Save and display QR code
            qr_element = self.browser.find_element(By.XPATH, QR_CODE_BOX_XPATH)
            qr_element.screenshot(QR_CODE_IMAGE_PATH)

            Logger.success("Scan the QR code to continue...")
            self._open_qr_code_image()

            # Wait for QR code to disappear (login successful)
            wait.until(EC.invisibility_of_element_located((By.XPATH, QR_CODE_BOX_XPATH)))
            self._cleanup_qr_code()

        except TimeoutException:
            Logger.error("QR code loading timeout")
            self.cleanup()
            sys.exit(1)
        except Exception as e:
            Logger.error(f"QR code handling failed: {e}")
            self.cleanup()
            sys.exit(1)

    def _open_qr_code_image(self) -> None:
        """Open QR code image for scanning."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(QR_CODE_IMAGE_PATH)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{QR_CODE_IMAGE_PATH}"' if sys.platform == 'darwin' else f'xdg-open "{QR_CODE_IMAGE_PATH}"')
        except Exception as e:
            Logger.warn(f"Could not open QR code image: {e}")

    def _cleanup_qr_code(self) -> None:
        """Clean up QR code image file."""
        try:
            if os.path.exists(QR_CODE_IMAGE_PATH):
                os.remove(QR_CODE_IMAGE_PATH)
        except Exception as e:
            Logger.warn(f"Could not remove QR code image: {e}")

    def find_group(self, group_name: str) -> None:
        """Find and navigate to a specific WhatsApp group."""
        if not self.browser:
            return

        try:
            Logger.info("Searching for group...")

            # Navigate to messages
            self.browser.find_element(By.XPATH, STATUS_XPATH).click()
            sleep(DEFAULT_SLEEP * 2)
            self.browser.find_element(By.XPATH, MESSAGES_XPATH).click()
            sleep(DEFAULT_SLEEP)
            self.browser.find_element(By.XPATH, MESSAGES_XPATH).click()
            sleep(DEFAULT_SLEEP)
            self.browser.find_element(By.XPATH, MESSAGES_XPATH).click()

            sleep(DEFAULT_SLEEP * 2)

            # Search for group
            pyautogui.press('tab', presses=4)
            sleep(DEFAULT_SLEEP)

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('delete')
            sleep(DEFAULT_SLEEP * 4)

            pyperclip.copy(group_name)
            sleep(DEFAULT_SLEEP / 2)

            pyautogui.hotkey('ctrl', 'v')
            sleep(DEFAULT_SLEEP)

            sleep(DEFAULT_SLEEP)
            pyautogui.press('down')
            sleep(DEFAULT_SLEEP / 5)
            pyautogui.press('space')
            sleep(DEFAULT_SLEEP)

            Logger.success(f"Group '{group_name}' found")

        except NoSuchElementException as e:
            Logger.error(f"Group not found: {e}")
            input("Press Enter to exit...")
            self.cleanup()
            sys.exit(1)

    def get_group_phones(self) -> List[str]:
        """Extract phone numbers from group members."""
        if not self.browser:
            return []

        try:
            Logger.info("Extracting phone numbers from group members...")

            wait = WebDriverWait(self.browser, SHORT_WAIT_TIMEOUT)
            wait.until(EC.text_to_be_present_in_element((By.XPATH, GROUP_MEMBERS_XPATH), ", "))

            members = self.browser.find_element(By.XPATH, GROUP_MEMBERS_XPATH).text.split(", ")
            phones = []

            for index, member in enumerate(members):
                if member.replace("+", "").replace(" ", "").replace("-", "").isnumeric():
                    phones.append(member)
                else:
                    Logger.info(f"Saved contact found: {member}")
                    phone = self._extract_phone_from_contact(member)
                    if phone:
                        Logger.success(f"Phone extracted: {phone}")
                        phones.append(phone)
                    else:
                        Logger.warn(f"Could not extract phone for: {member}")

            return phones

        except NoSuchElementException as e:
            Logger.error(f"Could not access group members: {e}")
            self.cleanup()
            sys.exit(1)

    def _extract_phone_from_contact(self, contact_name: str) -> Optional[str]:
        """Extract phone number from a saved contact."""
        if not self.browser:
            return None

        try:
            # Navigate to contact info
            self.find_group(contact_name)
            sleep(DEFAULT_SLEEP * 2)

            self.browser.find_element(By.XPATH, CONTACT_INFO_XPATH).click()
            sleep(DEFAULT_SLEEP * 2)

            # Try to get phone number
            try:
                phone = self.browser.find_element(By.XPATH, CONTACT_PHONE_XPATH).text
                return phone
            except NoSuchElementException:
                Logger.info("Business account detected, trying alternative XPaths...")

                for xpath in BUSINESS_PHONE_XPATHS:
                    try:
                        phone = self.browser.find_element(By.XPATH, xpath).text
                        return phone
                    except NoSuchElementException:
                        continue

                Logger.error("Phone number not found for business account")
                return None

        except Exception as e:
            Logger.error(f"Error extracting phone from contact: {e}")
            return None

    def send_message(self, phone: str, message: str) -> bool:
        """Send a message to a specific phone number."""
        if not self.browser:
            return False

        try:
            # Format message for URL
            formatted_message = message.replace("\\n", "%0A")
            url = f"https://web.whatsapp.com/send?phone={phone}&text={formatted_message}"

            self.browser.get(url)
            Logger.info(f"Preparing message for {phone}...")

            # Wait for send button to be available
            wait = WebDriverWait(self.browser, ELEMENT_WAIT_TIMEOUT)
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))

            send_button = self.browser.find_element(By.XPATH, SEND_BUTTON_XPATH)
            sleep(DEFAULT_SLEEP * 6)

            send_button.click()
            Logger.success(f"Message sent to {phone}")
            sleep(DEFAULT_SLEEP * 2)

            return True

        except Exception as e:
            Logger.error(f"Could not send message to {phone}: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up browser resources."""
        if self.browser:
            try:
                self.browser.quit()
                Logger.info("Browser closed")
            except Exception as e:
                Logger.error(f"Error closing browser: {e}")