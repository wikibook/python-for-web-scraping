from scrapy.exceptions import DropItem

from pymongo import MongoClient
import MySQLdb


class ValidationPipeline(object):
    """
    Item을 검증하는 Pipeline
    """
    def process_item(self, item, spider):
        if not item['title']:
            # title 필드가 추출되지 않으면 제거합니다.
            # DropItem()의 매개변수로 제거 이유를 나타내는 메시지를 입력합니다.
            raise DropItem('Missing title')
        # title 필드가 제대로 추출된 경우
        return item  
        
class MongoPipeline(object):
    """
    Itemd을 MongoDB에 저장하는 Pipeline
    """
    def open_spider(self, spider):
        """
        Spider를 시작할 때 MongoDB에 접속합니다.
        """
        # 호스트와 포트를 지정해서 클라이언트를 생성합니다.
        self.client = MongoClient('localhost', 27017)
         # scraping-book 데이터베이스를 추출합니다.
        self.db = self.client['scraping-book']
        # items 콜렉션을 추출합니다.
        self.collection = self.db['items']
    
    def close_spider(self, spider):
        """
        Spider가 종료될 때 MongoDB 접속을 끊습니다.
        """
        self.client.close()
    def process_item(self, item, spider):
        """
        Item을 콜렉션에 추가합니다.
        """
        # insert_one()의 매개변수에는 item을 깊은 복사를 통해 전달합니다.
        self.collection.insert_one(dict(item))
        return item

class MySQLPipeline(object):
    """
    Item을 MySQL에 저장하는 Pipeline
    """
    
    def open_spider(self, spider):
        """
        Spider를 시작할 때 MySQL 서버에 접속합니다.
        items 테이블이 존재하지 않으면 생성합니다.
        """
        # settings.py에서 설정을 읽어 들입니다.
        settings = spider.settings
        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'scraping'),
            'user': settings.get('MYSQL_USER', ''),
            'passwd': settings.get('MYSQL_PASSWORD', ''),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }
        # MySQL 서버에 접속합니다.
        self.conn = MySQLdb.connect(**params) 
        # 커서를 추출합니다.
        self.c = self.conn.cursor() 
        # items 테이블이 존재하지 않으면 생성합니다.
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER NOT NULL AUTO_INCREMENT,
                title CHAR(200) NOT NULL,
                PRIMARY KEY (id)
            )
        ''')
        # 변경을 커밋합니다.
        self.conn.commit()
    
    def close_spider(self, spider):
        """
        Spider가 종료될 때 MySQL 서버와의 접속을 끊습니다.
        """
        self.conn.close()
    def process_item(self, item, spider):
        """
        Item을 items 테이블에 삽입합니다.
        """
        self.c.execute('INSERT INTO items (title) VALUES (%(title)s)', dict(item))
        self.conn.commit()
        return item