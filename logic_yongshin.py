# logic_yongshin.py

class YongshinEngine:
    def __init__(self):
        # 십신 세력 분류 (신강/신약 판별용)
        # 내 편(인성, 비겁) vs 남의 편(식상, 재성, 관성)
        self.my_side = ["비견", "겁재", "정인", "편인"]
        self.other_side = ["식신", "상관", "정재", "편재", "정관", "편관"]

        # 지지별 힘의 가중치 (총합 100) - 월지가 가장 강력한 힘을 가짐
        self.power_weights = {
            "year_stem": 10, "year_branch": 10,
            "month_stem": 10, "month_branch": 35,
            "day_branch": 15,
            "hour_stem": 10, "hour_branch": 10
        }

    def determine_geokguk(self, bazi_data: dict, hidden_stems_data: dict) -> dict:
        """
        [격국(格局) 판별 알고리즘]
        월지(태어난 달)의 지장간이 천간에 어떻게 투출되었는지를 추적하여 사주의 그릇을 정합니다.
        """
        day_stem = bazi_data["day"]["stem"]
        month_branch_tg = bazi_data["month"]["branch_tg"]

        # 1. 특수격 (건록격, 양인격) 우선 판별
        if month_branch_tg == "비견":
            return {"name": "건록격", "hanja": "建祿格", "desc": "자수성가의 명. 독립심이 강하고 자신의 실력으로 세상을 개척하는 튼튼한 그릇입니다."}
        
        yang_stems = ["甲", "丙", "戊", "庚", "壬"]
        if day_stem in yang_stems and month_branch_tg == "겁재":
            return {"name": "양인격", "hanja": "羊刃格", "desc": "장군의 명. 칼을 쥔 격으로, 프로페셔널한 권력과 압도적 카리스마를 가진 거대한 그릇입니다."}

        # 2. 일반 정격(正格) 투출 판별 로직 (미완성 버그 수정 완료)
        month_hidden = hidden_stems_data["month"]
        
        projected_tg = None
        # 정기 -> 중기 -> 여기 순으로 천간에 떴는지 확인
        for key in ["main", "middle", "initial"]:
            h_stem, _ = month_hidden.get(key, (None, 0))
            if h_stem:
                # 천간(연, 월, 시) 중 어디에 떴는지 확인하여 해당 십신을 확보
                for pillar in ["year", "month", "hour"]:
                    if bazi_data[pillar]["stem"] == h_stem:
                        projected_tg = bazi_data[pillar]["stem_tg"]
                        break
            if projected_tg:
                break

        # 3. 투출된 십신이 있으면 그것이 격국, 없으면 월지 정기(본기)가 격국
        target_tg = projected_tg if projected_tg else month_branch_tg

        # 🚨 [수정 완료] 한자/한글 분리 (JSON 정규화)
        geokguk_texts = {
            "식신": {"name": "식신격", "hanja": "食神格", "desc": "연구와 창작의 명. 평생 의식주가 마르지 않으며 한 분야를 깊게 파고드는 전문가의 그릇입니다."},
            "상관": {"name": "상관격", "hanja": "傷官格", "desc": "혁신과 언변의 명. 기존의 틀을 깨는 천재성이 있으며, 말과 재능으로 세상을 매혹시키는 그릇입니다."},
            "정재": {"name": "정재격", "hanja": "正財格", "desc": "안정과 신용의 명. 치밀하고 꼼꼼하며, 정당한 노력으로 확실한 부(富)를 축적하는 금융가/관리자의 그릇입니다."},
            "편재": {"name": "편재격", "hanja": "偏財格", "desc": "사업과 공간지각의 명. 스케일이 크고 재물을 지배하는 능력이 탁월한 사업가적 그릇입니다."},
            "정관": {"name": "정관격", "hanja": "正官格", "desc": "명예와 규율의 명. 바르고 합리적이며, 조직에서 인정받고 높은 벼슬(임원/관직)에 오르는 그릇입니다."},
            "편관": {"name": "편관격", "hanja": "偏官格", "desc": "권력과 돌파력의 명. 극한의 스트레스를 이겨내고 큰 권력을 거머쥐는 스타트업 대표나 특수직의 그릇입니다."},
            "정인": {"name": "정인격", "hanja": "正印格", "desc": "학문과 도덕의 명. 배움에 대한 열정이 높고 사람들의 존경을 받는 학자나 교육자의 그릇입니다."},
            "편인": {"name": "편인격", "hanja": "偏印格", "desc": "영감과 특수재능의 명. 남들이 못 보는 것을 보는 직관력이 뛰어나며, 기획력과 아이디어로 승부하는 그릇입니다."}
        }

        if target_tg in ["겁재", "비견"]:
            return {"name": "월걸록격", "hanja": "月建祿格", "desc": "주체성이 강하고 타인의 지배를 받기 싫어하는 독립적인 그릇입니다."}

        return geokguk_texts.get(target_tg, {"name": f"{target_tg}격", "hanja": "", "desc": f"{target_tg}의 기운을 쓰는 그릇입니다."})

    def determine_strength(self, bazi_data: dict) -> dict:
        """
        [신강/신약 판별 알고리즘]
        시간 모름 체크 시 억울하게 극신약으로 빠지는 수학적 오류 수정. 
        퍼센테이지(%) 보정 알고리즘 적용 완료.
        """
        my_power = 0
        total_valid_power = 0

        def add_power(tg, weight):
            nonlocal my_power, total_valid_power
            if tg == "-" or not tg: return # 시간이 없거나 알 수 없는 값은 무시
            
            total_valid_power += weight
            if tg in self.my_side:
                my_power += weight

        # 점수 합산
        add_power(bazi_data["year"]["stem_tg"], self.power_weights["year_stem"])
        add_power(bazi_data["year"]["branch_tg"], self.power_weights["year_branch"])
        add_power(bazi_data["month"]["stem_tg"], self.power_weights["month_stem"])
        add_power(bazi_data["month"]["branch_tg"], self.power_weights["month_branch"])
        add_power(bazi_data["day"]["branch_tg"], self.power_weights["day_branch"])
        add_power(bazi_data["hour"]["stem_tg"], self.power_weights["hour_stem"])
        add_power(bazi_data["hour"]["branch_tg"], self.power_weights["hour_branch"])

        # 🚨 [수정 완료] 퍼센티지 스케일링 (시간을 모르면 80점 만점을 100%로 환산)
        if total_valid_power == 0: total_valid_power = 100
        my_percent = (my_power / total_valid_power) * 100
        other_percent = 100 - my_percent

        # 판별
        if my_percent >= 60: 
            status = "극신강"
            status_hanja = "極身强"
        elif my_percent >= 48: 
            status = "신강"
            status_hanja = "身强"
        elif my_percent >= 38: 
            status = "신약"
            status_hanja = "身弱"
        else: 
            status = "극신약"
            status_hanja = "極身弱"

        # 프론트엔드 출력을 위해 문자열 포맷팅
        status_full = f"{status}({status_hanja})"

        return {
            "my_power": int(my_percent), 
            "other_power": int(other_percent), 
            "status": status_full,
            "status_code": status
        }

    def determine_yongshin(self, bazi_data: dict, strength_data: dict) -> dict:
        """
        [용희구기(用喜仇忌) - 나의 수호신 도출 알고리즘]
        """
        month_branch = bazi_data["month"]["branch"]
        status_code = strength_data["status_code"]
        
        result = {
            "yongshin": "", 
            "huishin": "",  
            "gishin": "",   
            "desc": ""
        }

        # 1. 조후(기후) 판별
        if month_branch in ["亥", "子", "丑"]:
            result["yongshin"] = "조후용신: 화(火) 에너지"
            result["huishin"] = "조후희신: 목(木) 에너지"
            result["gishin"] = "기신: 수(水) 에너지"
            result["desc"] = "꽁꽁 얼어붙은 한겨울의 사주입니다. 다른 무엇보다 따뜻한 태양과 불(火)의 기운이 들어와야 만물이 소생하고 발복합니다. 물(水)이 들어오면 우울해지고 막힙니다."
            return result
            
        if month_branch in ["巳", "午", "未"]: 
            result["yongshin"] = "조후용신: 수(水) 에너지"
            result["huishin"] = "조후희신: 금(金) 에너지"
            result["gishin"] = "기신: 화(火) 에너지"
            result["desc"] = "사막처럼 펄펄 끓는 한여름의 사주입니다. 시원한 단비와 강물(水)의 기운이 수호신이 되어 사주를 적셔주어야 재물과 안정이 찾아옵니다."
            return result

        # 2. 억부(균형) 판별
        if "신강" in status_code:
            result["yongshin"] = "식상(식신/상관) 또는 재성(편재/정재)"
            result["huishin"] = "관성(편관/정관)"
            result["gishin"] = "인성(편인/정인) 및 비겁(비견/겁재)"
            result["desc"] = f"나의 에너지가 넘치는 {status_code} 사주입니다. 내 힘을 시원하게 빼주면서 결과물을 만들어내는 '식상'이나 '재성'이 최고의 수호신(용신)입니다. 반대로 나를 더 고집스럽게 만드는 '인성'이나 '비겁' 운이 오면 일이 꼬이고 재물이 흩어집니다."
        else:
            result["yongshin"] = "인성(편인/정인)"
            result["huishin"] = "비겁(비견/겁재)"
            result["gishin"] = "관성(편관/정관) 및 재성(편재/정재)"
            result["desc"] = f"나의 에너지가 다소 부족한 {status_code} 사주입니다. 나를 든든하게 생(生)해주는 '인성'이나 든든한 동료인 '비겁'이 수호신(용신)이 됩니다. 내 힘을 빼는 '관성'이나 무리한 '재성' 운이 오면 건강이 상하고 스트레스가 극심해집니다."

        return result