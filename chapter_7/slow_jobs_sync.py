import time

def slow_job(n):
    """
    매개변수로 지정한 시간 만큼 시간이 걸리는 처리를 수행하는 함수입니다.
    time.sleep()을 사용해 시간이 걸리는 처리를 비슷하게 재현해 봤습니다.
    """
    print('Job {0} will take {0} seconds'.format(n))
    # n초 대기합니다.
    time.sleep(n)
    print('Job {0} finished'.format(n))

slow_job(1)
slow_job(2)
slow_job(3)