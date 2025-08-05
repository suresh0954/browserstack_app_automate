# BrowserStack + Percy Mobile App Testing

This project provides a comprehensive Python script for automated mobile app testing using BrowserStack SDK with Percy integration for visual testing.

## Features

- ✅ **BrowserStack Authentication**: Loads credentials from shell script
- ✅ **Percy Integration**: Visual testing with automatic snapshots
- ✅ **Mobile App Automation**: Click, type, and search functionality
- ✅ **Real Device Testing**: Tests on real Android/iOS devices
- ✅ **Comprehensive Logging**: Detailed execution logs with emojis
- ✅ **Error Handling**: Robust error handling with fallback strategies
- ✅ **App Upload Utility**: Easy app upload to BrowserStack

## Prerequisites

1. **BrowserStack Account**: Sign up at [BrowserStack](https://www.browserstack.com/)
2. **Percy Account**: Sign up at [Percy](https://percy.io/)
3. **Python 3.7+**: Ensure Python is installed
4. **Mobile App**: Have your `.apk` (Android) or `.ipa` (iOS) file ready

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Credentials

Edit the `creds.sh` file with your actual credentials:

```bash
export BROWSERSTACK_USERNAME="your_actual_username"
export BROWSERSTACK_ACCESS_KEY="your_actual_access_key"
export APP_USERNAME="dummy_username"
export APP_PASSWORD="dummy_password"
export BROWSERSTACK_BUILD_NAME="Automate Build #123"
export BROWSERSTACK_PROJECT_NAME="bs-demo-cert"
export PERCY_TOKEN="your_actual_percy_token"
```

**How to get credentials:**

- **BrowserStack**: Login to BrowserStack → Account → Access Key
- **Percy**: Login to Percy → Account Settings → Tokens → Create New Token

### 4. Upload Your App

Use the provided utility to upload your app to BrowserStack:

```bash
# Upload app and get app ID
python upload_app.py upload path/to/your/app.apk

# List uploaded apps
python upload_app.py list

# Delete an app (if needed)
python upload_app.py delete bs://app-id-here
```

### 5. Update App ID

Copy the app URL from the upload step and update it in `browserstack_percy_app_test.py`:

```python
# Replace this line in the main() function
APP_ID = "bs://your-actual-app-id-here"
```

## Running the Tests

### Basic Test Execution

```bash
# Make the script executable
chmod +x browserstack_percy_app_test.py

# Run the test
python browserstack_percy_app_test.py
```

### Advanced Usage

You can customize the test by modifying the script:

1. **Change Device**: Edit the `setup_driver()` method
2. **Custom Test Flow**: Modify the `run_custom_test_flow()` method
3. **App-Specific Elements**: Update locators in `perform_search_test()`

## Script Features

### Authentication
- Automatically loads credentials from `creds.sh`
- Validates all required credentials before starting
- Supports environment variable override

### Percy Integration
- Takes snapshots after every major action
- Configurable snapshot names and options
- Handles Percy failures gracefully

### Mobile Automation
- Smart element detection with multiple locator strategies
- Robust wait conditions
- Cross-platform support (Android/iOS)

### Error Handling
- Graceful degradation on element not found
- Comprehensive logging with status indicators
- Automatic cleanup on failure

## Test Flow

The script performs the following actions:

1. **🔧 Setup**: Load credentials and initialize WebDriver
2. **📸 Initial Snapshot**: Capture app launch state
3. **🔍 Search Element Detection**: Find search field/button using multiple strategies
4. **👆 Click Action**: Click search element + Percy snapshot
5. **⌨️ Text Input**: Type search query + Percy snapshot
6. **🔍 Search Execution**: Perform search + Percy snapshot
7. **📊 Results Verification**: Capture final state + Percy snapshot
8. **🧹 Cleanup**: End session and cleanup resources

## Customization

### Adding Custom Test Steps

```python
def run_custom_test_flow(self):
    """Add your custom test steps here."""
    
    # Click a specific button
    self.click_element(AppiumBy.ID, "my_button_id", "My Custom Button")
    
    # Type in a specific field
    self.type_text(AppiumBy.ID, "my_input_id", "Custom Text", "My Input Field")
    
    # Take a custom snapshot
    self.take_percy_snapshot("Custom Test State")
```

### Changing Device Configuration

```python
# In setup_driver() method, modify these capabilities:
"device": "Google Pixel 7",
"os_version": "13.0",
"platformName": "Android",  # or "iOS"
```

### Percy Snapshot Options

```python
# Add custom Percy options
percy_options = {
    "fullPage": True,
    "widths": [375, 768, 1024]
}
self.take_percy_snapshot("Custom Snapshot", percy_options)
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify credentials in `creds.sh`
   - Check BrowserStack account status
   - Ensure Percy token is valid

2. **App Not Found**
   - Verify app ID is correct
   - Check if app upload was successful
   - Use `python upload_app.py list` to see uploaded apps

3. **Element Not Found**
   - Update element locators for your specific app
   - Use Appium Inspector to find correct element IDs
   - Check if app UI has changed

4. **Percy Snapshots Failing**
   - Verify Percy token is correct
   - Check Percy project settings
   - Ensure Percy service is available

### Debug Mode

Enable verbose logging by modifying the script:

```python
# Add this at the beginning of main()
import logging
logging.basicConfig(level=logging.DEBUG)
```

## File Structure

```
├── browserstack_percy_app_test.py  # Main test script
├── upload_app.py                   # App upload utility
├── creds.sh                        # Credentials file
├── requirements.txt                # Python dependencies
├── conftest.py                     # Pytest configuration
├── test_sample.py                  # Sample test
└── README.md                       # This file
```

## Dependencies

- `appium-python-client>=2.11.1`: Appium automation
- `selenium>=4.0.0`: WebDriver protocol
- `percy-appium-app>=1.2.0`: Percy visual testing
- `python-dotenv>=1.0.0`: Environment variable management
- `pytest>=7.0.0`: Testing framework

## Support

- **BrowserStack Docs**: [App Automate Documentation](https://www.browserstack.com/docs/app-automate)
- **Percy Docs**: [Percy for Mobile Apps](https://docs.percy.io/docs/mobile-apps)
- **Appium Docs**: [Appium Documentation](https://appium.io/docs/en/)

## Security Notes

- Never commit `creds.sh` with real credentials to version control
- Use environment variables in CI/CD pipelines
- Rotate access keys regularly
- Keep Percy tokens secure

## License

This project is provided as-is for educational and testing purposes.


