d = {'a': 1, 'b': 2}
try:
    # 예외가 발생할 가능성이 있는 처리를 넣습니다.
    print(d['x'])
except KeyError:
    # try 절 내부에서 except 절에 작성된 예외(현재 예제에서는 KeyError)가 발생하면
    # except 절이 실행됩니다. 여기서는 키가 존재하지 않을 때의 처리 내용을 지정했습니다.
    print('x is not found')

# open() 함수의 반환값은 변수 f에 할당되며 with 블록 내부에서 사용합니다.
# 이렇게 사용하면 블록을 벗어날 때 f.close()가 자동으로 호출됩니다.
with open('index.html') as f:
    print(f.read())