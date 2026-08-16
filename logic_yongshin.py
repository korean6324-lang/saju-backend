# logic_yongshin.py

class YongshinEngine:
    def __init__(self):
        self.my_side = ["비견", "겁재", "정인", "편인"]
        self.other_side = ["식신", "상관", "정재", "편재", "정관", "편관"]

        # 기본 가중치
        self.base_weights = {
            "year_stem": 10, "year_branch": 10,
            "month_stem": 10, "month_branch": 35,
            "day_branch": 15,
            "hour_stem": 10, "hour_branch": 10
        }

        # 오행 맵핑
        self.elements = {
            "목": ["甲", "乙", "寅", "卯"],
            "화": ["丙", "丁", "巳", "午"],
            "토": ["戊", "己", "辰", "戌", "丑", "未"],
            "금": ["庚", "辛", "申", "酉"],
            "수": ["壬", "癸", "亥", "子"]
        }

        # 합/충 정의
        self.samhap = {
            "목": {"亥", "卯", "未"}, "화": {"寅", "午", "戌"},
            "금": {"巳", "酉", "丑"}, "수": {"申", "子", "辰"}
        }
        self.banghap = {
            "목": {"寅", "卯", "辰"}, "화": {"巳", "午", "未"},
            "금": {"申", "酉", "戌"}, "수": {"亥", "子", "丑"}
        }
        self.chungs = [
            {"子", "午"}, {"丑", "未"}, {"寅", "申"}, 
            {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}
        ]

        # 🚨 [대가 수준 추상성 배제 DB] 상태 코드 1:1 매핑
        self.expert_text_db = {
            "WEAK_GWAN_EXCESS": "평탄해야 할 어린 시절 액운을 만나 일찍 부모를 여의거나 타향을 전전하는 뼈아픈 시련을 겪습니다. (平時值殺 早別父母) 주변의 억압이 극심하니 남 밑에 있지 말고 나만의 기술(인성/식상)로 독립해야 살길이 열립니다.",
            "WEAK_JAE_EXCESS": "재물과 이성에 대한 욕망은 거대하나 내 그릇이 작아 감당하지 못합니다. (財多身弱) 무리한 투자나 빚을 내어 사업을 벌이면 반드시 뼈저린 파산과 처의 이별수를 겪으니, 철저히 조직의 월급쟁이로 엎드려 살아야 흉을 면합니다.",
            "STRONG_IN_EXCESS": "나를 돕는 기운(어머니/망상)이 너무 과도하여 오히려 손발이 묶이고 나태해집니다. (母慈滅子) 지식만 쌓고 행동하지 않아 가정이 빈곤해지기 쉬우니, 재성(현실감각/아내)의 뼈아픈 직언을 듣고 무조건 바깥으로 뛰쳐나가야 합니다.",
            "STRONG_BI_EXCESS": "주체성과 고집이 하늘을 찔러 타인의 말을 절대 듣지 않고 충돌합니다. (群比爭財) 동업을 하거나 돈을 빌려주면 무조건 박살나며, 강한 통제력(관성)을 가진 배우자나 멘토에게 스스로 굽히고 들어가야 가정이 파탄 나지 않습니다.",
            "NO_IN_SIKJAE": "나를 돕는 자 없이 오직 나의 피땀으로 세상과 맞서야 합니다. 단 한 번도 편히 앉아 쉰 적 없이 뼈 빠지게 일하여 스스로 살아남아 빈손으로 가문을 일으킵니다. (一無坐時 勤力自生, 赤手成家)",
            "JONG_JAE": "[특수 종재격] 내 자존심을 완벽히 꺾고 재물(財)의 거대한 흐름에 완전히 엎드려 복종한 형국입니다. (棄命從財) 줏대를 세우지 말고 자본의 흐름과 돈이 많은 자를 따르면, 한평생 만금(萬金)을 거머쥐는 대부(大富)의 명입니다.",
            "JONG_SAL": "[특수 종살격] 나를 죽이려는 권력(殺)이 너무 강해, 오히려 그 권력에 철저히 흡수되어 버린 살벌한 형국입니다. (棄命從殺) 법, 군경, 사법 등 생사여탈권을 쥔 조직에서 타의 추종을 불허하는 권력을 쥐게 됩니다."
        }
        
        # 🚨 [신규 DB] 용신별 혼택(부부관계) 실전 가이드
        self.marriage_advice_db = {
            "비겁": "나의 줏대를 세워주는 기운이 수호신입니다. 결혼 후에도 부부간 상하관계가 아닌 '평등한 맞벌이 동반자' 형태를 유지해야 가정이 흔들리지 않습니다.",
            "식상": "내 에너지를 밖으로 표출하고 베푸는 기운이 수호신입니다. 배우자에게 먼저 양보하고, 특히 '자식을 낳고 기르는 과정'에서 가세가 폭발적으로 상승합니다.",
            "재성": "현실 감각과 결과물이 수호신입니다. 허황된 꿈을 꾸는 배우자보다는 꼼꼼하고 경제 관념이 뚜렷한 배우자를 만나 재테크를 전담시켜야 안정됩니다.",
            "관성": "나를 합리적으로 통제하는 기운이 수호신입니다. 연애결혼보다는 집안 어른이나 조직 내에서 검증된 반듯한 배우자를 만나는 것이 인생의 흉을 피하는 지름길입니다.",
            "인성": "나를 보살펴주는 든든한 어머니 같은 기운이 수호신입니다. 나보다 연상이거나, 학식이 높고 배울 점이 많아 정신적 지주가 되어줄 수 있는 배우자가 절대적으로 필요합니다."
        }

    # 🚨 [보안 추가] 안전한 문자열 처리 및 딕셔너리 접근
    def _safe_str(self, val) -> str:
        return str(val).strip() if val else ""
        
    def _safe_get(self, d: dict, key1: str, key2: str, default=""):
        if not isinstance(d, dict): return default
        sub_d = d.get(key1, {})
        if not isinstance(sub_d, dict): return default
        return self._safe_str(sub_d.get(key2, default))

    def _get_tg_group(self, tg: str) -> str:
        if tg in ["비견", "겁재"]: return "비겁"
        if tg in ["식신", "상관"]: return "식상"
        if tg in ["편재", "정재"]: return "재성"
        if tg in ["편관", "정관"]: return "관성"
        if tg in ["편인", "정인"]: return "인성"
        return "기타"

    def _determine_element(self, char: str) -> str:
        for elem, chars in self.elements.items():
            if char in chars: return elem
        return None

    def _get_tg_group_by_element(self, day_stem: str, target_elem: str) -> str:
        day_elem = self._determine_element(day_stem)
        if not day_elem or not target_elem: 
            return "기타"

        generates = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
        overcomes = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}
        
        if day_elem == target_elem: return "비겁"
        if generates[day_elem] == target_elem: return "식상"
        if overcomes[day_elem] == target_elem: return "재성"
        if overcomes[target_elem] == day_elem: return "관성"
        if generates[target_elem] == day_elem: return "인성"
        return "기타"

    def determine_strength(self, bazi_data: dict) -> dict:
        tg_scores = {"비겁": 0, "식상": 0, "재성": 0, "관성": 0, "인성": 0}
        instability_flag = False
        
        # 🚨 [보안 추가] KeyError 방어
        day_stem = self._safe_get(bazi_data, "day", "stem")
        if not day_stem: 
            return {"status_code": "에러", "expert_advice": "데이터 누락"}
        
        pillars = ["year", "month", "day", "hour"]
        branches = [self._safe_get(bazi_data, p, "branch", "-") for p in pillars]
        
        # 1. 기본 가중치 세팅
        for p, w in [("year_stem", 10), ("year_branch", 10), ("month_stem", 10), 
                     ("month_branch", 35), ("day_branch", 15), 
                     ("hour_stem", 10), ("hour_branch", 10)]:
            pillar = p.split("_")[0]
            t_type = p.split("_")[1]
            tg = self._safe_get(bazi_data, pillar, f"{t_type}_tg", "-")
            if tg and tg != "-":
                grp = self._get_tg_group(tg)
                if grp in tg_scores:
                    tg_scores[grp] += w

        # 2. 충(沖) 로직: 지지 충돌 시 점수 반토막 및 불안정 플래그 ON
        for i in range(len(branches)-1):
            if branches[i] == "-" or branches[i+1] == "-": continue
            pair = {branches[i], branches[i+1]}
            if pair in self.chungs:
                instability_flag = True
                tg1 = self._get_tg_group(self._safe_get(bazi_data, pillars[i], "branch_tg", "-"))
                tg2 = self._get_tg_group(self._safe_get(bazi_data, pillars[i+1], "branch_tg", "-"))
                if tg1 in tg_scores: tg_scores[tg1] -= (self.base_weights[f"{pillars[i]}_branch"] * 0.5)
                if tg2 in tg_scores: tg_scores[tg2] -= (self.base_weights[f"{pillars[i+1]}_branch"] * 0.5)

        # 3. 합(合) 로직: 삼합/방합 성립 시 에너지 폭증
        b_set = set(b for b in branches if b != "-")
        for elem, chars in self.samhap.items():
            if chars.issubset(b_set):
                target_grp = self._get_tg_group_by_element(day_stem, elem)
                if target_grp in tg_scores:
                    tg_scores[target_grp] += 50

        for elem, chars in self.banghap.items():
            if chars.issubset(b_set):
                target_grp = self._get_tg_group_by_element(day_stem, elem)
                if target_grp in tg_scores:
                    tg_scores[target_grp] += 40

        # 총합 및 내편/남편 계산
        total_score = sum(tg_scores.values())
        if total_score == 0: total_score = 100
        
        my_power_raw = tg_scores["비겁"] + tg_scores["인성"]
        my_percent = (my_power_raw / total_score) * 100

        # 4. 특수격(종격) 캐처 모듈
        status_code = ""
        expert_advice = ""
        is_special = False

        if my_percent < 15: 
            if tg_scores["재성"] >= 90 or (tg_scores["재성"] / total_score) >= 0.65:
                status_code = "JONG_JAE"
                expert_advice = self.expert_text_db.get("JONG_JAE", "")
                is_special = True
            elif tg_scores["관성"] >= 90 or (tg_scores["관성"] / total_score) >= 0.65:
                status_code = "JONG_SAL"
                expert_advice = self.expert_text_db.get("JONG_SAL", "")
                is_special = True
                
        if not is_special:
            if my_percent >= 60:
                status_code = "극신강"
                if tg_scores["인성"] > tg_scores["비겁"]: 
                    expert_advice = self.expert_text_db.get("STRONG_IN_EXCESS", "")
                else: 
                    expert_advice = self.expert_text_db.get("STRONG_BI_EXCESS", "")
            elif my_percent >= 48:
                status_code = "신강"
            elif my_percent >= 38:
                status_code = "신약"
            else:
                status_code = "극신약"
                if tg_scores["관성"] > tg_scores["재성"] and tg_scores["관성"] > tg_scores["식상"]:
                    expert_advice = self.expert_text_db.get("WEAK_GWAN_EXCESS", "")
                elif tg_scores["재성"] > tg_scores["식상"]:
                    expert_advice = self.expert_text_db.get("WEAK_JAE_EXCESS", "")
                
                if tg_scores["인성"] == 0 and (tg_scores["식상"] > 0 or tg_scores["재성"] > 0):
                    expert_advice = self.expert_text_db.get("NO_IN_SIKJAE", "")

        return {
            "my_power": int(my_percent), 
            "other_power": 100 - int(my_percent), 
            "status": "특수 종격(從格)" if is_special else status_code,
            "status_code": status_code,
            "tg_scores": tg_scores,
            "instability": instability_flag,
            "expert_advice": expert_advice
        }

    def determine_geokguk(self, bazi_data: dict, hidden_stems_data: dict) -> dict:
        day_stem = self._safe_get(bazi_data, "day", "stem")
        month_branch_tg = self._safe_get(bazi_data, "month", "branch_tg")

        if not day_stem:
            return {"name_clean": "알수없음", "hanja_clean": "", "desc": "격국 산출 불가"}

        if month_branch_tg == "비견":
            return {"name_clean": "건록격", "hanja_clean": "建祿格", "desc": "자수성가의 명. 독립심이 강하고 자신의 실력으로 세상을 개척하는 튼튼한 그릇입니다."}
        
        yang_stems = ["甲", "丙", "戊", "庚", "壬"]
        if day_stem in yang_stems and month_branch_tg == "겁재":
            return {"name_clean": "양인격", "hanja_clean": "羊刃格", "desc": "장군의 명. 펜이나 칼을 쥔 격으로, 프로페셔널한 권력과 압도적 카리스마를 가진 거대한 그릇입니다."}
        if day_stem not in yang_stems and month_branch_tg == "겁재":
            return {"name_clean": "월인격", "hanja_clean": "月刃格", "desc": "질긴 생명력의 명. 타인의 지배를 거부하고 은근한 고집으로 기어코 뜻을 이루어내는 그릇입니다."}

        # 🚨 [보안 추가] 지장간 데이터 타입 방어
        if not isinstance(hidden_stems_data, dict): hidden_stems_data = {}
        month_hidden = hidden_stems_data.get("month", {})
        if not isinstance(month_hidden, dict): month_hidden = {}
        
        projected_tg = None
        
        for key in ["main", "middle", "initial"]:
            h_stem_tuple = month_hidden.get(key, (None, 0))
            h_stem = h_stem_tuple[0] if isinstance(h_stem_tuple, (list, tuple)) else None
            
            if h_stem:
                for pillar in ["year", "month", "hour"]:
                    if self._safe_get(bazi_data, pillar, "stem") == h_stem:
                        projected_tg = self._safe_get(bazi_data, pillar, "stem_tg")
                        break
            if projected_tg: break

        target_tg = projected_tg if projected_tg else month_branch_tg

        geokguk_texts = {
            "식신": {"name_clean": "식신격", "hanja_clean": "食神格", "desc": "연구와 창작의 명. 평생 의식주가 마르지 않으며 한 분야를 깊게 파고드는 전문가의 그릇입니다."},
            "상관": {"name_clean": "상관격", "hanja_clean": "傷官格", "desc": "혁신과 언변의 명. 기존의 틀을 깨는 천재성이 있으며, 말과 재능으로 세상을 매혹시키는 그릇입니다."},
            "정재": {"name_clean": "정재격", "hanja_clean": "正財格", "desc": "안정과 신용의 명. 치밀하고 꼼꼼하며, 정당한 노력으로 확실한 부(富)를 축적하는 관리자의 그릇입니다."},
            "편재": {"name_clean": "편재격", "hanja_clean": "偏財格", "desc": "사업과 공간지각의 명. 스케일이 크고 거대한 재물의 흐름을 지배하는 사업가적 그릇입니다."},
            "정관": {"name_clean": "정관격", "hanja_clean": "正官格", "desc": "명예와 규율의 명. 바르고 합리적이며, 거대 조직에서 인정받고 높은 벼슬에 오르는 그릇입니다."},
            "편관": {"name_clean": "편관격", "hanja_clean": "偏官格", "desc": "권력과 돌파력의 명. 극한의 스트레스를 이겨내고 권력을 거머쥐는 리더나 특수직의 그릇입니다."},
            "정인": {"name_clean": "정인격", "hanja_clean": "正印格", "desc": "학문과 도덕의 명. 배움에 대한 열정이 높고 대중의 존경을 받는 학자나 교육자의 그릇입니다."},
            "편인": {"name_clean": "편인격", "hanja_clean": "偏印格", "desc": "영감과 특수재능의 명. 남들이 못 보는 것을 꿰뚫어 보는 직관력과 기획력으로 승부하는 그릇입니다."}
        }

        return geokguk_texts.get(target_tg, {"name_clean": f"{target_tg}격", "hanja_clean": "", "desc": f"사회를 살아가는 무기로 {target_tg}의 기운을 강력하게 쓰는 그릇입니다."})

    def determine_yongshin(self, bazi_data: dict, strength_data: dict) -> dict:
        month_branch = self._safe_get(bazi_data, "month", "branch")
        status_code = self._safe_str(strength_data.get("status_code"))
        tg_scores = strength_data.get("tg_scores", {})
        
        result = {"yongshin": "", "huishin": "", "gishin": "", "desc": "", "marriage_advice": ""}

        # 1. 특수격(종격) 절대 우선
        if status_code == "JONG_JAE":
            result["yongshin"] = "재성(재물/현실감각)"
            result["huishin"] = "식상(재능/활동)"
            result["gishin"] = "비겁(자존심/동업)"
            result["desc"] = strength_data.get("expert_advice", "")
            result["marriage_advice"] = self.marriage_advice_db.get("재성", "")
            return result
        elif status_code == "JONG_SAL":
            result["yongshin"] = "관성(권력/조직)"
            result["huishin"] = "재성(재물/목표)"
            result["gishin"] = "식상(반항/언변)"
            result["desc"] = strength_data.get("expert_advice", "")
            result["marriage_advice"] = self.marriage_advice_db.get("관성", "")
            return result

        # 2. 조후 vs 억부 충돌 방어 로직
        is_winter = month_branch in ["亥", "子", "丑"]
        is_summer = month_branch in ["巳", "午", "未"]
        is_weak = "약" in status_code

        if is_winter:
            if is_weak: 
                result["yongshin"] = "조후용신 방어: 목(木) 에너지 (인성/비겁)"
                result["huishin"] = "화(火) 에너지"
                result["gishin"] = "수(水) 에너지 및 금(金)"
                result["desc"] = "꽁꽁 얼어붙은 사주이나 기운마저 극도로 쇠약합니다. 섣불리 불(재물/권력)을 쫓아가면 얼음물이 녹아 나를 덮치니, 반드시 지식과 자격증(인성)을 먼저 갖추어 내실을 다져야만 다가올 부와 명예를 거머쥘 수 있습니다."
                result["marriage_advice"] = self.marriage_advice_db.get("인성", "")
                return result
            else:
                result["yongshin"] = "조후용신: 화(火) 에너지"
                result["huishin"] = "목(木) 에너지"
                result["gishin"] = "수(水) 에너지"
                result["desc"] = "동토의 얼어붙은 사주입니다. 나의 에너지가 든든하니 주저 없이 따뜻한 태양과 불(火)의 기운(사회적 활동/재물)을 쫓아야 만물이 소생하고 폭발적으로 발복합니다."
                result["marriage_advice"] = self.marriage_advice_db.get("재성", "")
                return result

        if is_summer:
            if is_weak: 
                result["yongshin"] = "조후용신 방어: 금(金) 에너지 (인성/비겁)"
                result["huishin"] = "수(水) 에너지"
                result["gishin"] = "화(火) 에너지 및 목(木)"
                result["desc"] = "펄펄 끓는 사막의 사주이나 체력이 고갈되었습니다. 섣불리 물(재물/결과)을 쫓으면 증발해 버리니, 바위처럼 단단한 원칙과 자격증(금 기운)으로 바탕을 다져야 물이 솟아나 갈증을 해소합니다."
                result["marriage_advice"] = self.marriage_advice_db.get("인성", "")
                return result
            else:
                result["yongshin"] = "조후용신: 수(水) 에너지"
                result["huishin"] = "금(金) 에너지"
                result["gishin"] = "화(火) 에너지"
                result["desc"] = "사막처럼 펄펄 끓는 한여름의 사주입니다. 내공이 튼튼하니 주저 없이 시원한 강물(수 기운)의 무대를 향해 나아가 맹활약하면 재물과 명예가 파도처럼 밀려옵니다."
                result["marriage_advice"] = self.marriage_advice_db.get("식상", "")
                return result

        # 3. 병약(病藥) 억부 판별
        adv = strength_data.get("expert_advice", "")
        if "신강" in status_code:
            if tg_scores.get("인성", 0) > tg_scores.get("비겁", 0):
                result["yongshin"] = "재성 (현실감각/목표)"
                result["gishin"] = "인성 (망상/게으름)"
                result["marriage_advice"] = self.marriage_advice_db.get("재성", "")
            else:
                result["yongshin"] = "관성 (규율/통제력)"
                result["gishin"] = "비겁 (오만/동업)"
                result["marriage_advice"] = self.marriage_advice_db.get("관성", "")
                
            result["huishin"] = "식상 (유연성/표현)"
            result["desc"] = adv if adv else f"나의 에너지가 넘치는 {status_code} 사주입니다. 흘러넘치는 내 힘을 시원하게 빼주면서 결과물을 만들어내는 기운이 최고의 수호신입니다."
        else:
            if tg_scores.get("관성", 0) > tg_scores.get("재성", 0) and tg_scores.get("관성", 0) > tg_scores.get("식상", 0):
                result["yongshin"] = "인성 (지식/문서/어머니)"
                result["gishin"] = "관성 (압박/스트레스)"
                result["marriage_advice"] = self.marriage_advice_db.get("인성", "")
            else:
                result["yongshin"] = "비겁 (동료/주체성)"
                result["gishin"] = "재성 (재물욕/과로)"
                result["marriage_advice"] = self.marriage_advice_db.get("비겁", "")
                
            result["huishin"] = "인성"
            result["desc"] = adv if adv else f"기운이 소진된 {status_code} 사주입니다. 나를 든든하게 생(生)해주는 지식(인성)이나 든든한 아군(비겁)이 수호신이 됩니다. 과도한 재물이나 명예를 쫓으면 건강이 박살 납니다."

        return result