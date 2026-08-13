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
# 길방: 생기(최상), 천을(건강/치유), 연년(조화/재물), 복위(안정)
# 흉방: 화해(가벼운 다툼), 육살(구설수), 오귀(화재/사고), 절명(최악/단절)
# ==========================================
EIGHT_MANSIONS_DIRECTIONS = {
    # 1. 감궁 (동사택)
    1: {"생기": "동남", "천을": "동", "연년": "남", "복위": "북", "화해": "서", "육살": "북서", "오귀": "북동", "절명": "남서"},
    # 2. 곤궁 (서사택)
    2: {"생기": "북동", "천을": "서", "연년": "북서", "복위": "남서", "화해": "동", "육살": "남", "오귀": "동남", "절명": "북"},
    # 3. 진궁 (동사택)
    3: {"생기": "남", "천을": "북", "연년": "동남", "복위": "동", "화해": "남서", "육살": "북동", "오귀": "북서", "절명": "서"},
    # 4. 손궁 (동사택)
    4: {"생기": "북", "천을": "남", "연년": "동", "복위": "동남", "화해": "북서", "육살": "서", "오귀": "남서", "절명": "북동"},
    # 6. 건궁 (서사택)
    6: {"생기": "서", "천을": "북동", "연년": "남서", "복위": "북서", "화해": "동남", "육살": "북", "오귀": "동", "절명": "남"},
    # 7. 태궁 (서사택)
    7: {"생기": "북서", "천을": "남서", "연년": "북동", "복위": "서", "화해": "북", "육살": "동남", "오귀": "남", "절명": "동"},
    # 8. 간궁 (서사택)
    8: {"생기": "남서", "천을": "북서", "연년": "서", "복위": "북동", "화해": "남", "육살": "동", "오귀": "북", "절명": "동남"},
    # 9. 이궁 (동사택)
    9: {"생기": "동", "천을": "동남", "연년": "북", "복위": "남", "화해": "북동", "육살": "남서", "오귀": "서", "절명": "북서"}
}

class FengShuiEngine:
    def __init__(self):
        pass

    def calculate_honmyeong_gung(self, base_year: int, gender: str) -> dict:
        """
        태어난 연도(입춘 기준)와 성별로 본명궁(1~9) 계산
        """
        # 1. 연도의 각 자리수를 더함 (예: 1990 -> 1+9+9+0 = 19)
        digit_sum = sum(int(digit) for digit in str(base_year))
        
        # 2. 한 자리가 될 때까지 다시 더함 (예: 19 -> 1+9 = 10 -> 1+0 = 1)
        while digit_sum > 9:
            digit_sum = sum(int(digit) for digit in str(digit_sum))
            
        # 3. 남녀에 따른 본명궁 공식 적용
        if gender == 'M':
            # 남성: 11 - digit_sum
            honmyeong_num = 11 - digit_sum
            if honmyeong_num > 9:
                honmyeong_num -= 9
            # 기궁법(특수규칙): 남성 5(오황토성)는 2(이흑토성/곤궁)으로 변환
            if honmyeong_num == 5:
                honmyeong_num = 2
        else: # 'F'
            # 여성: digit_sum + 4
            honmyeong_num = digit_sum + 4
            if honmyeong_num > 9:
                honmyeong_num -= 9
            # 기궁법(특수규칙): 여성 5(오황토성)는 8(팔백토성/간궁)으로 변환
            if honmyeong_num == 5:
                honmyeong_num = 8
                
        star_info = NINE_STARS[honmyeong_num]
        
        return {
            "number": honmyeong_num,
            "name": star_info["name"],
            "element": star_info["element"],
            "trigram": star_info["trigram"],
            "group": star_info["group"]
        }

    def get_auspicious_directions(self, honmyeong_num: int) -> dict:
        """
        본명궁 번호를 기반으로 8대 길흉 방위 반환
        """
        # 특수규칙 처리
        if honmyeong_num == 5:
            return {} 
            
        directions = EIGHT_MANSIONS_DIRECTIONS.get(honmyeong_num, {})
        
        # 길방과 흉방으로 분류하여 정리
        return {
            "good": {
                "생기(최상/활력)": directions.get("생기"),
                "천을(건강/치유)": directions.get("천을"),
                "연년(조화/재물)": directions.get("연년"),
                "복위(안정/휴식)": directions.get("복위")
            },
            "bad": {
                "화해(구설/다툼)": directions.get("화해"),
                "육살(관재/실패)": directions.get("육살"),
                "오귀(사고/화재)": directions.get("오귀"),
                "절명(최악/단절)": directions.get("절명")
            }
        }