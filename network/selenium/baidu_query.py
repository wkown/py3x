from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keywords = "红楼梦"
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
assert "百度一下，你就知道" in driver.title
elem = driver.find_element_by_name("wd")
elem.send_keys(keywords)
elem.send_keys(Keys.RETURN)
# time.sleep(5) # 此方式不推荐
try:
    element = WebDriverWait(driver, 10).until(
        EC.title_contains(keywords)
    )
    print(driver.page_source)
finally:
    driver.quit()
