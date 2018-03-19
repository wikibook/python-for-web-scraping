import os
# pip install tweepy
import tweepy

# 환경변수에서 인증 정보를 추출합니다.
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 인증 정보를 설정합니다.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# API 클라이언트를 생성합니다.
api = tweepy.API(auth)

# 사용자의 타임라인을 추출합니다.
public_tweets = api.home_timeline()
for status in public_tweets:
    # 사용자 이름과 트윗을 출력합니다.
    print('@' + status.user.screen_name, status.text)