import feedparser

# 알라딘 도서 RSS를 읽어 들입니다.
d = feedparser.parse('http://www.aladin.co.kr/rss/special_new/351')

# 항목을 순회합니다.
for entry in d.entries:
    print('이름:', entry.title)
    print('타이틀:', entry.title)
    print()