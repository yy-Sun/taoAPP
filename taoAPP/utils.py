from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from appium import webdriver


def get_driver():
    server = 'http://localhost:4723/wd/hub'
    desired_caps = {
        "platformName": "Android",
        "deviceName": "8c34fd6e4dfe",
        "appPackage": "com.taobao.taobao",
        "appActivity": "com.taobao.tao.TBMainActivity"}
    desired_caps['noReset'] = True
    print('得到一个driver对象')
    return webdriver.Remote(server, desired_caps)


driver = get_driver()
wait = WebDriverWait(driver, 30)


def get_element_by_id(id, time_out=30):
    if time_out != 30:
        temp_wait = WebDriverWait(driver, time_out)
        element = None
        try:
            element = temp_wait.until(EC.presence_of_element_located((By.ID, id)))
        except TimeoutException:
            pass
        return element
    return wait.until(EC.presence_of_element_located((By.ID, id)))


def get_text_by_id(id, time_out=30):
    ele = get_element_by_id(id, time_out)
    if ele is not None:
        return ele.get_attribute('text')
    return ''


def get_desc_content_by_id(id, time_out=30):
    element = get_element_by_id(id, time_out)
    if element is not None:
        return element.get_attribute('contentDescription')
    return ''


def get_element_by_xpath(xpath, time_out=30, limit=0):
    if time_out != 30:
        temp_wait = WebDriverWait(driver, time_out)
        element = None
        try:
            element = temp_wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            pass
        if limit > 0:
            for i in range(5):
                if element is None:
                    element = temp_wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    continue
                break
        return element
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))


def get_text_by_xpath(xpath, time_out=30):
    element = get_element_by_xpath(xpath, time_out)
    if element is not None:
        return element.get_attribute('text')
    return ''


def get_desc_content_by_xpath(xpath, time_out=30):
    element = get_element_by_xpath(xpath, time_out)
    if element is not None:
        return element.get_attribute('contentDescription')
    return ''


def get_elements_by_xpath(xpath, time_out=30, limit=0):
    if time_out != 30:
        temp_wait = WebDriverWait(driver, time_out)
        elements = None
        try:
            elements = temp_wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            pass
        if limit > 0:
            for i in range(5):
                if elements is None or len(elements) < limit:
                    elements = temp_wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                    continue
                break
        return elements

    return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


def get_texts_by_xpath(xpath, time_out=30):
    texts = []
    elements = get_elements_by_xpath(xpath, time_out)
    if elements is not None:
        for ele in elements:
            texts.append(ele.get_attribute('text'))
    return texts


def get_desc_contents_by_xpath(xpath, time_out=30):
    descs = []
    elements = get_elements_by_xpath(xpath, time_out)
    if elements is not None:
        for ele in elements:
            descs.append(ele.get_attribute('contentDescription'))
    return descs


def get_size_by_xpath(xpath, num, time_out):
    return get_elements_by_xpath(xpath, time_out)[num].size


def get_size_by_id(id, time_out=30):
    element = get_element_by_id(id, time_out)
    size_map = {}
    if element is not None:
        return element.size
    return size_map  # width height


def swipe_up(up):
    driver.swipe(350, 1000, 350, 1000 - up, 1000)


def swipe_right(right):
    driver.swipe(100, 500, 100 + right, 500, 500)


def swipe_down(down):
    driver.swipe(500, 300, 500, 300 + down, 500)


def swipe_left(left):
    driver.swipe(600, 500, 600 - left, 500, 500)


def get_png_path_by_screen():
    return driver.get_screenshot_as_png()


def get_file(path):
    driver.get_screenshot_as_file(path)
