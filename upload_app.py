#!/usr/bin/env python3
"""
BrowserStack App Upload Utility

This script helps upload mobile apps to BrowserStack and returns the app ID
that can be used for testing.
"""

import os
import subprocess
import requests
import json
import sys


class BrowserStackAppUploader:
    def __init__(self):
        """Initialize the uploader and load credentials."""
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
                    
            # Get credentials
            self.username = os.environ.get('BROWSERSTACK_USERNAME')
            self.access_key = os.environ.get('BROWSERSTACK_ACCESS_KEY')
            
            if not all([self.username, self.access_key]):
                raise ValueError("Missing BrowserStack credentials in creds.sh file")
                
            print("✅ BrowserStack credentials loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            raise

    def upload_app(self, app_path, custom_id=None):
        """
        Upload an app to BrowserStack.
        
        Args:
            app_path (str): Path to the app file (.apk, .ipa, etc.)
            custom_id (str): Optional custom ID for the app
            
        Returns:
            str: App URL/ID that can be used for testing
        """
        try:
            print(f"📱 Uploading app: {app_path}")
            
            # Check if file exists
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"App file not found: {app_path}")
            
            # Prepare upload URL
            url = "https://api-cloud.browserstack.com/app-automate/upload"
            
            # Prepare files and data
            files = {'file': open(app_path, 'rb')}
            data = {}
            
            if custom_id:
                data['custom_id'] = custom_id
            
            # Make request
            response = requests.post(
                url,
                files=files,
                data=data,
                auth=(self.username, self.access_key)
            )
            
            # Close file
            files['file'].close()
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                app_url = result.get('app_url')
                
                print("✅ App uploaded successfully!")
                print(f"📱 App URL: {app_url}")
                print(f"📱 App Name: {result.get('app_name', 'N/A')}")
                print(f"📱 App Version: {result.get('app_version', 'N/A')}")
                
                if custom_id:
                    print(f"🏷️  Custom ID: {custom_id}")
                
                return app_url
                
            else:
                print(f"❌ Upload failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error uploading app: {e}")
            return None

    def list_uploaded_apps(self):
        """List all uploaded apps in BrowserStack."""
        try:
            print("📋 Fetching uploaded apps...")
            
            url = "https://api-cloud.browserstack.com/app-automate/recent_apps"
            
            response = requests.get(url, auth=(self.username, self.access_key))
            
            if response.status_code == 200:
                apps = response.json()
                
                if apps:
                    print("✅ Uploaded apps:")
                    print("-" * 50)
                    
                    for app in apps:
                        print(f"📱 App Name: {app.get('app_name', 'N/A')}")
                        print(f"🆔 App URL: {app.get('app_url', 'N/A')}")
                        print(f"📅 Upload Time: {app.get('uploaded_at', 'N/A')}")
                        print(f"📊 App Version: {app.get('app_version', 'N/A')}")
                        print("-" * 50)
                else:
                    print("📭 No apps found")
                    
            else:
                print(f"❌ Failed to fetch apps: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error fetching apps: {e}")

    def delete_app(self, app_id):
        """
        Delete an app from BrowserStack.
        
        Args:
            app_id (str): App ID to delete
        """
        try:
            print(f"🗑️  Deleting app: {app_id}")
            
            url = f"https://api-cloud.browserstack.com/app-automate/app/delete/{app_id}"
            
            response = requests.delete(url, auth=(self.username, self.access_key))
            
            if response.status_code == 200:
                print("✅ App deleted successfully!")
            else:
                print(f"❌ Failed to delete app: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error deleting app: {e}")


def main():
    """Main function to handle command line operations."""
    if len(sys.argv) < 2:
        print("📱 BrowserStack App Upload Utility")
        print("=" * 40)
        print("Usage:")
        print("  python upload_app.py upload <app_path> [custom_id]")
        print("  python upload_app.py list")
        print("  python upload_app.py delete <app_id>")
        print("\nExamples:")
        print("  python upload_app.py upload myapp.apk")
        print("  python upload_app.py upload myapp.apk my_custom_id")
        print("  python upload_app.py list")
        print("  python upload_app.py delete bs://app-id-here")
        return
    
    uploader = BrowserStackAppUploader()
    command = sys.argv[1].lower()
    
    if command == "upload":
        if len(sys.argv) < 3:
            print("❌ Please provide app path")
            return
            
        app_path = sys.argv[2]
        custom_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        app_url = uploader.upload_app(app_path, custom_id)
        
        if app_url:
            print(f"\n🎯 Use this app URL in your test script:")
            print(f"APP_ID = \"{app_url}\"")
            
    elif command == "list":
        uploader.list_uploaded_apps()
        
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Please provide app ID to delete")
            return
            
        app_id = sys.argv[2]
        uploader.delete_app(app_id)
        
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()