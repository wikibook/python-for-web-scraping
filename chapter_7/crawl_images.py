import sys
import time
import requests
import lxml.html
import boto3

# S3 버킷 이름[자신이 생성한 버킷 이름으로 변경해 주세요]
S3_BUCKET_NAME = 'scraping-book'

def main():
    # Wikimedia Commons 페이지에서 이미지 URL을 추출합니다.
    image_urls = get_image_urls('https://commons.wikimedia.org/wiki/Category:Mountain_glaciers')
    # S3 Bucket 객체를 추출합니다.
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    
    for image_url in image_urls:
        # 2초 동안 대기합니다.
        time.sleep(2)
        
        # 이미지 파일을 내려받습니다.
        print('Downloading', image_url, file=sys.stderr)
        response = requests.get(image_url)
        
        # URL을 기반으로 파일 이름을 추출합니다.
        _, filename = image_url.rsplit('/', maxsplit=1)
        
        # 다운로드한 파일을 S3에 저장합니다.
        print('Putting', filename, file=sys.stderr)
        bucket.put_object(Key=filename, Body=response.content)

def get_image_urls(page_url):
    """
    매개변수로 전달된 페이지에 출력되고 있는 섬네일 이미지의 원래 URL을 추출합니다.
    """
    response = requests.get(page_url)
    html = lxml.html.fromstring(response.text)
    
    image_urls = []
    for img in html.cssselect('.thumb img'):
        thumbnail_url = img.get('src')
        image_urls.append(get_original_url(thumbnail_url))
    
    return image_urls

def get_original_url(thumbnail_url):
    """
    섬네일 URL에서 원래 이미지 URL을 추출합니다.
    """
    # /로 잘라서 디렉터리에 대응하는 부분의 URL을 추출합니다.
    directory_url, _ = thumbnail_url.rsplit('/', maxsplit=1)
    # /thumb/을 /로 변경해서 원래 이미지 URL을 추출합니다.
    original_url = directory_url.replace('/thumb/', '/')
    return original_url

if __name__ == '__main__':
    main()