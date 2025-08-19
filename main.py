import os
import re
import requests
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

def get_clean_meal_text(meal_type_code):
    """
    NEIS API에서 특정 식사 데이터를 가져와 깔끔한 텍스트로 반환합니다.
    """
    # ... (API 호출 부분은 이전과 동일)
    api_key = os.getenv("NEIS_API_KEY")
    if not api_key:
        raise ValueError("API 키가 .env 파일에 설정되지 않았습니다.")

    office_code = 'D10'
    school_code = '7240454'
    today = datetime.now().strftime("%Y%m%d")
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    
    params = {
        'KEY': api_key, 'Type': 'json', 'pIndex': 1, 'pSize': 100,
        'ATPT_OFCDC_SC_CODE': office_code, 'SD_SCHUL_CODE': school_code,
        'MLSV_YMD': today, 'MMEAL_SC_CODE': meal_type_code
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 데이터 파싱 및 정리
        meal_info = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        # HTML 태그와 알레르기 정보(숫자. 형식) 제거
        clean_text = re.sub(r'\s*\(\d+\.\d+\.\d+\.\d+\)', '', meal_info) # (1.2.3.4) 형식 제거
        clean_text = re.sub(r'\s*\(\d+\.\d+\)', '', clean_text) # (1.2) 형식 제거
        clean_text = re.sub(r'\s*\(\d+\)', '', clean_text) # (1) 형식 제거
        clean_text = clean_text.replace('<br/>', '\n') # <br/>을 줄바꿈으로 변경
        clean_text = re.sub(r'[\*#]', '', clean_text) # 특수문자 *, # 제거
        return clean_text.strip()

    except (requests.exceptions.RequestException, KeyError, IndexError):
        return "급식 정보가 없습니다."

def create_meal_image(breakfast, lunch, dinner):
    """
    조식, 중식, 석식 메뉴 텍스트를 받아 하나의 이미지로 생성합니다.
    """
    # 이미지 설정
    width, height = 1080, 1920  # 인스타 스토리 사이즈
    bg_color = "white"
    font_color = "black"
    
    # 새 이미지 생성
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # 폰트 설정 (시스템에 있는 기본 폰트 사용 시도, 없을 경우 Pillow 기본 폰트)
    try:
        # macOS의 경우 기본 한글 폰트 경로
        font_path = "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc"
        title_font = ImageFont.truetype(font_path, size=80)
        menu_font = ImageFont.truetype(font_path, size=50)
    except IOError:
        print("지정된 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
        title_font = ImageFont.load_default()
        menu_font = ImageFont.load_default()

    # 텍스트 그리기
    # Y 좌표
    y = 150
    
    # 조식
    draw.text((width/2, y), "🍙 조식", font=title_font, fill=font_color, anchor="mt")
    y += 120
    draw.text((100, y), breakfast, font=menu_font, fill=font_color, spacing=20)
    y += breakfast.count('\n') * 70 + 200 # 메뉴 줄 수에 따라 Y 간격 조절

    # 중식
    draw.text((width/2, y), "🍚 중식", font=title_font, fill=font_color, anchor="mt")
    y += 120
    draw.text((100, y), lunch, font=menu_font, fill=font_color, spacing=20)
    y += lunch.count('\n') * 70 + 200

    # 석식
    draw.text((width/2, y), "🌙 석식", font=title_font, fill=font_color, anchor="mt")
    y += 120
    draw.text((100, y), dinner, font=menu_font, fill=font_color, spacing=20)

    # 이미지 저장
    image.save("meal_story.png")
    print("'meal_story.png' 이미지가 성공적으로 생성되었습니다.")


if __name__ == "__main__":
    print("조식 정보 가져오는 중...")
    breakfast_menu = get_clean_meal_text("1")
    print("중식 정보 가져오는 중...")
    lunch_menu = get_clean_meal_text("2")
    print("석식 정보 가져오는 중...")
    dinner_menu = get_clean_meal_text("3")
    
    print("\n--- 정리된 메뉴 ---")
    print(f"[조식]\n{breakfast_menu}\n")
    print(f"[중식]\n{lunch_menu}\n")
    print(f"[석식]\n{dinner_menu}\n")

    print("\n이미지 생성 시작...")
    create_meal_image(breakfast_menu, lunch_menu, dinner_menu)
