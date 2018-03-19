# Rect라는 이름의 클래스를 지정합니다.
class Rect:
    # 인스턴스가 생성될 때 호출되는 특수한 메서드를 정의합니다.
    def __init__(self, width, height):
        self.width = width    # width 속성에 값을 할당합니다.
        self.height = height  # height 속성에 값을 할당합니다.
    # 사각형의 넓이를 계산하는 메서드를 정의합니다.
    def area(self):
        return self.width * self.height

r = Rect(100, 20)
print(r.width, r.height, r.area())   # 100 20 2000을 출력합니다.

# Rect를 상속받아 Square 클래스를 정의합니다.
class Square(Rect):
    def __init__(self, width):
        # 부모 클래스의 메서드를 호출합니다.
        super().__init__(width, width)