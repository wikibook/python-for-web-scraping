import sys
import os
import cv2

try:
    # 얼굴 검출 전용 특징량 파일의 경로
    cascade_path = sys.argv[1]
except IndexError:
    # 명령어 매개변수가 부족한 경우에는 사용법을 출력하고 곧바로 종료합니다.
    print('Usage: python extract_faces.py CASCADE_PATH IMAGE_PATH...', file=sys.stderr)
    exit(1)

# 얼굴 이미지 출력 대상 디렉터리가 존재하지 않으면 생성해 둡니다.
output_dir = 'faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 특징량 파일이 존재하는지 확인합니다.
assert os.path.exists(cascade_path)
# 특징량 파일의 경로를 지정해 분석 객체를 생성합니다.
classifier = cv2.CascadeClassifier(cascade_path)

# 두 번째 이후의 매개변수 파일 경로를 반복 처리합니다.
for image_path in sys.argv[2:]:
    print('Processing', image_path, file=sys.stderr)
    
    # 명령어 매개변수에서 얻은 경로의 이미지 파일을 읽어 들입니다.
    image = cv2.imread(image_path)
    # 얼굴 검출을 빠르게 할 수 있게 이미지를 그레이스케일로 변환합니다.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 얼굴을 검출합니다.
    faces = classifier.detectMultiScale(gray_image)
    
    # 이미지 파일 이름의 확장자를 제거합니다.
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # 추출된 얼굴의 리스트를 반복 처리합니다.
    # i는 0부터 시작되는 순번입니다.
    for i, (x, y, w, h) in enumerate(faces):
        # 얼굴 부분만 자릅니다.
        face_image = image[y:y + h, x: x + w]
        # 출력 대상 파일 경로를 생성합니다.
        output_path = os.path.join(output_dir, '{0}_{1}.jpg'.format(image_name, i))
        # 얼굴 이미지를 저장합니다.
        cv2.imwrite(output_path, face_image)