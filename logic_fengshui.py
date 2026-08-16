# logic_fengshui.py

# ==========================================
# 1. 구성기학(Nine-Star Ki) 메타데이터
# ==========================================
NINE_STARS = {
    1: {"name": "일백수성(一白水星)", "element": "수(水)", "trigram": "감(坎)", "group": "동사택"},
    2: {"name": "이흑토성(二黑土星)", "element": "토(土)", "trigram": "곤(坤)", "group": "서사택"},
    3: {"name": "삼벽목성(三碧木星)", "element": "목(木)", "trigram": "진(震)", "group": "동사택"},
    4: {"name": "사록목성(四綠木星)", "element": "목(木)", "trigram": "손(巽)", "group": "동사택"},
    5: {"name": "오황토성(五黃土星)", "element": "토(土)", "trigram": "중궁(中)", "group": "중앙"},
    6: {"name": "육백금성(六白金星)", "element": "금(金)", "trigram": "건(乾)", "group": "서사택"},
    7: {"name": "칠적금성(七赤金星)", "element": "금(金)", "trigram": "태(兌)", "group": "서사택"},
    8: {"name": "팔백토성(八白土星)", "element": "토(土)", "trigram": "간(艮)", "group": "서사택"},
    9: {"name": "구자화성(九紫火星)", "element": "화(火)", "trigram": "이(離)", "group": "동사택"}
}

# ==========================================
# 2. 팔사택(Eight Mansions) 8대 길흉 방위표
# ==========================================
EIGHT_MANSIONS_DIRECTIONS = {
    1: {"생기": "동남", "천을": "동", "연년": "남", "복위": "북", "화해": "서", "육살": "북서", "오귀": "북동", "절명": "남서"},
    2: {"생기": "북동", "천을": "서", "연년": "북서", "복위": "남서", "화해": "동", "육살": "남", "오귀": "동남", "절명": "북"},
    3: {"생기": "남", "천을": "북", "연년": "동남", "복위": "동", "화해": "남서", "육살": "북동", "오귀": "북서", "절명": "서"},
    4: {"생기": "북", "천을": "남", "연년": "동", "복위": "동남", "화해": "북서", "육살": "서", "오귀": "남서", "절명": "북동"},
    6: {"생기": "서", "천을": "북동", "연년": "남서", "복위": "북서", "화해": "동남", "육살": "북", "오귀": "동", "절명": "남"},
    7: {"생기": "북서", "천을": "남서", "연년": "북동", "복위": "서", "화해": "북", "육살": "동남", "오귀": "남", "절명": "동"},
    8: {"생기": "남서", "천을": "북서", "연년": "서", "복위": "북동", "화해": "남", "육살": "동", "오귀": "북", "절명": "동남"},
    9: {"생기": "동", "천을": "동남", "연년": "북", "복위": "남", "화해": "북동", "육살": "남서", "오귀": "서", "절명": "북서"}
}

# 🚨 [DB 추가] 사용자에게 실질적인 가치를 제공하기 위한 '풍수 행동 지침' 데이터베이스
DIRECTION_ADVICE_DB = {
    "생기": "최상의 길방입니다. 현관문이나 창문을 이 방향으로 내거나, 중요한 업무를 볼 때 이 방향을 바라보고 앉으면 재물과 명예가 크게 상승합니다.",
    "천을": "건강과 치유의 방위입니다. 침대의 머리를 이 방향으로 두면 질병이 낫고 심신이 안정되며 훌륭한 조력자를 만나게 됩니다.",
    "연년": "조화와 인연의 방위입니다. 부부의 침실을 두기에 가장 좋으며, 가정이 화목해지고 안정적인 재물을 모으게 됩니다.",
    "복위": "안정과 평온의 방위입니다. 학생의 책상이나 명상, 휴식 공간으로 적합하며 집중력과 판단력을 크게 높여줍니다.",
    "화해": "가벼운 구설수나 피로가 쌓이는 흉방입니다. 창고나 화장실을 두면 나쁜 기운을 억누를 수 있습니다.",
    "육살": "인간관계의 마찰과 법적 분쟁(관재구설)을 일으키는 흉방입니다. 이 방향으로 머리를 두고 자는 것을 피해야 합니다.",
    "오귀": "화재, 도난, 돌발 사고를 의미하는 독한 흉방입니다. 이 방향에 중요한 물건을 두거나 출입구를 내는 것을 절대 피해야 합니다.",
    "절명": "최악의 흉방으로 기운이 단절됨을 뜻합니다. 가급적 이 공간은 비워두거나 무거운 가구로 억눌러 흉한 기운을 차단하는 것이 좋습니다."
}

class FengShuiEngine:
    def __init__(self):
        pass

    def calculate_honmyeong_gung(self, base_year: int, gender: str) -> dict:
        """
        태어난 연도(입춘 기준)와 성별로 본명궁(1~9) 계산
        """
        # 🚨 [보안 추가] 입력값 타입 검증 및 방어적 캐스팅
        try:
            # base_year에서 숫자만 추출하거나 안전하게 정수로 변환
            clean_year = int("".join(filter(str.isdigit, str(base_year))))
        except ValueError:
            # 변환 실패 시 기본값(예: 1984 갑자년) 부여 또는 에러 핸들링
            clean_year = 1984
            
        # 🚨 [보안 추가] 성별 정규화 (소문자, 공백 등 무력화)
        safe_gender = str(gender).strip().upper() if gender else 'M'
        if safe_gender not in ['M', 'F']:
            safe_gender = 'M'

        # 1. 연도의 각 자리수를 더함
        digit_sum = sum(int(digit) for digit in str(clean_year))
        
        # 2. 한 자리가 될 때까지 다시 더함
        while digit_sum > 9:
            digit_sum = sum(int(digit) for digit in str(digit_sum))
            
        # 3. 남녀에 따른 본명궁 공식 적용
        if safe_gender == 'M':
            # 남성: 11 - digit_sum
            honmyeong_num = 11 - digit_sum
            if honmyeong_num > 9:
                honmyeong_num -= 9
            # 기궁법(특수규칙): 남성 5(오황토성)는 2(이흑토성/곤궁)으로 변환
            if honmyeong_num == 5:
                honmyeong_num = 2
        else: 
            # 여성: digit_sum + 4
            honmyeong_num = digit_sum + 4
            if honmyeong_num > 9:
                honmyeong_num -= 9
            # 기궁법(특수규칙): 여성 5(오황토성)는 8(팔백토성/간궁)으로 변환
            if honmyeong_num == 5:
                honmyeong_num = 8
                
        star_info = NINE_STARS.get(honmyeong_num, NINE_STARS[1]) # 안전장치
        
        return {
            "number": honmyeong_num,
            "name": star_info["name"],
            "element": star_info["element"],
            "trigram": star_info["trigram"],
            "group": star_info["group"]
        }

    def get_auspicious_directions(self, honmyeong_num: int) -> dict:
        """
        본명궁 번호를 기반으로 8대 길흉 방위 반환 (+ 풍수 개운법 추가)
        """
        # 🚨 [보안 추가] 유효하지 않은 타입 차단 및 프론트엔드 UI 렌더링 에러 방지를 위한 빈 틀 반환
        empty_result = {"good": {}, "bad": {}}
        
        try:
            honmyeong_num = int(honmyeong_num)
        except (ValueError, TypeError):
            return empty_result
            
        # 5번은 기궁법에 의해 프론트엔드에서 정상적으로 호출될 일이 없으나 방어 로직 유지
        if honmyeong_num == 5 or honmyeong_num not in EIGHT_MANSIONS_DIRECTIONS:
            return empty_result
            
        directions = EIGHT_MANSIONS_DIRECTIONS.get(honmyeong_num, {})
        
        # 🚨 [기능 추가] 길방과 흉방으로 분류하고, 사용자에게 유용한 풍수 개운법(advice) 결합
        return {
            "good": {
                "생기(최상/활력)": {"direction": directions.get("생기"), "advice": DIRECTION_ADVICE_DB["생기"]},
                "천을(건강/치유)": {"direction": directions.get("천을"), "advice": DIRECTION_ADVICE_DB["천을"]},
                "연년(조화/재물)": {"direction": directions.get("연년"), "advice": DIRECTION_ADVICE_DB["연년"]},
                "복위(안정/휴식)": {"direction": directions.get("복위"), "advice": DIRECTION_ADVICE_DB["복위"]}
            },
            "bad": {
                "화해(구설/다툼)": {"direction": directions.get("화해"), "advice": DIRECTION_ADVICE_DB["화해"]},
                "육살(관재/실패)": {"direction": directions.get("육살"), "advice": DIRECTION_ADVICE_DB["육살"]},
                "오귀(사고/화재)": {"direction": directions.get("오귀"), "advice": DIRECTION_ADVICE_DB["오귀"]},
                "절명(최악/단절)": {"direction": directions.get("절명"), "advice": DIRECTION_ADVICE_DB["절명"]}
            }
        }