from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_search_functionality(driver):
    # Wait for and click on the search bar
    search_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    search_element.click()

    # Enter search query
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
    )
    search_input.send_keys("Appium")

    # Validate that at least one result appears
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((MobileBy.ID, "org.wikipedia.alpha:id/page_list_item_title"))
    )
    assert len(results) > 0, "No search results found"
