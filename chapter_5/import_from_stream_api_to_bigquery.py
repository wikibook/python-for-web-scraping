import os
import sys
from datetime import timezone
import tweepy
import bigquery

# 트위터 인증 정보를 읽어 들입니다.
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# BigQuery 인증 정보(credentials.json)을 지정해 BigQuery 클라이언트를 생성합니다.
# 명시적으로 readonly=False를 지정하지 않으면 쓰기 작업을 할 수 없습니다.
client = bigquery.get_client(json_key_file='credentials.json', readonly=False)

# BigQuery 데이터 세트 이름
DATASET_NAME = 'twitter'

# BigQuery 테이블 이름
TABLE_NAME = 'tweets'

# 테이블이 존재하지 않으면 생성합니다.
if not client.check_table(DATASET_NAME, TABLE_NAME):
    print('Creating table {0}.{1}'.format(DATASET_NAME, TABLE_NAME), file=sys.stderr)
    # create_table()의 3번째 매개변수로 스키마를 지정합니다.
    client.create_table(DATASET_NAME, TABLE_NAME, [
        {'name': 'id',          'type': 'string',    'description': '트윗 ID'},
        {'name': 'lang',        'type': 'string',    'description': '트윗 언어'},
        {'name': 'screen_name', 'type': 'string',    'description': '사용자 이름'},
        {'name': 'text',        'type': 'string',    'description': '트윗 문장'},
        {'name': 'created_at',  'type': 'timestamp', 'description': '트윗 날짜'},
    ])

class MyStreamListener(tweepy.streaming.StreamListener):
    """
    Streaming API로 추출한 트윗을 처리하기 위한 클래스
    """
    status_list = []
    num_imported = 0
    def on_status(self, status):
        """
        트윗을 추출할 때 호출되는 메서드입니다.
        매개변수: 트윗을 나타내는 Status 객체
        """
        # Status 객체를 status_list에 추가합니다.
        self.status_list.append(status)
        if len(self.status_list) >= 500:
            # status_list에 500개의 데이터가 모이면 BigQuery에 임포트합니다.
            if not push_to_bigquery(self.status_list):
                # 임포트에 실패하면 False가 반환되므로 오류를 출력하고 종료합니다.
                print('Failed to send to bigquery', file=sys.stderr)
                return False
            # num_imported를 추가한 뒤 status_list를 비웁니다.
            self.num_imported += len(self.status_list)
            self.status_list = []
            print('Imported {0} rows'.format(self.num_imported), file=sys.stderr)
            # 요금이 많이 나오지 않게 5000개를 임포트했으면 종료합니다.
            # 계속 임포트하고 싶다면 다음 두 줄을 주석 처리해 주세요.
            if self.num_imported >= 5000:
                return False

    def push_to_bigquery(status_list):
        """
        트윗 리스트를 BigQuery에 임포트하는 메서드입니다.
        """
        # Tweepy의 Status 객체 리스트를 dict 리스트로 변환합니다.
        rows = []
        for status in status_list:
            rows.append({
                'id': status.id_str,
                'lang': status.lang,
                'screen_name': status.author.screen_name,
                'text': status.text,
                # datetime 객체를 UTC POSIX 타임스탬프로 변환합니다.
                'created_at': status.created_at.replace(tzinfo=timezone.utc).timestamp(),
            })
        # dict 리스트를 BigQuery에 임포트합니다.
        # 매개변수는 순서대로
        # <데이터 세트 이름>, <테이블 이름>, <데이터 리스트>, <데이터를 식별할 필드 이름>입니다.
        # insert_id_key는 데이터가 중복되지 않게 만들려고 사용했습니다.
        return client.push_rows(DATASET_NAME, TABLE_NAME, rows, insert_id_key='id')

# Stream API로 읽어 들이기 시작합니다.
print('Collecting tweets...', file=sys.stderr)
stream = tweepy.Stream(auth, MyStreamListener())

# 공개된 트윗을 샘플링한 스트림을 받습니다.
# 언어를 지정하지 않았으므로 모든 언어의 트윗을 추출할 수 있습니다.
stream.sample()