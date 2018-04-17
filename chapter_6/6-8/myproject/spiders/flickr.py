import os
from urllib.parse import urlencode
import scrapy
class FlickrSpider(scrapy.Spider):
    name = "flickr"
    # Files Pipeline으로 다운로드하는 이미지 파일은 allowed_domains에
    # 제한을 받으므로 allowed_domains에 'staticflickr.com'을 추가해야 합니다
    allowed_domains = ["api.flickr.com"]
    
    # 키워드 매개변수로 Spider 매개변수 값을 받습니다.
    def __init__(self, text='sushi'):
        # 부모 클래스의 __init__()을 실행합니다.
        super().__init__()
        # 환경변수와 Spider 매개변수 값을 사용해 start_urls를 조합합니다.
        # urlencode() 함수는 매개변수로 지정한 dict의 키와 값을 URI 인코드해서
        # key1=value1&key2=value2라는 문자열로 반환해 줍니다.
        self.start_urls = [
            'https://api.flickr.com/services/rest/?' + urlencode({
                'method': 'flickr.photos.search',
                'api_key': os.environ['FLICKR_API_KEY'],
                'text': text,
                'sort': 'relevance',
                # CC BY 2.0, CC BY-SA 2.0, CC0를 지정합니다.
                'license': '4,5,9',  
            }),
        ]
    def parse(self, response):
        """
        API의 응답을 파싱해서 file_urls라는 키를 포함한 dict를 생성하고 yield합니다.
        """
        for photo in response.css('photo'):
            yield {'file_urls': [flickr_photo_url(photo)]}

def flickr_photo_url(photo):
    """
    플리커 사진 URL을 조합합니다.
    참고: https://www.flickr.com/services/api/misc.urls.html
    """
    # 이 경우는 XPath가 CSS 선택자보다 쉬우므로 XPath를 사용하겠습니
    return 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
        farm=photo.xpath('@farm').extract_first(),
        server=photo.xpath('@server').extract_first(),
        id=photo.xpath('@id').extract_first(),
        secret=photo.xpath('@secret').extract_first(),
        size='b',
    )