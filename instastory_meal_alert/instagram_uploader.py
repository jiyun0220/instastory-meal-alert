from instagrapi import Client
import os
from .config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, MEAL_STORY_IMAGE_PATH

class InstagramUploader:
    def __init__(self, session_path: str = ".ig_session.json"):
        self.client = Client()
        self.session_path = session_path
        self._login()

    def _login(self):
        if not all([INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD]):
            raise ValueError("인스타그램 계정 정보가 .env 파일에 설정되지 않았습니다.")

        if os.path.exists(self.session_path):
            try:
                self.client.load_settings(self.session_path)
                print("인스타그램 세션을 로드했습니다.")
                self.client.user_info(self.client.user_id)
                print("세션이 유효하여, 로그인을 건너뜁니다.")
                return
            except Exception as e:
                print(f"세션이 유효하지 않습니다 ({e}). 새로 로그인합니다.")

        try:
            print("아이디/비밀번호로 로그인을 시도합니다.")
            self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            self.client.dump_settings(self.session_path)
            print("인스타그램 세션을 저장했습니다.")
        except Exception as e:
            raise RuntimeError(f"인스타그램 로그인 실패: {e}") from e

    def upload_story(self):
        try:
            self.client.photo_upload_to_story(MEAL_STORY_IMAGE_PATH)
            print("인스타그램 스토리에 사진을 업로드했습니다.")
        except Exception as e:
            print(f"인스타그램 업로드 중 오류 발생: {e}")