from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# PhantomJS 모듈의 WebDriver 객체를 생성합니다.
driver = webdriver.PhantomJS()

# Google 메인 페이지를 엽니다.
driver.get('https://www.google.co.kr/')

# 타이틀에 'Google'이 포함돼 있는지 확인합니다.
assert 'Google' in driver.title

# 검색어를 입력하고 검색합니다.
input_element = driver.find_element_by_name('q')
input_element.send_keys('Python')
input_element.send_keys(Keys.RETURN)

# 타이틀에 'Python'이 포함돼 있는지 확인합니다.
assert 'Python' in driver.title

# 스크린샷을 찍습니다.
driver.save_screenshot('search_results.png')

# 검색 결과를 출력합니다.
for a in driver.find_elements_by_css_selector('h3 > a'):
    print(a.text)
    print(a.get_attribute('href'))
    print()