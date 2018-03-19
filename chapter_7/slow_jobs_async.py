import asyncio

async def slow_job(n):
    """
    매개변수로 지정한 시간 만큼 시간이 걸리는 처리를
    비동기적으로 수행하는 코루틴입니다.
    asyncio.sleep()을 사용해 시간이 걸리는 처리를 비슷하게 재현해 봤습니다.
    """
    print('Job {0} will take {0} seconds'.format(n))
    # n초 동안 정지
    # await는 처리가 끝날 때까지 대기하는 구문입니다.
    await asyncio.sleep(n) 
    print('Job {0} finished'.format(n))

# 이벤트 루프 추출
loop = asyncio.get_event_loop()
# 3개의 코루틴을 생성합니다. 코루틴은 현재 시점에서 실행되는 것이 아닙니다.
coroutines = [slow_job(1), slow_job(2), slow_job(3)]
# 이벤트 루프로 3개의 코루틴을 실행합니다. 모두 종료될 때까지 이 줄에서 대기합니다.
loop.run_until_complete(asyncio.wait(coroutines))