import pyautogui
import pyperclip
from os import system
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# Elements XPATH
initial_startup = "app"

qr_code_box_xpath = "/html/body/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div"
qr_code_xpath = f"{qr_code_box_xpath}/div[2]/div[1]/div[2]/div/div/canvas"

messages_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/header/div/div[1]/div/div[1]/span/button"
status_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/header/div/div[1]/div/div[2]/span/button"

group_members_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/header/div[2]/div[2]/span"
contact_info_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/header/div[2]/div/div/div/div/span"

contact_phone_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/div[2]/span/div/span"
business_phone_xpaths = [
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[11]/div[3]/div/div/span/span/span",
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[11]/div[2]/div/div/span/span/span",
    "/html/body/div[1]/div/div/div/div/div[3]/div/div[6]/span/div/span/div/div/section/div[12]/div[3]/div/div/span/span/span"
]
send_button_xpath = "/html/body/div[1]/div/div/div/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div/div/div[4]/div/span/button"

# Flags
isDebug = True


def message(text, severity = 'info'):
    if severity == 'info':
        print(f"\x1b[1m[*]\x1b[m \x1b[33m{text}\x1b[m")
    elif severity == 'success':
        print(f"\x1b[1m[+]\x1b[m \x1b[1;32m{text}\x1b[m")
    elif severity == 'warn':
        print(f"\x1b[1m[+]\x1b[m \x1b[1;33m{text}\x1b[m")
    elif severity == 'error':
        print(f"\x1b[1m[!]\x1b[m \x1b[1;31m{text}\x1b[m")


def find_subject(browser, subject_name):
    try:
        message(text="Searching subject...")

        browser.find_element(By.XPATH, status_xpath).click()
        sleep(1)
        browser.find_element(By.XPATH, messages_xpath).click()
        sleep(0.5)
        browser.find_element(By.XPATH, messages_xpath).click()
        sleep(0.5)
        browser.find_element(By.XPATH, messages_xpath).click()

        sleep(1)

        pyautogui.press('tab', presses=4)

        sleep(1)

        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('delete')

        sleep(2) 

        pyperclip.copy(subject_name)
        sleep(0.2)

        pyautogui.hotkey('ctrl', 'v')
        sleep(0.5)


        sleep(1)
        pyautogui.press('down')
        sleep(0.1)
        pyautogui.press('space')
        sleep(1)

        return

    except NoSuchElementException as e:
        message(text=f"Subject element not found: {e}", severity='error')
        input()
        browser.quit()
        exit()


def get_phones(browser):
    try:
        message(text="Getting phone list...")

        wait = WebDriverWait(browser, 5)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, group_members_xpath), ", "))

        subjects = browser.find_element(By.XPATH, group_members_xpath).text.split(", ")
        for index, subject in enumerate(subjects):
            if not subject.replace("+", "").replace(" ", "").replace("-", "").isnumeric():
                message(text="Saved contact found:\x1b[m \x1b[1m{subject}")

                message(text="Extracting phone number...")

                find_subject(browser, subject)
                phone_number = get_phone_number(browser)

                if phone_number != None:
                    message(text=f"Success... | Phone: {phone_number}", severity='success')
                    subjects[index] = phone_number
                else:
                    message(text="Number not found...")

        return subjects

    except NoSuchElementException as e:
        message(text=f"Phones list element not found: {e}", severity='error')
        browser.quit()
        exit()


def get_phone_number(browser):
    try:
        browser.find_element(By.XPATH, contact_info_xpath).click()
        sleep(2)

    except NoSuchElementException as e:
        message(text=f"Contact info element not found: {e}", severity='error')
        browser.quit()
        exit()

    try:
        phone = browser.find_element(By.XPATH, contact_phone_xpath).text

    except:
        message(text="Number not found: It's a business account")
        try:
            phone = browser.find_element(By.XPATH, business_phone_xpaths[0]).text
        except NoSuchElementException as e:
            message(text="Number not found: Trying another xpath...")
            try:
                phone = browser.find_element(By.XPATH, business_phone_xpaths[1]).text
            except NoSuchElementException as e:
                message(text="Number not found: Trying another xpath...")
                try:
                    phone = browser.find_element(By.XPATH, business_phone_xpaths[2]).text
                except NoSuchElementException as e:
                    message(text=f"Number not found: {e}", severity='error')
                    phone = None
    return phone


def send_text(browser, phone, text):
    # try:
    try:
        text = text.replace("\\n", "%0A")
        browser.get(f"https://web.whatsapp.com/send?phone={phone}&text={text}")

    except Exception as e:
        message(text=f"Could not send message: {e}", severity='error')
        message("Skipping...")
        # browser.quit()
        # exit()

    message(text="Waiting to send the message...")

    wait = WebDriverWait(browser, 30)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "footer")))
    send_button = browser.find_element(By.XPATH, send_button_xpath)

    sleep(3)
    send_button.click()

    message(text=f"Message sent to phone: {phone}", severity='success')
    sleep(2)
    # except Exception as e:
    #     message(text=f"Error: {e}", severity='error')
    #     browser.quit()
    #     exit()


def banner():
    system("cls")
    print("\n{:.^75}".format("\x1b[37;4mhttps://github.com/DiegoBloise\x1b[0m"))
    print("\x1b[1;32m")
    print("-="*32)
    print()
    print(f"{'WhatsApp-Bot - Send Message to Group Members':^64}")
    print()
    print("-="*32)
    print("\x1b[m")


def confirm_message(text):
    print("\x1b[1;33m")
    print("-="*32)
    print("\x1b[m")
    message(text="Are you sure you want to send\n    the following message?:\n", severity="error")
    print(text.replace("\\n", "\n"))
    print("\x1b[1;33m")
    print("-="*32)
    print("\x1b[m")


if __name__ == "__main__":
    banner()

    group_name = str(input("\nEnter the group name to search \x1b[1;32m~>>\x1b[m ")).lower()
    phones_to_exclude = str(input("\nEnter the 4 final numbers of all phones\nyou want to exclude separated by spaces\nEx: XXXX XXXX XXXX\n\x1b[1;32m~>>\x1b[m ")).split(" ")
    text = str(input("\nEnter text message (use \"\\n\" to write in another line)\nEx: First Line\\nSecond Line\n\x1b[1;32m~>>\x1b[m "))

    options = Options()
    options.add_argument("window-size=800,600")
    if not isDebug: options.add_argument("--headless")

    print("\x1b[1;32m")
    print("-="*32)
    print("\x1b[m")

    message(text="Starting WebDriver...")
    try:
        browser = webdriver.Firefox(options=options)
    except Exception as e:
        message(text=f"Could not start the WebDriver: {e}", severity='error')
        exit()

    message(text="Acessing WhatsAppWeb...")
    try:
        browser.get("https://web.whatsapp.com/")
    except Exception as e:
        message(text=f"Could not access WhatsAppWeb: {e}", severity='error')
        browser.quit()
        exit()

    wait = WebDriverWait(browser, 120)
    wait.until(EC.visibility_of_element_located((By.ID, initial_startup)))

    message(text="Loading QR Code...")
    wait.until(EC.visibility_of_element_located((By.XPATH, qr_code_xpath)))

    message(text="Scan the QR code to continue...", severity="success")
    browser.find_element(By.XPATH, qr_code_box_xpath).screenshot("qrcode.png")
    system("qrcode.png")

    wait.until(EC.invisibility_of_element_located((By.XPATH, qr_code_box_xpath)))
    system("del qrcode.png")
    window = pyautogui.getWindowsWithTitle("qrcode.png")[0]
    window.activate()
    pyautogui.hotkey('alt', 'f4')

    message(text="Loading...")
    wait.until(EC.visibility_of_element_located((By.ID, "pane-side")))

    message(text="Success...", severity="success")
    sleep(2)

    find_subject(browser, group_name)
    phones = get_phones(browser)

    message(text=f"Total of members: {len(phones)}")

    for phone in phones:
        print(phone)

    confirm_message(text)

    if input("\x1b[1m[Y/N] \x1b[1;32m~>> \x1b[m").lower() in 'y':
        print("\n\n")
        for i, phone in enumerate(phones):
            if phone[-4:] not in phones_to_exclude:
                message(text=f"Sending Message to {i+1}º : {phone}", severity="warn")
                send_text(browser, phone, text)
    else:
        message(text="Aborted by user.\n", severity="error")

    browser.quit()

    message(text="All done!", severity="success")
    system("pause")