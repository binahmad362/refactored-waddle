import pyautogui
import time
import subprocess
import requests
import os
import keyboard
import ctypes
import sys

# Function to check if script is running as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to disconnect RDP session
def disconnect_rdp():
    print("Attempting to disconnect RDP session...")
    try:
        # Get current username
        username = os.getenv('USERNAME')
        
        # Run query user command to get session ID
        result = subprocess.run(['query', 'user', username], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # Skip header line and process each session
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 3:
                        session_id = parts[2]
                        print(f"Found session ID: {session_id}")
                        
                        # Disconnect the session
                        disconnect_cmd = ['tscon', session_id, '/dest:console']
                        disconnect_result = subprocess.run(disconnect_cmd, capture_output=True, text=True)
                        
                        if disconnect_result.returncode == 0:
                            print(f"Successfully disconnected session {session_id}")
                            return True
                        else:
                            print(f"Failed to disconnect session {session_id}: {disconnect_result.stderr}")
            
            print("No active RDP sessions found for current user")
            return True
        else:
            print("Error querying user sessions:", result.stderr)
            return False
            
    except Exception as e:
        print(f"Error during RDP disconnection: {e}")
        return False

# Enable failsafe - move mouse to top-left corner to abort
pyautogui.FAILSAFE = False

def main():
    # Check if running as administrator
    if not is_admin():
        print("This script requires administrator privileges to disconnect RDP sessions.")
        print("Please run as Administrator.")
        # Re-run the script with admin rights
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        except Exception as e:
            print(f"Failed to elevate privileges: {e}")
            print("Continuing without RDP disconnection...")
    
    # Disconnect RDP session
    print("=== RDP DISCONNECTION PHASE ===")
    rdp_success = disconnect_rdp()
    
    if rdp_success:
        print("RDP disconnection completed successfully!")
    else:
        print("RDP disconnection failed, but continuing with automation...")
    
    # Wait a moment before starting main automation
    time.sleep(3)
    
    print("\n=== STARTING MAIN AUTOMATION ===")
    
    # Rest of your existing main function continues here...
    time.sleep(60)
    # Open MuMu_Installer.exe without blocking
    print("Opening MuMu_Installer.exe...")
    subprocess.Popen("MuMu_Installer.exe")

    # Wait 3 seconds for the installer to load
    print("Waiting 3 seconds for installer to load...")
    time.sleep(3)

    # Look for the install.png image on screen
    print("Searching for install.png on screen...")
    install_location = pyautogui.locateOnScreen('install.png', confidence=0.8)
    install_center = pyautogui.center(install_location)
    print(f"Found install.png at: {install_location}")
    print(f"Clicking at center: X: {install_center.x}, Y: {install_center.y}")
    pyautogui.click(install_center)
    print("Successfully clicked the install button!")

    # Wait for installation to complete
    print("Waiting for installation to complete...")
    time.sleep(70)

    # Click option.png
    print("Searching for option.png on screen...")
    option_location = pyautogui.locateOnScreen('option.png', confidence=0.8)
    option_center = pyautogui.center(option_location)
    print(f"Found option.png at: {option_location}")
    print(f"Clicking at center: X: {option_center.x}, Y: {option_center.y}")
    pyautogui.click(option_center)
    print("Successfully clicked option.png!")

    # Wait a moment for options to load
    time.sleep(5)

    # Click backup_restore.png
    print("Searching for backup_restore.png on screen...")
    backup_restore_location = pyautogui.locateOnScreen('backup_restore.png', confidence=0.8)
    backup_restore_center = pyautogui.center(backup_restore_location)
    print(f"Found backup_restore.png at: {backup_restore_location}")
    print(f"Clicking at center: X: {backup_restore_center.x}, Y: {backup_restore_center.y}")
    pyautogui.click(backup_restore_center)
    print("Successfully clicked backup_restore.png!")

    # Wait a moment for backup/restore options to load
    time.sleep(5)

    # Click restore.png
    print("Searching for restore.png on screen...")
    restore_location = pyautogui.locateOnScreen('restore.png', confidence=0.8)
    restore_center = pyautogui.center(restore_location)
    print(f"Found restore.png at: {restore_location}")
    print(f"Clicking at center: X: {restore_center.x}, Y: {restore_center.y}")
    pyautogui.click(restore_center)
    print("Successfully clicked restore.png!")

    # Wait for restore dialog to load
    time.sleep(5)

    # Click change_directory.png
    print("Searching for change_directory.png on screen...")
    change_directory_location = pyautogui.locateOnScreen('change_directory.png', confidence=0.8)
    change_directory_center = pyautogui.center(change_directory_location)
    print(f"Found change_directory.png at: {change_directory_location}")
    print(f"Clicking at center: X: {change_directory_center.x}, Y: {change_directory_center.y}")
    pyautogui.click(change_directory_center)
    print("Successfully clicked change_directory.png!")

    # Wait for directory dialog to load
    time.sleep(1)

    # Type the directory path and press Enter
    print("Typing directory path...")
    pyautogui.write(r'C:\Users\Rdpuser\Desktop\whatsapp')
    pyautogui.press('enter')
    print("Directory path entered successfully!")

    # Wait for directory to load
    time.sleep(5)

    # Double click on mumudata.png
    print("Searching for mumudata.png on screen...")
    mumudata_location = pyautogui.locateOnScreen('mumudata.png', confidence=0.8)
    mumudata_center = pyautogui.center(mumudata_location)
    print(f"Found mumudata.png at: {mumudata_location}")
    print(f"Double clicking at center: X: {mumudata_center.x}, Y: {mumudata_center.y}")
    pyautogui.doubleClick(mumudata_center)
    print("Successfully double clicked mumudata.png!")

    time.sleep(5)
    # Click start_emulator.png
    print("Searching for start_emulator.png on screen...")
    start_emulator = pyautogui.locateOnScreen('start_emulator.png', confidence=0.8)
    start_emulator_center = pyautogui.center(start_emulator)
    print(f"Found start_emulator.png at: {start_emulator}")
    print(f"Clicking at center: X: {start_emulator_center.x}, Y: {start_emulator_center.y}")
    pyautogui.click(start_emulator_center)
    print("Successfully clicked start_emulator.png!")

    # Wait 20 seconds for emulator to start
    print("Waiting 20 seconds for emulator to start...")
    time.sleep(60)

    # Rest of your WhatsApp automation code...
    whatsapp_icon = pyautogui.locateOnScreen('whatsapp_icon.png', confidence=0.8)
    whatsapp_icon = pyautogui.center(whatsapp_icon)
    print(f"Found whatsapp_icon.png at: {whatsapp_icon}")
    print(f"Clicking at center: X: {whatsapp_icon.x}, Y: {whatsapp_icon.y}")
    pyautogui.click(whatsapp_icon)
    print("Successfully clicked whatsapp_icon.png!")

    time.sleep(5)

    print("Searching for first_agree.png on screen...")
    first_agree = pyautogui.locateOnScreen('first_agree.png', confidence=0.8)
    first_agree = pyautogui.center(first_agree)
    print(f"Found start_emulator.png at: {first_agree}")
    print(f"Clicking at center: X: {first_agree.x}, Y: {first_agree.y}")
    pyautogui.click(first_agree)
    print("Successfully clicked first_agree.png!")

    time.sleep(5)

    print("Setting up number verification...")
    if not download_numbers_file():
        return
    
    country_name, country_code, numbers = read_numbers_file()
    
    if not country_name or not country_code or not numbers:
        print("Failed to get valid data from numbers file")
        return
    
    print(f"\nStarting automation for {len(numbers)} numbers...")
    print("Make sure WhatsApp is ready for number input!")
    
    # Wait a moment for user to prepare
    time.sleep(2)
    
    # Start processing numbers
    process_numbers(country_name, country_code, numbers)
    
    print("\nAutomation completed! Check not_usable.txt for unusable numbers.")

# Your existing functions (download_numbers_file, read_numbers_file, etc.) remain the same below...
def download_numbers_file():
    url = "https://raw.githubusercontent.com/binahmad362/bookish-octo-couscous/main/rough.txt"
    try:
        print("Downloading numbers file...")
        response = requests.get(url)
        response.raise_for_status()
        
        with open("rough.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Numbers file downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading numbers file: {e}")
        return False

def read_numbers_file():
    try:
        with open("rough.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if len(lines) < 3:
            print("Error: File doesn't contain enough data")
            return None, None, []
        
        country_name = lines[0]
        country_code = lines[1]
        numbers = lines[2:]
        
        print(f"Country: {country_name}")
        print(f"Country code: {country_code}")
        print(f"Numbers to check: {len(numbers)}")
        
        return country_name, country_code, numbers
    except Exception as e:
        print(f"Error reading numbers file: {e}")
        return None, None, []

def save_not_usable_number(number):
    try:
        with open("not_usable.txt", "a", encoding="utf-8") as f:
            f.write(number + "\n")
        print(f"Saved {number} to not_usable.txt")
    except Exception as e:
        print(f"Error saving to not_usable.txt: {e}")

def save_request_review_number(number):
    try:
        with open("request_review.txt", "a", encoding="utf-8") as f:
            f.write(number + "\n")
        print(f"Saved {number} to request_review.txt")
    except Exception as e:
        print(f"Error saving to request_review.txt: {e}")

def type_with_delay(text, delay=0.1):
    """Type text with specified delay between characters"""
    pyautogui.write(text, interval=delay)

def wait_and_click(image, timeout=10, confidence=0.8):
    """Wait for an image to appear and click it - QUICK VERSION"""
    print(f"Searching for {image} on screen...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"Found {image} at: {location}")
                print(f"Clicking at center: X: {center.x}, Y: {center.y}")
                pyautogui.click(center)
                print(f"Successfully clicked {image}!")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.1)  # Small sleep to prevent CPU overload
    
    print(f"❌ {image} not found on screen within {timeout} seconds")
    return False

def wait_for_image(image, timeout=10, confidence=0.8):
    """Wait for an image to appear without clicking it - QUICK VERSION"""
    print(f"Searching for {image} on screen...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location:
                print(f"Found {image} at: {location}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.1)  # Small sleep to prevent CPU overload
    
    print(f"❌ {image} not found on screen within {timeout} seconds")
    return False

def check_too_long_phone_number():
    """Check if too_long_phone_number.png is on screen and handle it - QUICK VERSION"""
    if wait_for_image('too_long_phone_number.png', timeout=2):
        print("⚠️ Too long phone number detected! Handling the error...")
        
        # Click ok.png
        if wait_and_click('ok.png', timeout=5):
            print("Clicked ok.png to dismiss the error")
            time.sleep(1)
            
            # Press backspace 50 times to clear everything
            print("Clearing phone number field with 50 backspaces...")
            for _ in range(50):
                keyboard.press_and_release('backspace')
            time.sleep(1)
            
            print("Phone number field cleared successfully")
            return True
        else:
            print("Failed to find ok.png")
            return False
    return False

def process_numbers(country_name, country_code, numbers):
    """Process all numbers through the WhatsApp verification flow - OPTIMIZED"""
    
    # Check for too_long_phone_number.png before starting
    if check_too_long_phone_number():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click select_country.png
    if not wait_and_click('select_country.png', timeout=10):
        print("Failed to find select_country.png. Aborting.")
        return
    
    time.sleep(2)
    
    # Check for too_long_phone_number.png after clicking select_country
    if check_too_long_phone_number():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click search_the_country.png
    if not wait_and_click('search_the_country.png', timeout=10):
        print("Failed to find search_the_country.png. Aborting.")
        return
    
    time.sleep(1)
    
    # Check for too_long_phone_number.png after clicking search_the_country
    if check_too_long_phone_number():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Type country name
    print(f"Typing country: {country_name}")
    type_with_delay(country_name)
    time.sleep(1)
    
    # Check for too_long_phone_number.png after typing country name
    if check_too_long_phone_number():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click confirm_the_country.png
    if not wait_and_click('confirm_the_country.png', timeout=10):
        print("Failed to find confirm_the_country.png. Aborting.")
        return
    
    time.sleep(2)
    
    # Check for too_long_phone_number.png after clicking confirm_the_country
    if check_too_long_phone_number():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Process each number
    for i, full_number in enumerate(numbers):
        print(f"\n--- Processing number {i+1}/{len(numbers)}: {full_number} ---")
        
        # Check for too_long_phone_number.png before processing each number
        if check_too_long_phone_number():
            print("Recovered from too_long_phone_number error, continuing with current number...")
        
        # Remove country code from the number
        if full_number.startswith(country_code):
            number_without_code = full_number[len(country_code):]
        else:
            number_without_code = full_number
            print(f"Warning: Number doesn't start with country code {country_code}")
        
        print(f"Typing number without country code: {number_without_code}")
        
        # Type the number without country code
        type_with_delay(number_without_code)
        time.sleep(0.5)
        
        # Check for too_long_phone_number.png after typing number
        if check_too_long_phone_number():
            print("Recovered from too_long_phone_number error, re-typing current number...")
            # Re-type the number since it was cleared
            type_with_delay(number_without_code)
            time.sleep(0.5)
        
        # Click next.png
        if not wait_and_click('next.png', timeout=10):
            print("Failed to find next.png. Moving to next number.")
            continue
        
        # Check for too_long_phone_number.png after clicking next
        if check_too_long_phone_number():
            print("Recovered from too_long_phone_number error, continuing to next number...")
            continue
        
        # Wait for result (edit.png or not_usable.png) - QUICK VERSION
        print("Waiting for result (edit.png or not_usable.png)...")
        result_found = False
        start_time = time.time()
        
        while time.time() - start_time < 8 and not result_found:
            # Check for edit.png
            if wait_for_image('edit.png', timeout=0.5):
                print("Edit button found - number might be valid but needs modification")
                # Click edit.png to clear field
                wait_and_click('edit.png', timeout=2)
                # Clear the field with backspaces
                for _ in range(20):
                    keyboard.press_and_release('backspace')
                time.sleep(1)
                result_found = True
                break
            
            # Check for not_usable.png
            if wait_for_image('not_usable.png', timeout=0.5):
                print("Number is not usable - saving to file")
                save_not_usable_number(full_number)
                # Click not_usable.png
                wait_and_click('not_usable.png', timeout=2)
                result_found = True
                break
            
            time.sleep(0.1)
        
        if not result_found:
            print("Neither edit.png nor not_usable.png found - unexpected state")
            # Try to go back or reset state
            pyautogui.press('esc')
            time.sleep(2)
            
            # Check for too_long_phone_number.png after pressing escape
            if check_too_long_phone_number():
                print("Recovered from too_long_phone_number error, continuing to next number...")
                continue
            
            # Check if we're back at number entry screen
            if wait_and_click('register_new_number.png', timeout=5):
                print("Back at registration screen, continuing...")
            else:
                print("Could not recover to registration screen")
                continue
            continue
        
        # Handle registration flow after not_usable
        if wait_for_image('not_usable.png', timeout=1):
            # Check for register_new_number.png first
            if wait_and_click('register_new_number.png', timeout=8):
                # Check for too_long_phone_number.png after clicking register_new_number
                if check_too_long_phone_number():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                # Click agree.png if needed
                wait_and_click('agree_2.png', timeout=5)
                
                # Check for too_long_phone_number.png after clicking agree_2
                if check_too_long_phone_number():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                # Wait before processing next number
                time.sleep(2)
            else:
                # If register_new_number.png is not found, check for request_review.png
                print("Failed to find register_new_number.png, checking for request_review.png...")
                
                # Check for too_long_phone_number.png before checking request_review
                if check_too_long_phone_number():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                if wait_for_image('request_review.png', timeout=5):
                    print("Found request_review.png - saving number to request_review.txt")
                    save_request_review_number(full_number)
                    
                    # Click show_option.png
                    if wait_and_click('show_option.png', timeout=8):
                        # Check for too_long_phone_number.png after clicking show_option
                        if check_too_long_phone_number():
                            print("Recovered from too_long_phone_number error, continuing to next number...")
                            continue
                        
                        time.sleep(1)
                        
                        # Click register_new_number_after_it_is_review.png
                        if wait_and_click('register_new_number_after_it_is_review.png', timeout=8):
                            # Check for too_long_phone_number.png after clicking register_new_number_after_it_is_review
                            if check_too_long_phone_number():
                                print("Recovered from too_long_phone_number error, continuing to next number...")
                                continue
                            
                            time.sleep(1)
                            
                            # Click agree_2.png
                            if wait_and_click('agree_2.png', timeout=8):
                                # Check for too_long_phone_number.png after clicking agree_2
                                if check_too_long_phone_number():
                                    print("Recovered from too_long_phone_number error, continuing to next number...")
                                    continue
                                
                                print("Successfully navigated through request review flow")
                                time.sleep(2)
                            else:
                                print("Failed to find agree_2.png after request review")
                        else:
                            print("Failed to find register_new_number_after_it_is_review.png")
                    else:
                        print("Failed to find show_option.png")
                else:
                    print("Neither register_new_number.png nor request_review.png found")

if __name__ == "__main__":
    main()
