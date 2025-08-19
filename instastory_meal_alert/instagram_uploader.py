from instagrapi import Client
from .config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, MEAL_STORY_IMAGE_PATH

class InstagramUploader:
    def __init__(self):
        self.client = Client()
        self._login()

    def _login(self):
        if not all([INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD]):
            raise ValueError("인스타그램 계정 정보가 .env 파일에 설정되지 않았습니다.")
        self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    def upload_story(self):
        try:
            self.client.photo_upload_to_story(MEAL_STORY_IMAGE_PATH)
            print("인스타그램 스토리에 사진을 업로드했습니다.")
        except Exception as e:
            print(f"인스타그램 업로드 중 오류 발생: {e}")
