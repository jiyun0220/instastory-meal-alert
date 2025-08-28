import os
import getpass
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

print("인스타그램 세션 생성을 시작합니다.")
print("아이디와 비밀번호를 입력해주세요.")

username = os.getenv("INSTAGRAM_USERNAME") or input("Instagram Username: ")
password = os.getenv("INSTAGRAM_PASSWORD") or getpass.getpass("Instagram Password: ")

client = Client()

try:
    client.login(username, password)
except Exception as e:
    if "ChallengeRequired" in str(e) or "Please check your inbox" in str(e):
        verification_code = input("인스타그램에서 받은 6자리 코드를 입력하세요: ")
        client.login(username, password, verification_code=verification_code)
    else:
        raise e

client.dump_settings(".ig_session.json")
print("\n로그인 성공! .ig_session.json 파일이 생성되었습니다.")

