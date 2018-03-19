from redis import Redis
from rq import Queue
from tasks import add

# localhost의 TCP 포트 6379에 있는 Redis에 접속합니다.
# 이러한 매개변수는 기본값이므로 생략해도 됩니다.
conn = Redis('localhost', 6379)

# default라는 이름의 Queue 객체를 추출합니다.
# 이 이름도 기본값이므로 생략해도 됩니다
q = Queue('default', connection=conn)

# 함수와 매개변수를 지정하고 잡을 추가합니다.
q.enqueue(add, 3, 4)