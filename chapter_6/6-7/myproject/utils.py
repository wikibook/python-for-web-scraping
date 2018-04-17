import logging
import lxml.html
import readability
# Readability의 DEBUG/INFO 수준의 로그를 출력하지 않게 합니다.
# Spider를 실행할 때 Readability의 로그가 많이 출력되므로
# 출력이 보기 힘들어지는 것을 막는 것입니다.
logging.getLogger('readability.readability').setLevel(logging.WARNING)
def get_content(html):
    """
    HTML 문자열에서 (<제목>, <본문>) 형태의 튜플을 찾은 뒤 반환합니다. 
    """
    document = readability.Document(html)
    content_html = document.summary()
    # HTM 태그를 제거하고 텍스트만 추출합니다.
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()
    
    return short_title, content_text