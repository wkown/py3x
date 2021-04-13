from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

keywords = "红楼梦"

# 设置代理
PROXY = "http://127.0.0.1:8888"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={proxy}".format(proxy=PROXY))

driver = webdriver.Chrome(chrome_options=chrome_options)
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
