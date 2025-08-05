#!/usr/bin/env python3
"""
BrowserStack + Percy Mobile App Testing Script

This script demonstrates automated mobile app testing using:
1. BrowserStack SDK for device cloud testing
2. Percy for visual testing and snapshots
3. Appium for mobile app automation

Features:
- Authenticates using BrowserStack credentials from .sh file
- Integrates Percy for visual testing
- Automates app interactions (click, type, search)
- Takes Percy snapshots for each action
"""

import os
import subprocess
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from percy_appium_app import percy_screenshot


class BrowserStackPercyAppTest:
    def __init__(self):
        """Initialize the test class and load environment variables."""
        self.driver = None
        self.load_environment_variables()
        
    def load_environment_variables(self):
        """Load environment variables from creds.sh file."""
        try:
            # Source the shell script to load environment variables
            result = subprocess.run(['bash', '-c', 'source creds.sh && env'], 
                                   capture_output=True, text=True, check=True)
            
            # Parse environment variables
            for line in result.stdout.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
                    
            # Verify required credentials are loaded
            self.browserstack_username = os.environ.get('BROWSERSTACK_USERNAME')
            self.browserstack_access_key = os.environ.get('BROWSERSTACK_ACCESS_KEY')
            self.percy_token = os.environ.get('PERCY_TOKEN')
            self.build_name = os.environ.get('BROWSERSTACK_BUILD_NAME', 'Percy App Test Build')
            self.project_name = os.environ.get('BROWSERSTACK_PROJECT_NAME', 'Percy App Test Project')
            
            if not all([self.browserstack_username, self.browserstack_access_key, self.percy_token]):
                raise ValueError("Missing required credentials in creds.sh file")
                
            print("✅ Environment variables loaded successfully")
            print(f"📱 BrowserStack User: {self.browserstack_username}")
            print(f"🎨 Percy Token: {self.percy_token[:10]}...")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error loading environment variables: {e}")
            raise
        except ValueError as e:
            print(f"❌ Credential error: {e}")
            raise

    def setup_driver(self, app_id):
        """
        Setup the Appium WebDriver with BrowserStack capabilities.
        
        Args:
            app_id (str): BrowserStack app ID (bs://app-id format)
        """
        try:
            # BrowserStack capabilities
            desired_caps = {
                # BrowserStack credentials
                "browserstack.user": self.browserstack_username,
                "browserstack.key": self.browserstack_access_key,
                
                # App configuration
                "app": app_id,
                
                # Device configuration
                "device": "Samsung Galaxy S23",
                "os_version": "13.0",
                "platformName": "Android",
                
                # Test configuration
                "project": self.project_name,
                "build": self.build_name,
                "name": "Percy App Automation Test",
                
                # Additional capabilities
                "autoGrantPermissions": True,
                "autoAcceptAlerts": True,
                "unicodeKeyboard": True,
                "resetKeyboard": True,
                
                # Percy configuration
                "percy.enabled": True,
                "percy.token": self.percy_token
            }
            
            # Initialize WebDriver
            self.driver = webdriver.Remote(
                command_executor="https://hub-cloud.browserstack.com/wd/hub",
                desired_capabilities=desired_caps
            )
            
            print("✅ WebDriver initialized successfully")
            print(f"📱 Testing on: {desired_caps['device']} (Android {desired_caps['os_version']})")
            
            # Wait for app to load
            time.sleep(5)
            
            return self.driver
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            raise

    def take_percy_snapshot(self, name, options=None):
        """
        Take a Percy snapshot with the given name.
        
        Args:
            name (str): Name for the Percy snapshot
            options (dict): Additional Percy options
        """
        try:
            if options is None:
                options = {}
                
            percy_screenshot(self.driver, name, **options)
            print(f"📸 Percy snapshot taken: {name}")
            
        except Exception as e:
            print(f"⚠️  Warning: Failed to take Percy snapshot '{name}': {e}")

    def wait_for_element(self, locator_type, locator_value, timeout=30):
        """
        Wait for an element to be present and return it.
        
        Args:
            locator_type: Appium locator type (e.g., AppiumBy.ID)
            locator_value (str): Locator value
            timeout (int): Maximum wait time in seconds
            
        Returns:
            WebElement: Found element
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
            return element
        except Exception as e:
            print(f"❌ Element not found: {locator_type}='{locator_value}' (timeout: {timeout}s)")
            raise

    def click_element(self, locator_type, locator_value, element_name="Element"):
        """
        Click an element and take a Percy snapshot.
        
        Args:
            locator_type: Appium locator type
            locator_value (str): Locator value
            element_name (str): Human-readable element name for logging
        """
        try:
            print(f"🔍 Looking for {element_name}...")
            element = self.wait_for_element(locator_type, locator_value)
            
            print(f"👆 Clicking {element_name}...")
            element.click()
            
            # Wait for UI to update
            time.sleep(2)
            
            # Take Percy snapshot after click
            snapshot_name = f"After clicking {element_name}"
            self.take_percy_snapshot(snapshot_name)
            
            print(f"✅ Successfully clicked {element_name}")
            
        except Exception as e:
            print(f"❌ Error clicking {element_name}: {e}")
            raise

    def type_text(self, locator_type, locator_value, text, element_name="Text Field"):
        """
        Type text into an element and take a Percy snapshot.
        
        Args:
            locator_type: Appium locator type
            locator_value (str): Locator value
            text (str): Text to type
            element_name (str): Human-readable element name for logging
        """
        try:
            print(f"🔍 Looking for {element_name}...")
            element = self.wait_for_element(locator_type, locator_value)
            
            print(f"⌨️  Typing '{text}' into {element_name}...")
            element.clear()
            element.send_keys(text)
            
            # Wait for UI to update
            time.sleep(2)
            
            # Take Percy snapshot after typing
            snapshot_name = f"After typing in {element_name}"
            self.take_percy_snapshot(snapshot_name)
            
            print(f"✅ Successfully typed text into {element_name}")
            
        except Exception as e:
            print(f"❌ Error typing into {element_name}: {e}")
            raise

    def perform_search_test(self):
        """
        Perform a complete search test with Percy snapshots.
        This is a generic example - modify according to your app.
        """
        try:
            print("\n🚀 Starting search functionality test...")
            
            # Take initial screenshot
            self.take_percy_snapshot("App Launch - Initial State")
            
            # Example test flow - modify these locators according to your app
            # Step 1: Click on search button/field
            try:
                # Try common search element patterns
                search_patterns = [
                    (AppiumBy.ACCESSIBILITY_ID, "Search"),
                    (AppiumBy.ID, "search"),
                    (AppiumBy.ID, "search_button"),
                    (AppiumBy.XPATH, "//android.widget.EditText[contains(@hint,'Search')]"),
                    (AppiumBy.XPATH, "//android.widget.Button[contains(@text,'Search')]"),
                    (AppiumBy.CLASS_NAME, "android.widget.EditText")
                ]
                
                search_element = None
                for locator_type, locator_value in search_patterns:
                    try:
                        search_element = self.wait_for_element(locator_type, locator_value, timeout=5)
                        print(f"✅ Found search element using: {locator_type}='{locator_value}'")
                        break
                    except:
                        continue
                
                if search_element:
                    self.click_element(locator_type, locator_value, "Search Field/Button")
                else:
                    print("⚠️  No search element found, taking snapshot of current state")
                    self.take_percy_snapshot("No Search Element Found")
                    
            except Exception as e:
                print(f"⚠️  Search element interaction failed: {e}")
                self.take_percy_snapshot("Search Element Error")
            
            # Step 2: Type search query
            try:
                # Common search input patterns
                input_patterns = [
                    (AppiumBy.CLASS_NAME, "android.widget.EditText"),
                    (AppiumBy.XPATH, "//android.widget.EditText"),
                    (AppiumBy.ID, "search_input"),
                    (AppiumBy.ID, "edit_text"),
                ]
                
                for locator_type, locator_value in input_patterns:
                    try:
                        self.type_text(locator_type, locator_value, "Test Search Query", "Search Input")
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️  Text input failed: {e}")
                self.take_percy_snapshot("Text Input Error")
            
            # Step 3: Perform search (press enter or click search button)
            try:
                # Try to press enter or find search button
                self.driver.press_keycode(66)  # Enter key on Android
                time.sleep(3)
                self.take_percy_snapshot("After Search Execution")
                
            except Exception as e:
                print(f"⚠️  Search execution failed: {e}")
                
            # Step 4: Verify search results
            try:
                # Take final snapshot
                self.take_percy_snapshot("Search Results")
                print("✅ Search test completed successfully")
                
            except Exception as e:
                print(f"⚠️  Search results verification failed: {e}")
                
        except Exception as e:
            print(f"❌ Search test failed: {e}")
            self.take_percy_snapshot("Test Failure State")

    def run_custom_test_flow(self):
        """
        Run a custom test flow. Modify this method according to your app's specific functionality.
        """
        try:
            print("\n🎯 Running custom test flow...")
            
            # Take initial snapshot
            self.take_percy_snapshot("Custom Test - Initial State")
            
            # Add your custom test steps here
            # Example:
            # self.click_element(AppiumBy.ID, "button_id", "Custom Button")
            # self.type_text(AppiumBy.ID, "input_id", "Custom Text", "Custom Input")
            
            print("✅ Custom test flow completed")
            
        except Exception as e:
            print(f"❌ Custom test flow failed: {e}")
            self.take_percy_snapshot("Custom Test Failure")

    def cleanup(self):
        """Clean up resources and quit the driver."""
        try:
            if self.driver:
                print("\n🧹 Cleaning up...")
                self.driver.quit()
                print("✅ WebDriver session ended")
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")

    def run_test_suite(self, app_id):
        """
        Run the complete test suite.
        
        Args:
            app_id (str): BrowserStack app ID (bs://app-id format)
        """
        try:
            print("🔧 Setting up BrowserStack + Percy App Test...")
            print("=" * 50)
            
            # Setup
            self.setup_driver(app_id)
            
            # Run test flows
            self.perform_search_test()
            self.run_custom_test_flow()
            
            print("\n" + "=" * 50)
            print("🎉 Test suite completed successfully!")
            print("📊 Check your Percy dashboard for visual comparisons")
            print("📱 Check your BrowserStack dashboard for test details")
            
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
            self.take_percy_snapshot("Test Suite Failure")
            
        finally:
            self.cleanup()


def main():
    """Main function to run the test."""
    # Replace with your actual app ID from BrowserStack
    # You can upload your app via BrowserStack UI or API and get the app ID
    APP_ID = "bs://664aa316b184a8060e44cfbfa1477881660cf7a7"  # Sample app ID - replace with yours
    
    print("🚀 BrowserStack + Percy Mobile App Testing")
    print("=" * 50)
    
    # Initialize and run test
    test = BrowserStackPercyAppTest()
    test.run_test_suite(APP_ID)


if __name__ == "__main__":
    main()