import sys
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def find_textboxes_recursively(layout_obj):
    """
    재귀적으로 텍스트 박스(LTTextBox)를 찾고
    텍스트 박스들을 리스트로 반환합니다.
    """
    # LTTextBox를 상속받은 객체의 경우 리스트에 곧바로 넣어서 반환합니다.
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]
    # LTContainer를 상속받은 객체의 경우 자식 요소를 포함하고 있다는 의미이므로
    # 재귀적으로 자식 요소를 계속 찾습니다.
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))
        return boxes
    # 아무것도 없다면 빈 리스트를 반환합니다.
    return []

# 공유 리소스를 관리하는 리소스 매니저를 생성합니다.
laparams = LAParams()
resource_manager = PDFResourceManager()

# 페이지를 모으는 PageAggregator 객체를 생성합니다.
device = PDFPageAggregator(resource_manager, laparams=laparams)

# Interpreter 객체를 생성합니다.
interpreter = PDFPageInterpreter(resource_manager, device)

# 파일을 바이너리 형식으로 읽어 들입니다.
with open(sys.argv[1], 'rb') as f:
    # PDFPage.get_pages()로 파일 객체를 지정합니다.
    # PDFPage 객체를 차례대로 추출합니다.
    # 키워드 매개변수인 pagenos로 처리할 페이지 번호(0-index)를 리스트 형식으로 지정할 수도 있습니다.
    for page in PDFPage.get_pages(f):
        # 페이지를 처리합니다.
        interpreter.process_page(page)
        # LTPage 객체를 추출합니다.
        layout = device.get_result()
        # 페이지 내부의 텍스트 박스를 리스트로 추출합니다.
        boxes = find_textboxes_recursively(layout)
        # 텍스트 박스를 왼쪽 위의 좌표부터 차례대로 정렬합니다.
        # y1(Y 좌표)는 위에 있을수록 크므로 음수로 변환하게 해서 비교했습니다.
        boxes.sort(key=lambda b: (-b.y1, b.x0))
        for box in boxes:
            # 읽기 쉽게 선을 출력합니다.
            print('-' * 10)
            # 텍스트 박스의 내용을 출력합니다.
            print(box.get_text().strip())