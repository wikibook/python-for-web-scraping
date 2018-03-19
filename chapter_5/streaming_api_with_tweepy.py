import os
import tweepy

# 환경변수에서 인증 정보를 추출합니다.
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 인증 정보를 설정합니다.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
class MyStreamListener(tweepy.StreamListener):
    """
    Streaming API로 추출한 트윗을 처리하는 클래스입니다.
    """
    def on_status(self, status):
        """
        트윗을 받을 때 호출되는 메서드
        매개변수로 트윗을 나타내는 Status 객체가 전달됩니다.
        """
        print('@' + status.author.screen_name, status.text)
# 인증 정보와 StreamListener를 지정해서 Stream 객체를 추출합니다.
stream = tweepy.Stream(auth, MyStreamListener())

# 공개돼 있는 트윗을 샘플링한 스트림을 받습니다.
# 키워드 매개변수인 languages로 한국어 트윗만 추출합니다
stream.sample(languages=['ko'])