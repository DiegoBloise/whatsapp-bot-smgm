"""
Constants and configuration for WhatsApp Bot SMGM.

This module contains all the configuration values, XPath selectors,
timeouts, and other constants used throughout the WhatsApp bot application.

Author: Diego Bloise
Repository: https://github.com/DiegoBloise/whatsapp-bot-smgm
"""

from typing import List, Final

# =============================================================================
# WhatsApp Web XPath Selectors
# =============================================================================

"""XPath selectors for QR code authentication."""
QR_CODE_BOX_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div"
QR_CODE_XPATH: Final[str] = f"{QR_CODE_BOX_XPATH}/div[2]/div[1]/div[2]/div/div/canvas"

"""XPath selectors for navigation elements."""
MESSAGES_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/header/div/div[1]/div/div[1]/span/button"
STATUS_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/header/div/div[1]/div/div[2]/span/button"

"""XPath selectors for group and contact information."""
GROUP_MEMBERS_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/header/div[2]/div[2]/span"
CONTACT_INFO_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/header/div[2]/div/div/div/div/span"

"""XPath selectors for phone number extraction."""
CONTACT_PHONE_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div[2]/span/div/span"

"""Alternative XPath selectors for business accounts (tried in order)."""
BUSINESS_PHONE_XPATHS: Final[List[str]] = [
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[11]/div[3]/div/div/span/span/span",
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[11]/div[2]/div/div/span/span/span",
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[12]/div[3]/div/div/span/span/span"
]

"""XPath selector for message send button."""
SEND_BUTTON_XPATH: Final[str] = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div/div/div[4]/div/span/button"

# =============================================================================
# Element IDs
# =============================================================================

"""Element IDs for key WhatsApp Web components."""
INITIAL_STARTUP_ID: Final[str] = "app"
PANE_SIDE_ID: Final[str] = "pane-side"

# =============================================================================
# Timeout Configuration (in seconds)
# =============================================================================

"""Timeout for QR code scanning and authentication."""
QR_CODE_TIMEOUT: Final[int] = 120

"""Default timeout for element visibility checks."""
ELEMENT_WAIT_TIMEOUT: Final[int] = 30

"""Short timeout for quick element interactions."""
SHORT_WAIT_TIMEOUT: Final[int] = 5

"""Default sleep duration between actions."""
DEFAULT_SLEEP: Final[float] = 0.5

# =============================================================================
# Browser and Window Configuration
# =============================================================================

"""Default browser window size."""
DEFAULT_WINDOW_SIZE: Final[str] = "800,600"

# =============================================================================
# File Paths
# =============================================================================

"""Path for temporary QR code image."""
QR_CODE_IMAGE_PATH: Final[str] = "qrcode.png"

# =============================================================================
# Debug and Development Settings
# =============================================================================

"""Enable debug mode for additional logging and non-headless execution."""
IS_DEBUG: bool = True