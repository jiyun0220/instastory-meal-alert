import schedule
import time
from .neis_api import get_meal_data
from .image_generator import ImageGenerator
from .instagram_uploader import InstagramUploader

class Scheduler:
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.instagram_uploader = InstagramUploader()

    def _job(self):
        print("급식 정보 확인 및 이미지 생성을 시작합니다.")
        breakfast = get_meal_data("1")
        lunch = get_meal_data("2")
        dinner = get_meal_data("3")

        if "없습니다" in breakfast and "없습니다" in lunch and "없습니다" in dinner:
            print("오늘은 급식 정보가 없습니다.")
            return

        self.image_generator.create(breakfast, lunch, dinner)
        print("급식 이미지를 생성했습니다.")
        self.instagram_uploader.upload_story()

    def run(self):
        print("스케줄러를 시작합니다. 매일 06:50에 작업이 실행됩니다.")
        schedule.every().day.at("06:50").do(self._job)

        self._job()

        while True:
            schedule.run_pending()
            time.sleep(60)
