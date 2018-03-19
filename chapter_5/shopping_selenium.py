import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 인증 정보를 환경변수에서 추출합니다.
NAVER_ID = os.environ['NAVER_ID']
NAVER_PASSWORD = os.environ['NAVER_PASSWORD']

def main():
    """
    메인 처리
    """
    # PhantomJS의 WebDriver 객체를 생성합니다.
    driver = webdriver.PhantomJS()
    
    # 화면 크기를 설정합니다.
    driver.set_window_size(800, 600)
    
    # 로그인하고 이동한 뒤 주문 이력을 가져옵니다.
    sign_in(driver)
    navigate(driver)
    goods = scrape_history(driver)
    # 출력합니다.
    print(goods)

def sign_in(driver):
    """
    로그인합니다
    """
    print('Navigating...', file=sys.stderr)
    print('Waiting for sign in page loaded...', file=sys.stderr)
    time.sleep(2)
    
    # 입력 양식을 입력하고 전송합니다.
    driver.get('https://nid.naver.com/nidlogin.login')
    e = driver.find_element_by_id('id')
    e.clear()
    e.send_keys(NAVER_ID)
    e = driver.find_element_by_id('pw')
    e.clear()
    e.send_keys(NAVER_PASSWORD)
    form = driver.find_element_by_css_selector("input.btn_global[type=submit]")
    form.submit()

def navigate(driver):
    """
    적절한 페이지로 이동한 뒤 
    """
    print('Navigating...', file=sys.stderr)
    driver.get("https://order.pay.naver.com/home?tabMenu=SHOPPING")
    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)
    
    # 페이지를 아래로 스크롤합니다.
    # 사실 현재 예제에서는 필요 없지만 활용 예를 위해 넣어봤습니다.
    # 스크롤을 해서 데이터를 가져오는 페이지의 경우 활용할 수 있습니다.
    driver.execute_script('scroll(0, document.body.scrollHeight)')
    wait = WebDriverWait(driver, 10)
    
    # [더보기] 버튼을 클릭할 수 있는 상태가 될 때까지 대기하고 클릭합니다.
    # 두 번 클릭해서 과거의 정보까지 들고옵니다.
    driver.save_screenshot('note-1.png')
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_moreButton a')))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_moreButton a')))
    button.click()
    # 2초 대기합니다.
    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)

def scrape_history(driver):
    """
    페이지에서 주문 이력을 추출합니다.
    """
    goods = []
    for info in driver.find_elements_by_css_selector('.p_info'):
        # 요소를 추출합니다.
        link_element = info.find_element_by_css_selector('a')
        title_element = info.find_element_by_css_selector('span')
        date_element = info.find_element_by_css_selector('.date')
        price_element = info.find_element_by_css_selector('em')
        # 텍스트를 추출합니다.
        goods.append({
            'url': link_element.get_attribute('.a'),
            'title': title_element.text,
            'description': date_element.text + " - " + price_element.text + "원"
        })
    return goods
    
if __name__ == '__main__':
    main()