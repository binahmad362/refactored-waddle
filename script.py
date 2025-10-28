import pyautogui
import time
import subprocess
import requests
import os
import keyboard
import ctypes
import sys
import cv2
import numpy as np

# Function to check if script is running as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to run the existing rdp.bat file
def run_rdp_bat():
    print("Looking for rdp.bat in current directory...")
    
    # Check if rdp.bat exists in current directory
    if not os.path.exists('rdp.bat'):
        print("❌ rdp.bat not found in current directory!")
        print("Please make sure rdp.bat exists in the same folder as this script.")
        return False
    
    try:
        print("✅ Found rdp.bat, executing it...")
        # Run the batch file and wait for completion
        result = subprocess.run(['rdp.bat'], capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            print("✅ rdp.bat executed successfully!")
            print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ rdp.bat execution failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error executing rdp.bat: {e}")
        return False

# Enhanced image detection function with scaling support
def find_image_advanced(image_path, confidence=0.8, scales=None, timeout=10):
    """
    Enhanced image detection with scaling support and multiple attempts
    """
    if scales is None:
        scales = [0.5, 0.75, 1.0, 1.25, 1.5]
    
    print(f"Advanced search for {image_path} with scales {scales}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Take a screenshot of the entire screen
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Load template
            template = cv2.imread(image_path, 0)
            if template is None:
                print(f"Warning: Could not load template {image_path}")
                time.sleep(0.1)
                continue
                
            tw, th = template.shape[::-1]
            best_match = None
            best_val = 0

            for scale in scales:
                try:
                    resized_template = cv2.resize(template, (int(tw * scale), int(th * scale)))
                    res = cv2.matchTemplate(gray_screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    
                    if max_val > best_val:
                        best_val = max_val
                        best_match = (max_loc, resized_template.shape[::-1])
                except Exception as e:
                    continue

            if best_match and best_val >= confidence:
                top_left = best_match[0]
                tw, th = best_match[1]
                center_x = top_left[0] + tw // 2
                center_y = top_left[1] + th // 2
                location = (top_left[0], top_left[1], tw, th)
                print(f"✅ Found {image_path} at: {location} with confidence {best_val:.2f}")
                return location, (center_x, center_y), best_val
                
        except Exception as e:
            print(f"Error during image detection: {e}")
            
        time.sleep(0.1)
    
    print(f"❌ {image_path} not found on screen within {timeout} seconds")
    return None, None, 0

# Enhanced click function with scaling support
def click_image_advanced(image_path, confidence=0.8, scales=None, timeout=10):
    """
    Find and click an image with scaling support
    """
    location, center, confidence_val = find_image_advanced(image_path, confidence, scales, timeout)
    if location and center:
        print(f"Clicking at center: X: {center[0]}, Y: {center[1]}")
        pyautogui.click(center[0], center[1])
        print(f"✅ Successfully clicked {image_path}!")
        return True
    return False

# Enhanced wait for image function with scaling support
def wait_for_image_advanced(image_path, confidence=0.8, scales=None, timeout=10):
    """
    Wait for an image to appear with scaling support
    """
    location, center, confidence_val = find_image_advanced(image_path, confidence, scales, timeout)
    return location is not None

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
    
    # Run rdp.bat file
    print("=== RDP DISCONNECTION PHASE ===")
    rdp_success = run_rdp_bat()
    
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

    # Look for the install.png image on screen with scaling support
    print("Searching for install.png on screen...")
    if click_image_advanced('install.png', confidence=0.8, timeout=30):
        print("Successfully clicked the install button!")
    else:
        print("Failed to find install button!")
        return

    # Wait for installation to complete
    print("Waiting for installation to complete...")
    time.sleep(70)

    # Click option.png with scaling support
    if click_image_advanced('option.png', confidence=0.8, timeout=30):
        print("Successfully clicked option.png!")
    else:
        print("Failed to find option.png!")
        return

    # Wait a moment for options to load
    time.sleep(5)

    # Click backup_restore.png with scaling support
    if click_image_advanced('backup_restore.png', confidence=0.8, timeout=30):
        print("Successfully clicked backup_restore.png!")
    else:
        print("Failed to find backup_restore.png!")
        return

    # Wait a moment for backup/restore options to load
    time.sleep(5)

    # Click restore.png with scaling support
    if click_image_advanced('restore.png', confidence=0.8, timeout=30):
        print("Successfully clicked restore.png!")
    else:
        print("Failed to find restore.png!")
        return

    # Wait for restore dialog to load
    time.sleep(5)

    # Click change_directory.png with scaling support
    if click_image_advanced('change_directory.png', confidence=0.8, timeout=30):
        print("Successfully clicked change_directory.png!")
    else:
        print("Failed to find change_directory.png!")
        return

    # Wait for directory dialog to load
    time.sleep(1)

    # Type the directory path and press Enter
    print("Typing directory path...")
    pyautogui.write(r'C:\Users\Rdpuser\Desktop\whatsapp')
    pyautogui.press('enter')
    print("Directory path entered successfully!")

    # Wait for directory to load
    time.sleep(5)

    # Double click on mumudata.png with scaling support
    print("Searching for mumudata.png on screen...")
    location, center, confidence_val = find_image_advanced('mumudata.png', confidence=0.8, timeout=30)
    if location and center:
        print(f"Double clicking at center: X: {center[0]}, Y: {center[1]}")
        pyautogui.doubleClick(center[0], center[1])
        print("Successfully double clicked mumudata.png!")
    else:
        print("Failed to find mumudata.png!")
        return

    time.sleep(5)
    
    # Click start_emulator.png with scaling support
    if click_image_advanced('start_emulator.png', confidence=0.8, timeout=30):
        print("Successfully clicked start_emulator.png!")
    else:
        print("Failed to find start_emulator.png!")
        return

    # Wait 20 seconds for emulator to start
    print("Waiting 150 seconds for emulator to start...")
    time.sleep(150)

    # Rest of your WhatsApp automation code with enhanced image detection...
    if click_image_advanced('whatsapp_icon.png', confidence=0.8, timeout=30):
        print("Successfully clicked whatsapp_icon.png!")
    else:
        print("Failed to find whatsapp_icon.png!")
        return

    time.sleep(5)

    if click_image_advanced('first_agree.png', confidence=0.8, timeout=30):
        print("Successfully clicked first_agree.png!")
    else:
        print("Failed to find first_agree.png!")
        return

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
    process_numbers_enhanced(country_name, country_code, numbers)
    
    print("\nAutomation completed! Check not_usable.txt for unusable numbers.")

# Your existing functions remain the same...
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

def check_too_long_phone_number_enhanced():
    """Check if too_long_phone_number.png is on screen and handle it - ENHANCED VERSION"""
    if wait_for_image_advanced('too_long_phone_number.png', confidence=0.8, timeout=2):
        print("⚠️ Too long phone number detected! Handling the error...")
        
        # Click ok.png
        if click_image_advanced('ok.png', confidence=0.8, timeout=5):
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

def process_numbers_enhanced(country_name, country_code, numbers):
    """Process all numbers through the WhatsApp verification flow - ENHANCED VERSION"""
    
    # Check for too_long_phone_number.png before starting
    if check_too_long_phone_number_enhanced():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click select_country.png with enhanced detection
    if not click_image_advanced('select_country.png', confidence=0.8, timeout=10):
        print("Failed to find select_country.png. Aborting.")
        return
    
    time.sleep(2)
    
    # Check for too_long_phone_number.png after clicking select_country
    if check_too_long_phone_number_enhanced():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click search_the_country.png with enhanced detection
    if not click_image_advanced('search_the_country.png', confidence=0.8, timeout=10):
        print("Failed to find search_the_country.png. Aborting.")
        return
    
    time.sleep(1)
    
    # Check for too_long_phone_number.png after clicking search_the_country
    if check_too_long_phone_number_enhanced():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Type country name
    print(f"Typing country: {country_name}")
    type_with_delay(country_name)
    time.sleep(1)
    
    # Check for too_long_phone_number.png after typing country name
    if check_too_long_phone_number_enhanced():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Click confirm_the_country.png with enhanced detection
    if not click_image_advanced('confirm_the_country.png', confidence=0.8, timeout=10):
        print("Failed to find confirm_the_country.png. Aborting.")
        return
    
    time.sleep(2)
    
    # Check for too_long_phone_number.png after clicking confirm_the_country
    if check_too_long_phone_number_enhanced():
        print("Recovered from too_long_phone_number error, continuing...")
    
    # Process each number
    for i, full_number in enumerate(numbers):
        print(f"\n--- Processing number {i+1}/{len(numbers)}: {full_number} ---")
        
        # Check for too_long_phone_number.png before processing each number
        if check_too_long_phone_number_enhanced():
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
        if check_too_long_phone_number_enhanced():
            print("Recovered from too_long_phone_number error, re-typing current number...")
            # Re-type the number since it was cleared
            type_with_delay(number_without_code)
            time.sleep(0.5)
        
        # Click next.png with enhanced detection
        if not click_image_advanced('next.png', confidence=0.8, timeout=10):
            print("Failed to find next.png. Moving to next number.")
            continue
        
        # Check for too_long_phone_number.png after clicking next
        if check_too_long_phone_number_enhanced():
            print("Recovered from too_long_phone_number error, continuing to next number...")
            continue
        
        # Wait for result (edit.png or not_usable.png) - ENHANCED VERSION
        print("Waiting for result (edit.png or not_usable.png)...")
        result_found = False
        start_time = time.time()
        
        while time.time() - start_time < 8 and not result_found:
            # Check for edit.png with enhanced detection
            if wait_for_image_advanced('edit.png', confidence=0.8, timeout=0.5):
                print("Edit button found - number might be valid but needs modification")
                # Click edit.png to clear field
                click_image_advanced('edit.png', confidence=0.8, timeout=2)
                # Clear the field with backspaces
                for _ in range(20):
                    keyboard.press_and_release('backspace')
                time.sleep(1)
                result_found = True
                break
            
            # Check for not_usable.png with enhanced detection
            if wait_for_image_advanced('not_usable.png', confidence=0.8, timeout=0.5):
                print("Number is not usable - saving to file")
                save_not_usable_number(full_number)
                # Click not_usable.png
                click_image_advanced('not_usable.png', confidence=0.8, timeout=2)
                result_found = True
                break
            
            time.sleep(0.1)
        
        if not result_found:
            print("Neither edit.png nor not_usable.png found - unexpected state")
            # Try to go back or reset state
            pyautogui.press('esc')
            time.sleep(2)
            
            # Check for too_long_phone_number.png after pressing escape
            if check_too_long_phone_number_enhanced():
                print("Recovered from too_long_phone_number error, continuing to next number...")
                continue
            
            # Check if we're back at number entry screen
            if click_image_advanced('register_new_number.png', confidence=0.8, timeout=5):
                print("Back at registration screen, continuing...")
            else:
                print("Could not recover to registration screen")
                continue
            continue
        
        # Handle registration flow after not_usable with enhanced detection
        if wait_for_image_advanced('not_usable.png', confidence=0.8, timeout=1):
            # Check for register_new_number.png first
            if click_image_advanced('register_new_number.png', confidence=0.8, timeout=8):
                # Check for too_long_phone_number.png after clicking register_new_number
                if check_too_long_phone_number_enhanced():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                # Click agree.png if needed
                click_image_advanced('agree_2.png', confidence=0.8, timeout=5)
                
                # Check for too_long_phone_number.png after clicking agree_2
                if check_too_long_phone_number_enhanced():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                # Wait before processing next number
                time.sleep(2)
            else:
                # If register_new_number.png is not found, check for request_review.png
                print("Failed to find register_new_number.png, checking for request_review.png...")
                
                # Check for too_long_phone_number.png before checking request_review
                if check_too_long_phone_number_enhanced():
                    print("Recovered from too_long_phone_number error, continuing to next number...")
                    continue
                
                if wait_for_image_advanced('request_review.png', confidence=0.8, timeout=5):
                    print("Found request_review.png - saving number to request_review.txt")
                    save_request_review_number(full_number)
                    
                    # Click show_option.png
                    if click_image_advanced('show_option.png', confidence=0.8, timeout=8):
                        # Check for too_long_phone_number.png after clicking show_option
                        if check_too_long_phone_number_enhanced():
                            print("Recovered from too_long_phone_number error, continuing to next number...")
                            continue
                        
                        time.sleep(1)
                        
                        # Click register_new_number_after_it_is_review.png
                        if click_image_advanced('register_new_number_after_it_is_review.png', confidence=0.8, timeout=8):
                            # Check for too_long_phone_number.png after clicking register_new_number_after_it_is_review
                            if check_too_long_phone_number_enhanced():
                                print("Recovered from too_long_phone_number error, continuing to next number...")
                                continue
                            
                            time.sleep(1)
                            
                            # Click agree_2.png
                            if click_image_advanced('agree_2.png', confidence=0.8, timeout=8):
                                # Check for too_long_phone_number.png after clicking agree_2
                                if check_too_long_phone_number_enhanced():
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
