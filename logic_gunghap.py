# ==========================================
# 1. 구성기학(Nine-Star Ki) 및 팔사택 메타데이터
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
# 2. 혼택 전용 길흉 데이터베이스
# ==========================================
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

GOJIN_GWASUK_MAP = {
    "수": {"branches": ["亥", "子", "丑"], "gojin": "寅", "gwasuk": "戌"},
    "목": {"branches": ["寅", "卯", "辰"], "gojin": "巳", "gwasuk": "丑"},
    "화": {"branches": ["巳", "午", "未"], "gojin": "申", "gwasuk": "辰"},
    "금": {"branches": ["申", "酉", "戌"], "gojin": "亥", "gwasuk": "未"}
}

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

HONTAEK_SPECIAL_DB = {
    "천지합덕": {"hanja": "天地合德格", "desc": "하늘(천간)과 땅(지지)이 완벽히 화합하는 구조. 정신과 육체, 안과 밖이 빈틈없이 결합하는 궁합 최고의 대길상(大吉相)입니다."},
    "교귀격": {"hanja": "交貴格", "desc": "남녀가 서로의 귀인(천을귀인)을 교환하는 특별한 명리 구조. 흉함을 덮고 서로의 사회적 성취를 크게 끌어올려 줍니다."},
    "교록격": {"hanja": "交祿格", "desc": "남녀가 서로의 사주에서 튼튼한 복록(건록)을 상호 교환하는 대길격. 결혼 후 재물이 폭발적으로 일어나고 부귀쌍전합니다."}
}

class FengShuiHontaekEngine:
    def __init__(self):
        self.cheon_hap = [{"甲", "己"}, {"乙", "庚"}, {"丙", "辛"}, {"丁", "壬"}, {"戊", "癸"}]
        self.ji_hap = [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
        self.gwiin_map = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        self.geonrok_map = {"甲":"寅", "乙":"卯", "丙":"巳", "戊":"巳", "丁":"午", "己":"午", "庚":"申", "辛":"酉", "壬":"亥", "癸":"子"}

    def _safe_str(self, val) -> str: return str(val).strip() if val else ""
    def _safe_int(self, val, default=1984) -> int:
        try:
            clean_str = "".join(filter(str.isdigit, str(val)))
            return int(clean_str) if clean_str else default
        except (ValueError, TypeError): return default

    def calculate_honmyeong_gung(self, base_year: int, gender: str) -> dict:
        clean_year = self._safe_int(base_year)
        safe_gender = self._safe_str(gender).upper()
        if safe_gender not in ['M', 'F']: safe_gender = 'M'
        digit_sum = sum(int(digit) for digit in str(clean_year))
        while digit_sum > 9:
            digit_sum = sum(int(digit) for digit in str(digit_sum))
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

    # 🚨 실수로 누락되었던 8사택 방위 계산 함수 완벽 복구
    def get_auspicious_directions(self, honmyeong_num: int) -> dict:
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

    def _get_element_desc(self, el_pure: str) -> str:
        descs = {
            "목": "유연하고 뻗어나가는 목(木, 나무)의 에너지",
            "화": "뜨겁고 맹렬하게 타오르는 화(火, 불)의 에너지",
            "토": "만물을 포용하고 중재하는 토(土, 흙)의 에너지",
            "금": "강하고 단단한 금(金, 쇠)의 에너지",
            "수": "깊고 유연하게 스며드는 수(水, 물)의 에너지"
        }
        return descs.get(el_pure, "")

    def _analyze_element_relation(self, m_el: str, f_el: str) -> dict:
        """[핵심] 오행의 생극제화를 분석하여 딥 리포트용 텍스트를 자동 생성합니다."""
        el_map = {"목": 0, "화": 1, "토": 2, "금": 3, "수": 4}
        hanja_map = {"목": "木", "화": "火", "토": "土", "금": "金", "수": "水"}
        m_idx = el_map.get(m_el, 0)
        f_idx = el_map.get(f_el, 0)
        
        rel_type = ""
        title = ""
        desc = ""
        m_stance = ""
        f_stance = ""

        if m_idx == f_idx:
            rel_type = "비화"
            title = f"오행의 든든한 동질성 ({m_el}비화, {hanja_map[m_el]}比和)"
            desc = f"두 분은 같은 {m_el}의 에너지를 지녀 서로가 서로를 거울처럼 비추고 든든하게 지지해 주는 관계입니다."
            m_stance = "권위의식 없이 아내와 눈높이를 맞추며 평등하고 편안한 관계를 유지합니다."
            f_stance = "남편이라기보다 동등한 친구나 든든한 동료처럼 깊은 편안함을 느낍니다."
        elif f_idx == (m_idx + 1) % 5:
            rel_type = "남생여"
            title = f"오행의 이타적인 상생 작용 ({m_el}생{f_el}, {hanja_map[m_el]}生{hanja_map[f_el]})"
            desc = f"남성의 {m_el} 기운이 여성의 {f_el} 기운을 끊임없이 보살피고 키워주는 헌신적인 상생(相生) 관계입니다."
            m_stance = "아내를 위해 헌신하고 조건 없이 내어주는 것에 큰 기쁨과 보람을 느낍니다."
            f_stance = "남편의 전폭적인 지지와 희생 덕분에 정서적으로 완벽한 편안함과 안정감을 느낍니다."
        elif m_idx == (f_idx + 1) % 5:
            rel_type = "여생남"
            title = f"오행의 이타적인 상생 작용 ({f_el}생{m_el}, {hanja_map[f_el]}生{hanja_map[m_el]})"
            desc = f"여성의 {f_el} 기운이 남성의 {m_el} 기운을 끊임없이 보살피고 키워주는 내조의 상생(相生) 관계입니다."
            m_stance = "아내의 헌신적인 내조와 지지 덕분에 밖에서 사회적 능력을 마음껏 펼칠 수 있습니다."
            f_stance = "남편을 보살피고 뒷바라지하는 것에 보람을 느끼며, 가정의 든든한 뿌리 역할을 합니다."
        elif f_idx == (m_idx + 2) % 5:
            rel_type = "남극여"
            title = f"오행의 치명적인 상극 작용 ({m_el}극{f_el}, {hanja_map[m_el]}克{hanja_map[f_el]})"
            desc = f"두 분이 가진 에너지의 본질이 서로를 파괴하는 상극(相剋) 관계에 놓여 있습니다. 자연의 이치상 도끼({m_el})가 나무({f_el})를 치는 '{m_el}극{f_el}'의 현상이 발생합니다."
            m_stance = "본인은 그럴 의도가 없더라도 결과적으로 여성의 에너지를 꺾고 일방적으로 통제하는 형태가 되어버립니다. 기운이 매끄럽게 순환하지 못해 남성 역시 피로감을 느낍니다."
            f_stance = "남성의 강한 기운과 성향에 심리적, 육체적으로 지속적인 억압을 받게 됩니다. 본인의 능력을 마음껏 펼치지 못하고 답답함을 느끼며 위축됩니다."
        elif m_idx == (f_idx + 2) % 5:
            rel_type = "여극남"
            title = f"오행의 치명적인 상극 작용 ({f_el}극{m_el}, {hanja_map[f_el]}克{hanja_map[m_el]})"
            desc = f"두 분이 가진 에너지의 본질이 서로를 파괴하는 상극(相剋) 관계에 놓여 있습니다. 자연의 이치상 도끼({f_el})가 나무({m_el})를 치는 '{f_el}극{m_el}'의 현상이 발생합니다."
            m_stance = "여성의 강한 주관과 기운에 심리적으로 억압을 받으며, 집 안에서 안식을 찾기 어렵고 기가 눌려 무기력해지기 쉽습니다."
            f_stance = "본인은 그럴 의도가 없더라도 남편의 행동이 성에 차지 않아 끊임없이 통제하려 들며, 이로 인해 스스로도 피로와 예민함을 느낍니다."

        return {"title": title, "desc": desc, "m_stance": m_stance, "f_stance": f_stance, "is_clash": "극" in rel_type}

    def evaluate_hontaek_gunghap(self, m_year: int, f_year: int, m_name: str = "신랑", f_name: str = "신부") -> dict:
        """🚨 [핵심 업데이트] 동서명합 딥 리포트(Deep Report) 자동 생성 엔진"""
        result = {"status": "error", "star": "알 수 없음", "type": "-", "desc": "연산 오류"}
        m_gung = self.calculate_honmyeong_gung(m_year, 'M')
        f_gung = self.calculate_honmyeong_gung(f_year, 'F')
        m_num = m_gung.get("number")
        f_num = f_gung.get("number")
        if not m_num or not f_num: return result
        
        matched_star = DAEYUNYEON_MATRIX.get(m_num, {}).get(f_num)
        if matched_star:
            interpretation = HONTAEK_GUNGHAP_DB.get(matched_star, {})
            
            # 딥 리포트 로직 가동
            m_group = m_gung['group']
            f_group = f_gung['group']
            is_match = (m_group == f_group)
            
            m_el_pure = m_gung['element'].split('(')[0]
            f_el_pure = f_gung['element'].split('(')[0]

            # 이유 1: 주파수
            if is_match:
                freq_title = f"1. 생체 주파수와 공간 에너지의 완벽한 조화 ({m_group} 결합)"
                freq_desc = f"두 분은 '{m_group}'이라는 동일한 주파수 대역을 수신합니다. 결혼이나 동거를 통해 한 공간에 살게 될 경우, 침대의 방향이나 현관문의 위치 등 공간의 에너지가 두 사람 모두에게 건강과 재물을 증폭시켜주는 강력한 시너지 구조가 형성됩니다."
            else:
                freq_title = "1. 생체 주파수와 공간 에너지의 정반대 대립 (동사택 vs 서사택)"
                freq_desc = "동사택과 서사택은 마치 'AM 라디오와 FM 라디오'처럼 수신하는 주파수 대역이 완전히 다릅니다. 한 공간에 살게 되면 심각한 모순이 발생하여, 한쪽을 반드시 희생시키거나 기를 빨아먹는 구조가 되므로 장기적으로 원인 모를 컨디션 난조나 무기력증에 시달리게 됩니다."

            # 이유 2: 오행 분석
            rel_data = self._analyze_element_relation(m_el_pure, f_el_pure)
            
            # 이유 3: 팔택명경
            star_title = f"3. 팔택명경(八宅明鏡)상 '{matched_star}' 에너지의 형성"
            if is_match:
                star_desc = f"역학적으로 '{matched_star}'라는 훌륭한 에너지가 생성됩니다. 소통의 주파수가 맞아 대화의 핀트가 정확히 일치하며, 사소한 오해 없이 서로를 향한 깊은 신뢰와 화합을 주관하는 든든한 뼈대가 됩니다."
            else:
                star_desc = f"역학적으로 '{matched_star}'라는 흉한 에너지가 생성됩니다. '{matched_star}'란 재앙과 피해를 의미하며 소통의 단절을 주관합니다. 가치관과 삶의 템포가 달라 대화의 핀트가 자꾸 엇나가며, 서로 좋은 의도로 한 행동조차 상대방에게는 간섭이나 스트레스로 곡해되어 전달되는 빈도가 매우 높습니다."

            # 발현 양상 (Manifestations)
            manifestations = []
            if is_match and not rel_data["is_clash"]:
                manifestations.append({"title": "\"함께 있을수록 에너지가 충전된다\"", "desc": "함께 시간을 보내고 같은 공간에서 잠을 잘 때, 서로의 기운이 톱니바퀴처럼 맞물려 방전된 체력이 빠르게 회복되는 느낌을 받게 됩니다."})
                manifestations.append({"title": "\"가까워질수록 서로의 능력을 키워준다\"", "desc": f"오행의 조화({m_el_pure}-{f_el_pure})로 인해, 대화를 나눌수록 막혀있던 아이디어가 떠오르고 사회적 성취를 크게 끌어올려 줍니다."})
                manifestations.append({"title": "결정적 순간의 가치관 일치", "desc": "주거지 이동이나 금전 문제 등 중요한 결정을 내릴 때, 서로 바라보는 길흉의 체계가 같아 갈등 없이 평탄하게 뜻을 모을 수 있습니다."})
                conclusion = "명리학과 풍수지리적 관점에서 볼 때, 두 분의 결합은 톱니바퀴가 완벽하게 맞물려 돌아가는 최상의 구조입니다. 서로가 서로의 결핍을 채워주고 공간의 에너지를 온전히 흡수할 수 있으니, 의구심을 가질 필요 없이 득(得)이 넘쳐나는 완벽한 천생연분임이 분명합니다."
            else:
                manifestations.append({"title": "\"함께 있을수록 이유 없이 피곤하다\"", "desc": "함께 시간을 보내고 같은 공간에서 잠을 자는데도 에너지가 충전되는 것이 아니라 서로 방전되는 느낌을 받게 됩니다."})
                if rel_data["is_clash"]:
                    manifestations.append({"title": "\"가까워질수록 상처를 준다\"", "desc": f"{rel_data['title'].split(' ')[-1]}의 형국이므로, 무심코 뱉은 말이나 행동이 날카로운 비수처럼 꽂혀 지울 수 없는 상처가 되기 쉽습니다."})
                else:
                    manifestations.append({"title": "\"채워지지 않는 공허함\"", "desc": "겉으로는 다투지 않더라도, 근본적인 에너지의 방향성이 달라 마음 한구석에 늘 채워지지 않는 외로움과 공허함이 자리 잡기 쉽습니다."})
                manifestations.append({"title": "결정적 순간의 가치관 충돌", "desc": "주거지 이동, 금전 문제 등 중요한 결정을 내릴 때, 서로 바라보는 방향(길흉의 체계)이 정반대이므로 끝없는 평행선을 달리게 됩니다."})
                conclusion = "명리학과 풍수지리적 관점에서 볼 때, 두 분의 결합은 톱니바퀴의 규격이 달라 맞물려 돌아갈수록 마모가 심해지는 구조입니다. 어느 한쪽이 나빠서가 아니라, 타고난 에너지의 설계도 자체가 서로를 밀어내고 극(剋)하는 방향으로 세팅되어 있기 때문입니다. 의구심을 가질 필요 없이, 역학적 원리상 서로에게 득보다 실이 많은 인연임이 분명하게 나타납니다."

            deep_report = {
                "groom_profile": {
                    "name": f"{m_name} 님 ({m_year}년생 남성)",
                    "gung": f"{m_gung['trigram']}궁",
                    "group": m_gung['group'],
                    "element_desc": self._get_element_desc(m_el_pure)
                },
                "bride_profile": {
                    "name": f"{f_name} 님 ({f_year}년생 여성)",
                    "gung": f"{f_gung['trigram']}궁",
                    "group": f_gung['group'],
                    "element_desc": self._get_element_desc(f_el_pure)
                },
                "is_good": (is_match and not rel_data["is_clash"]),
                "reasons": [
                    {"title": freq_title, "desc": freq_desc},
                    {"title": rel_data['title'], "desc": rel_data['desc'], "m_stance": rel_data['m_stance'], "f_stance": rel_data['f_stance']},
                    {"title": star_title, "desc": star_desc}
                ],
                "manifestations": manifestations,
                "conclusion": conclusion
            }

            result = {
                "status": "success",
                "star": matched_star,
                "type": interpretation.get("type", ""),
                "desc": interpretation.get("desc", ""),
                "deep_report": deep_report # 🚨 프론트로 발송되는 딥 리포트 객체
            }
        return result

    def get_gachwi_gilwol(self, f_year_branch: str) -> dict:
        f_b = self._safe_str(f_year_branch)
        if not f_b or f_b not in GACHWI_GILWOL_DB: return {"status": "error", "message": "누락"}
        data = GACHWI_GILWOL_DB[f_b]
        return {"status": "success", "best_months": data["대리월"], "good_months": data["소리월"], "warning": "대리월(大利月)과 소리월(小利月) 내에서 택일하는 것이 혼택촬요의 제1원칙입니다.", "forbidden": {"신부부모흉": data["방녀부모"], "시부모흉": data["방옹고"], "신랑흉": data["방부"], "신부흉": data["방녀"]}}

    def check_taekil_gojin_gwasuk(self, m_branch: str, f_branch: str, target_day_branch: str) -> dict:
        m_b, f_b, t_b = self._safe_str(m_branch), self._safe_str(f_branch), self._safe_str(target_day_branch)
        result = {"is_banned": False, "reason": "사용 가능한 무난한 날짜입니다."}
        if not t_b: return result
        for group in GOJIN_GWASUK_MAP.values():
            if m_b in group["branches"] and t_b == group["gojin"]: return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신랑({m_b}띠)에게 고진살(孤辰殺, 홀아비살)입니다. 절대 배제하십시오."}
            if f_b in group["branches"] and t_b == group["gwasuk"]: return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신부({f_b}띠)에게 과숙살(寡宿殺, 상부살)입니다. 절대 배제하십시오."}
        return result

    def analyze_special_gunghap(self, m_day_stem: str, m_day_branch: str, f_day_stem: str, f_day_branch: str) -> list:
        m_ds, m_db = self._safe_str(m_day_stem), self._safe_str(m_day_branch)
        f_ds, f_db = self._safe_str(f_day_stem), self._safe_str(f_day_branch)
        results = []
        if not m_ds or not m_db or not f_ds or not f_db: return results
        is_cheon_hap = {m_ds, f_ds} in self.cheon_hap
        is_ji_hap = {m_db, f_db} in self.ji_hap
        if is_cheon_hap and is_ji_hap: results.append({"name": "천지합덕격", "desc": HONTAEK_SPECIAL_DB["천지합덕"]["desc"]})
        else:
            if is_cheon_hap: results.append({"name": "간합", "desc": "천간이 합을 이루어 부부간 정신적 교감과 뜻의 일치가 매우 깊습니다."})
            if is_ji_hap: results.append({"name": "지합", "desc": "지지가 합을 이루어 속궁합과 현실적인 생활 패턴이 완벽하게 융화됩니다."})
        if m_db in self.gwiin_map.get(f_ds, []) and f_db in self.gwiin_map.get(m_ds, []): results.append({"name": "교귀격", "desc": HONTAEK_SPECIAL_DB["교귀격"]["desc"]})
        if m_db == self.geonrok_map.get(f_ds) and f_db == self.geonrok_map.get(m_ds): results.append({"name": "교록격", "desc": HONTAEK_SPECIAL_DB["교록격"]["desc"]})
        return results

# ==========================================
# 🌟 이상형 자동 매칭 엔진 (기존 보존)
# ==========================================
class IdealPartnerEngine:
    def __init__(self, hontaek_engine: FengShuiHontaekEngine):
        self.hontaek = hontaek_engine
        self.samhap = {
            "申":["子","辰"], "子":["申","辰"], "辰":["申","子"],
            "亥":["卯","未"], "卯":["亥","未"], "未":["亥","卯"],
            "寅":["午","戌"], "午":["寅","戌"], "戌":["寅","午"],
            "巳":["酉","丑"], "酉":["巳","丑"], "丑":["巳","酉"]
        }
        self.wonjin = {"子":"未", "丑":"午", "寅":"酉", "卯":"申", "辰":"亥", "巳":"戌", "午":"丑", "未":"子", "申":"卯", "酉":"寅", "戌":"巳", "亥":"辰"}
        self.chung = {"子":"午", "丑":"未", "寅":"申", "卯":"酉", "辰":"戌", "巳":"亥", "午":"子", "未":"丑", "申":"寅", "酉":"卯", "戌":"辰", "亥":"巳"}
        self.tg_ideal_desc = {
            "비견": "당신은 누군가에게 일방적으로 억압받는 것을 견디지 못합니다. 친구처럼 동등하게 취미를 공유하고, 주도권 다툼 없이 서로의 영역과 독립성을 존중해 주는 편안한 동반자를 만나야 숨이 트입니다.",
            "겁재": "조용하고 평탄하기만 한 관계는 당신을 지루하게 만듭니다. 강한 주관과 승부욕을 갖추어 나를 끊임없이 자극하고 이끌어주며 긍정적인 경쟁 시너지를 내는 열정적인 파트너가 제격입니다.",
            "식신": "당신은 따뜻한 온기와 정서적 교감을 중시합니다. 다정다감한 성품으로 조건 없는 헌신과 사랑을 주며, 요리와 식도락을 함께 즐기며 일상의 행복을 누릴 수 있는 따뜻한 배우자가 완벽합니다.",
            "상관": "틀에 박힌 권위주의나 잔소리는 당신의 매력을 죽입니다. 재치와 유머 감각이 뛰어나며, 통통 튀는 아이디어로 지루할 틈 없이 당신의 삶에 활력을 불어넣어 주는 매력적인 연인에게 강하게 끌립니다.",
            "편재": "당신은 자유로운 영혼이자 큰 무대에서 활약해야 할 사람입니다. 좁은 우물에 당신을 구속하려는 사람보다는, 스케일이 크고 호탕하여 당신의 사회적 능력을 전폭적으로 지지해 주는 통 큰 파트너가 최상입니다.",
            "정재": "당신에게 가장 필요한 것은 삶의 흔들림 없는 닻입니다. 헛된 꿈을 좇기보다는 책임감이 매우 강하고 치밀하여 가계를 알뜰하게 꾸려가는, 평생 믿고 의지할 수 있는 성실한 배우자가 운명의 짝입니다.",
            "편관": "때로는 기댈 수 있는 거대한 바위 같은 존재가 필요합니다. 카리스마와 강한 리더십으로 당신을 험난한 외부의 위험으로부터 철저하게 보호하고 든든하게 리드해 주는 동반자를 만나야 안심합니다.",
            "정관": "당신은 상식과 도리가 통하는 평화로운 관계를 지향합니다. 감정 기복이 심한 사람보다는, 바르고 이성적이며 도덕적 규범을 잘 지켜 한평생 변함없는 신뢰를 유지할 수 있는 모범적인 배우자가 최고입니다.",
            "편인": "당신의 영혼은 꽤 깊고 예민합니다. 겉핥기식 대화보다는, 독특한 예술적 감각이나 영적 직관력을 지녀 굳이 말하지 않아도 내 깊은 마음속의 상처와 고독을 단숨에 꿰뚫어 보고 보듬어주는 소울메이트를 갈망합니다.",
            "정인": "당신은 상처받기 쉬운 여린 마음을 가졌습니다. 마치 어머니처럼 넓고 조건 없는 사랑으로, 당신의 부족한 허물과 실수마저도 넉넉하게 감싸 안아주며 언제든 돌아갈 수 있는 든든한 품이 되어주는 배우자가 필요합니다."
        }

    def _generate_real_life_manifestation(self, my_group: str, optimal_elements: str, day_tg: str) -> list:
        manifestations = []
        manifestations.append({"title": "함께 있을수록 에너지가 충전된다", "desc": f"서로가 같은 {my_group}의 생체 주파수를 공유하므로, 한 공간에 거주하거나 잠을 잘 때 기운이 엇갈리지 않습니다. 밖에서 방전된 체력이 배우자 옆에만 가면 이상하게 편안해지며 빠르게 회복됩니다."})
        manifestations.append({"title": "운의 막힘이 뚫리는 개운(開運) 효과", "desc": f"당신에게 절실히 필요한 [{optimal_elements}] 기운을 상대방이 듬뿍 채워줍니다. 결혼 전 풀리지 않던 진로나 금전 문제가, 신기하게도 이 파트너를 만난 직후부터 톱니바퀴 맞물리듯 술술 풀려나갑니다."})
        tg_focus = "주도권 없는 평등함" if day_tg in ["비견", "겁재"] else "조건 없는 따뜻한 보살핌" if day_tg in ["정인", "편인"] else "안정적인 현실 감각"
        manifestations.append({"title": "결정적 순간의 가치관 일치", "desc": f"배우자궁 성향({day_tg})이 완벽히 부합하므로, 주거지 이동이나 금전 문제 등 결정적인 순간에 서로 헛발질하지 않습니다. {tg_focus}을(를) 바탕으로 소모적인 감정싸움 없이 위기를 함께 극복해 냅니다."})
        return manifestations

    def find_optimal_partner(self, formatted_bazi: dict, user_year: int, gender: str, yongshin_data: dict) -> dict:
        day_stem = formatted_bazi.get("day", {}).get("stem", "-")
        day_branch = formatted_bazi.get("day", {}).get("branch", "-")
        year_branch = formatted_bazi.get("year", {}).get("branch", "-")
        day_tg = formatted_bazi.get("day", {}).get("branch_tg", "")
        if not day_tg or day_tg == "-" or day_tg == "일간": day_tg = "비견"

        my_gung = self.hontaek.calculate_honmyeong_gung(user_year, gender)
        my_group = my_gung.get("group", "알 수 없음")
        my_element = my_gung.get("element", "")
        group_desc = f"사람은 태어난 해에 따라 고유의 생체 주파수를 갖는데, 당신은 {my_element}의 기운을 띤 '{my_group}'에 속합니다. 반대 그룹을 만나면 AM/FM 라디오 주파수가 어긋나듯 일상 공간에서 서로의 기(氣)를 빨아먹고 화해(禍害)의 흉액이 발생합니다. 따라서 당신의 파트너는 반드시 당신과 동일한 주파수 대역인 '{my_group}'의 사람이어야만 생기(生氣)와 연년(延年)의 대길함을 누릴 수 있습니다."

        ideal_stem, ideal_branch = "", ""
        for pair in self.hontaek.cheon_hap:
            if day_stem in pair: ideal_stem = list(pair - {day_stem})[0]; break
        for pair in self.hontaek.ji_hap:
            if day_branch in pair: ideal_branch = list(pair - {day_branch})[0]; break
        ideal_ilju = f"{ideal_stem}{ideal_branch} 일주" if ideal_stem and ideal_branch else "기운 혼합형"
        ilju_desc = f"명리학에서 천간(天干)은 생각과 가치관을, 지지(地支)는 현실과 육체를 의미합니다. 당신의 일주({day_stem}{day_branch})와 하늘 땅이 모두 완벽하게 맞물리는 이 일주를 가진 사람은, 굳이 말하지 않아도 영혼이 통하고 현실적 속궁합까지 들어맞는 '천지합덕격(天地合德格)'의 100점짜리 인연입니다."

        best_zodiacs = []
        for z in self.hontaek.gwiin_map.get(day_stem, []):
            if z: best_zodiacs.append({"zodiac": z+"띠", "reason": "천을귀인(하늘의 수호성)"})
        rok = self.hontaek.geonrok_map.get(day_stem, "")
        if rok: best_zodiacs.append({"zodiac": rok+"띠", "reason": "교록격(마르지 않는 재물)"})
        if ideal_branch: best_zodiacs.append({"zodiac": ideal_branch+"띠", "reason": "지합(단단한 현실 결속)"})
        for z in self.samhap.get(year_branch, []):
            if z: best_zodiacs.append({"zodiac": z+"띠", "reason": "삼합(흔들림 없는 가치관)"})

        unique_best = []
        seen = set()
        for item in best_zodiacs:
            if item["zodiac"] not in seen:
                unique_best.append(item)
                seen.add(item["zodiac"])

        worst_zodiacs = []
        w_z = self.wonjin.get(year_branch, "")
        if w_z: worst_zodiacs.append({"zodiac": w_z+"띠", "reason": "원진살(끝없는 원망과 의심)"})
        c_z = self.chung.get(year_branch, "")
        if c_z: worst_zodiacs.append({"zodiac": c_z+"띠", "reason": "상충살(정면충돌과 파경)"})

        ideal_elements = "균형잡힌 오행"
        if isinstance(yongshin_data, dict):
            y_str = str(yongshin_data.get("yongshin", "")).replace("None", "").strip()
            h_str = str(yongshin_data.get("huishin", "")).replace("None", "").strip()
            elements_arr = []
            if y_str: elements_arr.append(f"{y_str}")
            if h_str: elements_arr.append(f"{h_str}")
            if elements_arr: ideal_elements = ", ".join(elements_arr)

        ideal_elements_desc = f"사주 원국 분석 결과, 현재 당신의 삶에 가장 절실하게 필요한 절대적 기운은 [{ideal_elements}]입니다. 이 기운이 메마른 사람을 만나면 도끼로 나무를 치는 듯한 상극(相剋) 현상으로 함께 있을수록 피가 마릅니다. 반면 이 기운을 듬뿍 가진 사람을 만나면, 당신의 억부와 조후가 완벽히 보완되며 막혔던 재물운과 건강이 폭발적으로 트이게 됩니다."
        ideal_personality = self.tg_ideal_desc.get(day_tg, "서로를 존중하고 헌신하는 따뜻한 배우자")
        manifestations = self._generate_real_life_manifestation(my_group, ideal_elements, day_tg)
        conclusion = f"종합하자면, 고객님의 운명의 짝은 막연히 성격이 좋은 사람이 아닙니다. 역학적 설계도상 반드시 생체 주파수({my_group})가 일치하고, 당신의 텅 빈 헛점([{ideal_elements}])을 메워주는 사주 구조를 가져야만 톱니바퀴의 마모 없이 백년해로가 가능합니다. 의구심을 가질 필요 없이, 우주의 원리상 이 조건에 부합하는 파트너야말로 득(得)이 흉(凶)을 덮고 당신을 살리는 진짜 인연입니다."

        if gender == 'M':
            role = "정재(正財)와 식신(食神)"
            role_desc = "남성에게 최고의 길신인 바르고 알뜰한 아내(정재)와, 다정다감하게 자손을 번창시키는 넉넉한 기운(식신)을 가진 여성이 당신의 완벽한 짝입니다."
        else:
            role = "정관(正官)과 정인(正印)"
            role_desc = "여성에게 최고의 길신인 명예롭고 책임감 강한 반듯한 남편(정관)과, 조건 없는 사랑으로 든든한 울타리가 되어주는 기운(정인)을 가진 남성이 당신의 완벽한 짝입니다."

        return {
            "dongseo_group": my_group,
            "dongseo_desc": group_desc,
            "ideal_ilju": ideal_ilju,
            "ideal_ilju_desc": ilju_desc,
            "best_zodiacs": unique_best,
            "worst_zodiacs": worst_zodiacs,
            "ideal_elements": ideal_elements,
            "ideal_elements_desc": ideal_elements_desc,
            "day_tg": day_tg,
            "ideal_personality": ideal_personality,
            "manifestations": manifestations, 
            "conclusion": conclusion,
            "ideal_role": role,
            "ideal_role_desc": role_desc
        }