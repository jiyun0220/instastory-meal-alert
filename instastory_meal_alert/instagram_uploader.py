from instagrapi import Client
import os
import json
from .config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, MEAL_STORY_IMAGE_PATH

class InstagramUploader:
    def __init__(self, session_path: str = ".ig_session.json"):
        self.client = Client()
        self.session_path = session_path
        self._login()

    def _load_session(self):
        if os.path.exists(self.session_path):
            try:
                with open(self.session_path, "r") as f:
                    settings = json.load(f)
                self.client.set_settings(settings)
                print("인스타그램 세션을 로드했습니다.")
            except Exception:
                print("세션 로드 실패. 새 로그인 시도합니다.")

    def _save_session(self):
        try:
            with open(self.session_path, "w") as f:
                json.dump(self.client.get_settings(), f)
            print("인스타그램 세션을 저장했습니다.")
        except Exception:
            print("세션 저장 실패(무시).")

    def _login(self):
        if not all([INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD]):
            raise ValueError("인스타그램 계정 정보가 .env 파일에 설정되지 않았습니다.")

        self._load_session()

        try:
            self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            self._save_session()
        except Exception as e:
            print(f"인스타그램 로그인 실패: {e}")
            try:
                self.client = Client()
                self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                self._save_session()
            except Exception as e2:
                raise RuntimeError(f"인스타그램 로그인 재시도 실패: {e2}") from e

    def upload_story(self):
        try:
            self.client.photo_upload_to_story(MEAL_STORY_IMAGE_PATH)
            print("인스타그램 스토리에 사진을 업로드했습니다.")
        except Exception as e:
            print(f"인스타그램 업로드 중 오류 발생: {e}")
