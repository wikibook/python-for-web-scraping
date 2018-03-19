import os
from requests_oauthlib import OAuth1Session

# 환경변수에서 인증 정보를 추출합니다.
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 인증 정보를 사용해 OAuth1Session 객체를 생성합니다.
twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)

# 사용자의 타임라인을 추출합니다.
response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

# API 응답이 JSON 형식의 문자열이므로 response.json()으로 파싱합니다.
# status는 트윗(Twitter API에서는 Status라고 부릅니다)를 나타내는 dict입니다.
for status in response.json():
    # 사용자 이름과 트윗을 출력합니다.
    print('@' + status['user']['screen_name'], status['text'])