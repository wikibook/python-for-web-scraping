import smtplib
from email.mime.text import MIMEText
from email.header import Header

# MIMEText 객체로 메일을 생성합니다.
msg = MIMEText('메일 본분입니다.')  

# 제목에 한글이 포함될 경우 Header 객체를 사용합니다.
msg['Subject'] = Header('메일 제목입니다.', 'utf-8') 
msg['From'] = 'me@example.com'
msg['To'] = 'you@example.com'

# SMTP()의 첫 번째 매개변수에 SMTP 서버의 호스트 이름을 지정합니다.
with smtplib.SMTP('localhost') as smtp:
    # 메일을 전송합니다.
    smtp.send_message(msg)

'''
with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
    # 구글 계정의 사용자 이름과 비밀번호를 지정해서 로그인합니다.
    # 2단계 인증을 설정한 경우 애플리케이션 비밀번호를 사용해 주세요.
    smtp.login('사용자 이름', '비밀번호')
    # send_message() 메서드로 메일을 전송합니다.
    smtp.send_message(msg)
'''
