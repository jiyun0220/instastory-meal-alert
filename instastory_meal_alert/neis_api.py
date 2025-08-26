import re
import requests
from datetime import datetime, timezone, timedelta
from .config import NEIS_API_KEY, OFFICE_CODE, SCHOOL_CODE


def get_meal_data(meal_type_code: str) -> str:
    """NEIS API를 통해 급식 정보를 가져옵니다."""
    if not NEIS_API_KEY:
        raise ValueError("API 키가 .env 파일에 설정되지 않았습니다.")

    kst = timezone(timedelta(hours=9))
    today = datetime.now(kst).strftime("%Y%m%d")
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        'KEY': NEIS_API_KEY,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 100,
        'ATPT_OFCDC_SC_CODE': OFFICE_CODE,
        'SD_SCHUL_CODE': SCHOOL_CODE,
        'MLSV_YMD': today,
        'MMEAL_SC_CODE': meal_type_code
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        meal_info = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        return _clean_meal_text(meal_info)
    except (requests.exceptions.RequestException, KeyError, IndexError):
        return "급식 정보가 없습니다."

def _clean_meal_text(text: str) -> str:
    """급식 정보 텍스트를 정제합니다."""
    text = re.sub(r'\s*\([^)]*\)', '', text)
    text = text.replace('<br/>', '\n')
    text = re.sub(r'[\*#]', '', text)
    return text.strip()
