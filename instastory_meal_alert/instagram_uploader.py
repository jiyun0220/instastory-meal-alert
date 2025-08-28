from instagrapi import Client
import os
from .config import MEAL_STORY_IMAGE_PATH

class InstagramUploader:
    def __init__(self, session_path: str = ".ig_session.json"):
        self.client = Client()
        self.session_path = session_path
        self._login()

    def _login(self):
        if not os.path.exists(self.session_path):
            raise FileNotFoundError(
                f"인스타그램 세션 파일({self.session_path})을 찾을 수 없습니다. "
            )

        try:
            print("인스타그램 세션을 로드합니다.")
            self.client.load_settings(self.session_path)
            self.client.user_info(self.client.user_id)
            print("세션이 유효하여, 로그인을 건너뜁니다.")
        except Exception as e:
            raise RuntimeError(f"인스타그램 세션이 유효하지 않습니다. 로컬에서 세션을 갱신해주세요. 오류: {e}") from e

    def upload_story(self):
        try:
            self.client.photo_upload_to_story(MEAL_STORY_IMAGE_PATH)
            print("인스타그램 스토리에 사진을 업로드했습니다.")
        except Exception as e:
            print(f"인스타그램 업로드 중 오류 발생: {e}")
