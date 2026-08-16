# logic_gunghap.py

# ==========================================
# 1. 구성기학(Nine-Star Ki) 및 팔사택 메타데이터 (보존)
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

DIRECTION_ADVICE_DB = {
    "생기": "최상의 길방입니다. 이 방향으로 출입구를 내거나 머리를 두고 자면 재물과 명예가 크게 상승합니다.",
    "천을": "건강과 치유의 방위입니다. 침대를 이 방향으로 두면 질병이 낫고 훌륭한 귀인(조력자)을 만나게 됩니다.",
    "연년": "조화와 인연의 방위입니다. 부부 침실을 두기에 가장 좋으며, 가정이 화목해지고 안정적인 재물을 모읍니다.",
    "복위": "안정과 평온의 방위입니다. 학생의 책상이나 명상 공간으로 적합하며 집중력을 크게 높여줍니다.",
    "화해": "구설수나 피로가 쌓이는 흉방입니다. 창고나 화장실을 두면 흉한 기운을 억누를 수 있습니다.",
    "육살": "인간관계 마찰과 관재구설을 일으킵니다. 이 방향으로 머리를 두고 자는 것을 절대 피해야 합니다.",
    "오귀": "화재, 돌발 사고를 의미하는 독한 흉방입니다. 중요한 물건을 두거나 출입구를 내는 것을 피해야 합니다.",
    "절명": "최악의 흉방으로 기운이 단절됩니다. 가급적 공간을 비워두거나 무거운 가구로 억눌러 기운을 차단해야 합니다."
}

# ==========================================
# 2. [혼택촬요 업그레이드 DB] 혼택 전용 길흉 데이터베이스
# ==========================================

# 대유년법(大遊年法) 교차 매트릭스 (동서명합)
DAEYUNYEON_MATRIX = {
    1: {1: "복위", 2: "절명", 3: "천을", 4: "생기", 6: "육살", 7: "화해", 8: "오귀", 9: "연년"},
    2: {1: "절명", 2: "복위", 3: "화해", 4: "오귀", 6: "연년", 7: "천을", 8: "생기", 9: "육살"},
    3: {1: "천을", 2: "화해", 3: "복위", 4: "연년", 6: "오귀", 7: "절명", 8: "육살", 9: "생기"},
    4: {1: "생기", 2: "오귀", 3: "연년", 4: "복위", 6: "화해", 7: "육살", 8: "절명", 9: "천을"},
    6: {1: "육살", 2: "연년", 3: "오귀", 4: "화해", 6: "복위", 7: "생기", 8: "천을", 9: "절명"},
    7: {1: "화해", 2: "천을", 3: "절명", 4: "육살", 6: "생기", 7: "복위", 8: "연년", 9: "오귀"},
    8: {1: "오귀", 2: "생기", 3: "육살", 4: "절명", 6: "천을", 7: "연년", 8: "복위", 9: "화해"},
    9: {1: "연년", 2: "육살", 3: "생기", 4: "천을", 6: "절명", 7: "오귀", 8: "화해", 9: "복위"}
}

HONTAEK_GUNGHAP_DB = {
    "생기": {"type": "사길성(四吉星)", "desc": "【대길합】 자손이 번창하고 재물이 크게 일어나는 최고의 궁합입니다. 생명력이 넘치는 천생연분입니다."},
    "천을": {"type": "사길성(四吉星)", "desc": "【길합】 잔병치레가 없고 뜻밖의 귀인이 나타나 위기를 구원해 주는 평안하고 조화로운 궁합입니다."},
    "연년": {"type": "사길성(四吉星)", "desc": "【길합】 부부가 화목하고 수명이 길어 백년해로하는 훌륭한 길합입니다. 인연이 깊고 다정합니다."},
    "복위": {"type": "사길성(四吉星)", "desc": "【길합】 기운이 흩어지지 않고 안정되어 가정이 큰 굴곡 없이 평탄하게 유지되는 무난한 길합입니다."},
    "화해": {"type": "사흉성(四凶星)", "desc": "【흉합】 동서상혼(東西相混)으로 재물이 흩어지고 크고 작은 다툼과 상해를 입기 쉬운 흉합입니다."},
    "육살": {"type": "사흉성(四凶星)", "desc": "【흉합】 음란함, 시비, 관재구설이 발생하기 쉬운 흉합으로, 부부간의 강한 인내와 신뢰가 필요합니다."},
    "오귀": {"type": "사흉성(四凶星)", "desc": "【대흉합】 오귀천궁(五鬼穿宮). 예기치 않은 돌발 재난, 화재, 구설수가 따르는 매우 불안정한 결합입니다."},
    "절명": {"type": "사흉성(四凶星)", "desc": "【대흉합】 자손이 귀해지고 수명이 꺾일 우려가 있는 가장 치명적인 흉합입니다. 강력한 택일(개운법) 비보가 필수적입니다."}
}

# 고진(홀아비) / 과숙(과부) 방합 이탈 로직 맵핑
GOJIN_GWASUK_MAP = {
    "수": {"branches": ["亥", "子", "丑"], "gojin": "寅", "gwasuk": "戌"},
    "목": {"branches": ["寅", "卯", "辰"], "gojin": "巳", "gwasuk": "丑"},
    "화": {"branches": ["巳", "午", "未"], "gojin": "申", "gwasuk": "辰"},
    "금": {"branches": ["申", "酉", "戌"], "gojin": "亥", "gwasuk": "未"}
}

# [혼택촬요 제3부 용월법] 신부 띠 기준 길월/흉월 표 (음력 기준)
GACHWI_GILWOL_DB = {
    "子": {"대리월": [6, 12], "소리월": [1, 7], "방녀부모": [2, 8], "방부": [3, 9], "방옹고": [4, 10], "방녀": [5, 11]},
    "丑": {"대리월": [5, 11], "소리월": [4, 10], "방녀부모": [3, 9], "방부": [2, 8], "방옹고": [1, 7], "방녀": [6, 12]},
    "寅": {"대리월": [2, 8], "소리월": [3, 9], "방녀부모": [4, 10], "방부": [5, 11], "방옹고": [6, 12], "방녀": [1, 7]},
    "卯": {"대리월": [1, 7], "소리월": [6, 12], "방녀부모": [5, 11], "방부": [4, 10], "방옹고": [3, 9], "방녀": [2, 8]},
    "辰": {"대리월": [4, 10], "소리월": [5, 11], "방녀부모": [6, 12], "방부": [1, 7], "방옹고": [2, 8], "방녀": [3, 9]},
    "巳": {"대리월": [3, 9], "소리월": [2, 8], "방녀부모": [1, 7], "방부": [6, 12], "방옹고": [5, 11], "방녀": [4, 10]},
    "午": {"대리월": [6, 12], "소리월": [1, 7], "방녀부모": [2, 8], "방부": [3, 9], "방옹고": [4, 10], "방녀": [5, 11]},
    "未": {"대리월": [5, 11], "소리월": [4, 10], "방녀부모": [3, 9], "방부": [2, 8], "방옹고": [1, 7], "방녀": [6, 12]},
    "申": {"대리월": [2, 8], "소리월": [3, 9], "방녀부모": [4, 10], "방부": [5, 11], "방옹고": [6, 12], "방녀": [1, 7]},
    "酉": {"대리월": [1, 7], "소리월": [6, 12], "방녀부모": [5, 11], "방부": [4, 10], "방옹고": [3, 9], "방녀": [2, 8]},
    "戌": {"대리월": [4, 10], "소리월": [5, 11], "방녀부모": [6, 12], "방부": [1, 7], "방옹고": [2, 8], "방녀": [3, 9]},
    "亥": {"대리월": [3, 9], "소리월": [2, 8], "방녀부모": [1, 7], "방부": [6, 12], "방옹고": [5, 11], "방녀": [4, 10]}
}

# [혼택촬요 제2부 특수 격국] 심층 텍스트 DB
HONTAEK_SPECIAL_DB = {
    "천지합덕": {"hanja": "天地合德格", "desc": "하늘(천간)과 땅(지지)이 완벽히 화합하는 구조. 정신과 육체, 안과 밖이 빈틈없이 결합하는 궁합 최고의 대길상(大吉相)입니다."},
    "교귀격": {"hanja": "交貴格", "desc": "남녀가 서로의 귀인(천을귀인)을 교환하는 특별한 명리 구조. 흉함을 덮고 서로의 사회적 성취를 크게 끌어올려 줍니다."},
    "교록격": {"hanja": "交祿格", "desc": "남녀가 서로의 사주에서 튼튼한 복록(건록)을 상호 교환하는 대길격. 결혼 후 재물이 폭발적으로 일어나고 부귀쌍전합니다."},
    "상문공망": {"hanja": "喪門空亡", "desc": "상실을 뜻하는 상문살과 텅 비어버리는 공망이 겹친 치명적인 흉상. 다른 조건이 아무리 좋아도 절대 혼례일로 쓰지 말아야 할 금기입니다."},
    "단명살": {"hanja": "短命煞", "desc": "목숨이 짧게 끊어지는 치명적인 흉살. 부부 중 한 명이 생리사별의 비극을 겪을 수 있어 택일 시 완벽히 배제해야 합니다."}
}


class FengShuiHontaekEngine:
    def __init__(self):
        # 간합, 지합 판별
        self.cheon_hap = [{"甲", "己"}, {"乙", "庚"}, {"丙", "辛"}, {"丁", "壬"}, {"戊", "癸"}]
        self.ji_hap = [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
        
        # 교귀격(천을귀인 교환) / 교록격(건록 교환) 기준표
        self.gwiin_map = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        self.geonrok_map = {"甲":"寅", "乙":"卯", "丙":"巳", "戊":"巳", "丁":"午", "己":"午", "庚":"申", "辛":"酉", "壬":"亥", "癸":"子"}

    # 🚨 [보안 적용] 안전한 타입 캐스팅 헬퍼 메서드
    def _safe_str(self, val) -> str:
        return str(val).strip() if val else ""

    def _safe_int(self, val, default=1984) -> int:
        try:
            clean_str = "".join(filter(str.isdigit, str(val)))
            return int(clean_str) if clean_str else default
        except (ValueError, TypeError):
            return default

    def calculate_honmyeong_gung(self, base_year: int, gender: str) -> dict:
        """태어난 연도(입춘 기준)와 성별로 본명궁(1~9) 안전 계산"""
        clean_year = self._safe_int(base_year)
            
        safe_gender = self._safe_str(gender).upper()
        if safe_gender not in ['M', 'F']: safe_gender = 'M'

        digit_sum = sum(int(digit) for digit in str(clean_year))
        while digit_sum > 9:
            digit_sum = sum(int(digit) for digit in str(digit_sum))
            
        # 남곤여간(男坤女艮) 기궁법 적용
        if safe_gender == 'M':
            honmyeong_num = 11 - digit_sum
            if honmyeong_num > 9: honmyeong_num -= 9
            if honmyeong_num == 5: honmyeong_num = 2
        else: 
            honmyeong_num = digit_sum + 4
            if honmyeong_num > 9: honmyeong_num -= 9
            if honmyeong_num == 5: honmyeong_num = 8
                
        star_info = NINE_STARS.get(honmyeong_num, NINE_STARS[1])
        
        return {
            "number": honmyeong_num,
            "name": star_info["name"],
            "element": star_info["element"],
            "trigram": star_info["trigram"],
            "group": star_info["group"]
        }

    def get_auspicious_directions(self, honmyeong_num: int) -> dict:
        """본명궁 번호 기반 8대 길흉 방위 반환 (+ 풍수 개운법)"""
        empty_result = {"good": {}, "bad": {}}
        h_num = self._safe_int(honmyeong_num, default=0)
            
        if h_num == 5 or h_num not in EIGHT_MANSIONS_DIRECTIONS:
            return empty_result
            
        dirs = EIGHT_MANSIONS_DIRECTIONS.get(h_num, {})
        
        return {
            "good": {
                "생기": {"dir": dirs.get("생기"), "advice": DIRECTION_ADVICE_DB.get("생기", "")},
                "천을": {"dir": dirs.get("천을"), "advice": DIRECTION_ADVICE_DB.get("천을", "")},
                "연년": {"dir": dirs.get("연년"), "advice": DIRECTION_ADVICE_DB.get("연년", "")},
                "복위": {"dir": dirs.get("복위"), "advice": DIRECTION_ADVICE_DB.get("복위", "")}
            },
            "bad": {
                "화해": {"dir": dirs.get("화해"), "advice": DIRECTION_ADVICE_DB.get("화해", "")},
                "육살": {"dir": dirs.get("육살"), "advice": DIRECTION_ADVICE_DB.get("육살", "")},
                "오귀": {"dir": dirs.get("오귀"), "advice": DIRECTION_ADVICE_DB.get("오귀", "")},
                "절명": {"dir": dirs.get("절명"), "advice": DIRECTION_ADVICE_DB.get("절명", "")}
            }
        }

    def evaluate_hontaek_gunghap(self, m_year: int, f_year: int) -> dict:
        """[혼택 제7장 동서명합길흉] 대유년법 매트릭스를 통한 최종 8유성 궁합 판별"""
        result = {"status": "error", "star": "알 수 없음", "type": "-", "desc": "연산 오류"}
        
        m_num = self.calculate_honmyeong_gung(m_year, 'M').get("number")
        f_num = self.calculate_honmyeong_gung(f_year, 'F').get("number")
        
        if not m_num or not f_num: return result
            
        matched_star = DAEYUNYEON_MATRIX.get(m_num, {}).get(f_num)
        
        if matched_star:
            interpretation = HONTAEK_GUNGHAP_DB.get(matched_star, {})
            result = {
                "status": "success",
                "star": matched_star,
                "type": interpretation.get("type", ""),
                "desc": interpretation.get("desc", "")
            }
        return result

    def get_gachwi_gilwol(self, f_year_branch: str) -> dict:
        """[혼택 제4장 용월법] 신부의 띠를 기준으로 혼인하기 좋은 달(가취길월) 판별"""
        f_b = self._safe_str(f_year_branch)
        if not f_b or f_b not in GACHWI_GILWOL_DB:
            return {"status": "error", "message": "신부의 띠 정보가 누락되었습니다."}

        data = GACHWI_GILWOL_DB[f_b]
        return {
            "status": "success",
            "best_months": data["대리월"],
            "good_months": data["소리월"],
            "warning": "대리월(大利月)과 소리월(小利月) 내에서 택일하는 것이 혼택촬요의 제1원칙입니다.",
            "forbidden": {"신부부모흉": data["방녀부모"], "시부모흉": data["방옹고"], "신랑흉": data["방부"], "신부흉": data["방녀"]}
        }

    def check_taekil_gojin_gwasuk(self, m_branch: str, f_branch: str, target_day_branch: str) -> dict:
        """[혼택 제5,6장 개정고진/과숙] 택일일의 홀아비/과부살 흉액 필터"""
        m_b = self._safe_str(m_branch)
        f_b = self._safe_str(f_branch)
        t_b = self._safe_str(target_day_branch)
        
        result = {"is_banned": False, "reason": "사용 가능한 무난한 날짜입니다."}
        if not t_b: return result

        # 고진살(신랑 기준) 체크
        for group in GOJIN_GWASUK_MAP.values():
            if m_b in group["branches"] and t_b == group["gojin"]:
                return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신랑({m_b}띠)에게 고진살(孤辰殺, 홀아비살)입니다. 절대 배제하십시오."}
            
        # 과숙살(신부 기준) 체크
        for group in GOJIN_GWASUK_MAP.values():
            if f_b in group["branches"] and t_b == group["gwasuk"]:
                return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신부({f_b}띠)에게 과숙살(寡宿殺, 상부살)입니다. 절대 배제하십시오."}
            
        return result

    def analyze_special_gunghap(self, m_day_stem: str, m_day_branch: str, f_day_stem: str, f_day_branch: str) -> list:
        """
        [혼택 특수격국 분석] 천지합덕격, 교귀격, 교록격 등 대길(大吉) 구조 스캐너
        """
        m_ds, m_db = self._safe_str(m_day_stem), self._safe_str(m_day_branch)
        f_ds, f_db = self._safe_str(f_day_stem), self._safe_str(f_day_branch)
        results = []
        
        if not m_ds or not m_db or not f_ds or not f_db:
            return results

        # 1. 천지합덕격 (천간합 + 지지합)
        stem_pair = {m_ds, f_ds}
        branch_pair = {m_db, f_db}
        is_cheon_hap = stem_pair in self.cheon_hap
        is_ji_hap = branch_pair in self.ji_hap

        if is_cheon_hap and is_ji_hap:
            results.append({"name": "천지합덕격", "desc": HONTAEK_SPECIAL_DB["천지합덕"]["desc"]})
        else:
            if is_cheon_hap: results.append({"name": "간합", "desc": "천간이 합을 이루어 부부간 정신적 교감과 뜻의 일치가 매우 깊습니다."})
            if is_ji_hap: results.append({"name": "지합", "desc": "지지가 합을 이루어 속궁합과 현실적인 생활 패턴이 완벽하게 융화됩니다."})

        # 2. 교귀격 (서로의 천을귀인 교환)
        m_gives_gwiin = m_db in self.gwiin_map.get(f_ds, [])
        f_gives_gwiin = f_db in self.gwiin_map.get(m_ds, [])
        if m_gives_gwiin and f_gives_gwiin:
            results.append({"name": "교귀격", "desc": HONTAEK_SPECIAL_DB["교귀격"]["desc"]})

        # 3. 교록격 (서로의 건록 교환)
        m_gives_rok = m_db == self.geonrok_map.get(f_ds)
        f_gives_rok = f_db == self.geonrok_map.get(m_ds)
        if m_gives_rok and f_gives_rok:
            results.append({"name": "교록격", "desc": HONTAEK_SPECIAL_DB["교록격"]["desc"]})

        return results