import matplotlib

# 렌더링 백엔드로 데스크톱 환경이 필요 없는 Agg를 사용합니다.
matplotlib.use('Agg')

# 한국어를 렌더링할 수 있게 폰트를 지정합니다.
# macOS와 우분투 모두 정상적으로 출력하도록 2개의 폰트를 지정했습니다.
# 기본 상태에서는 한국어가 □로 출력됩니다.
matplotlib.rcParams['font.sans-serif'] = 'NanumGothic,AppleGothic'
import matplotlib.pyplot as plt

# plot()의 세 번째 매개변수로 계열 스타일을 나타내는 문자열을 지정합니다.
# 'b'는 파란색, 'x'는 × 표시 마커, '-'는 마커를 실선으로 연결하라는 의미입니다.
# 키워드 매개변수 label로 지정한 계열의 이름은 범례로 사용됩니다.
plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'bx-', label='첫 번째 함수')

# 'r'은 붉은색,'o'는 ○ 표시 마커, '--'는 점선을 의미합니다.
plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 'ro--', label='두 번째 함수')
# xlabel() 함수로 X축의 레이블을 지정합니다.
plt.xlabel('X 값')
# ylabel() 함수로 Y축의 레이블을 지정합니다.
plt.ylabel('Y 값')
# title() 함수로 그래프의 제목을 지정합니다.
plt.title('matplotlib 샘플')
# legend() 함수로 범례를 출력합니다. loc='best'는 적당한 위치에 출력하라는 의미입니다.
plt.legend(loc='best')

# X축 범위를 0~6으로 지정합니다. ylim() 함수를 사용하면 Y축 범위를 지정할 수 있습니다.
plt.xlim(0, 6)

# 그래프를 그리고 파일로 저장합니다.
plt.savefig('advanced_graph.png', dpi=300)