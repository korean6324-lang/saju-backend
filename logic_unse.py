# logic_unse.py

class UnseEngine:
    def __init__(self):
        # 오행 정의
        self.stem_elem = {
            "甲": "목", "乙": "목", "丙": "화", "丁": "화", "戊": "토",
            "己": "토", "庚": "금", "辛": "금", "壬": "수", "癸": "수"
        }
        self.branch_elem = {
            "子": "수", "丑": "토", "寅": "목", "卯": "목", "辰": "토", "巳": "화",
            "午": "화", "未": "토", "申": "금", "酉": "금", "戌": "토", "亥": "수"
        }
        # 지지 충(沖) 관계
        self.chungs = {
            "子": "午", "午": "子", "丑": "未", "未": "丑", "寅": "申", "申": "寅",
            "卯": "酉", "酉": "卯", "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"
        }
        # 지지 육합(六合) 관계
        self.habs = {
            "子": "丑", "丑": "子", "寅": "亥", "亥": "寅", "卯": "戌", "戌": "卯",
            "辰": "酉", "酉": "辰", "巳": "申", "申": "巳", "午": "未", "未": "午"
        }

    def _get_element(self, char: str) -> str:
        return self.stem_elem.get(char, self.branch_elem.get(char, ""))

    def _eval_luck_score(self, luck_branch: str, tg: str, yongshin_data: dict) -> int:
        """
        운의 지지(luck_branch) 오행과 십신(tg)을 용신/희신/기신과 대조하여 정밀 점수(-2 ~ +2) 계산
        """
        luck_elem = self._get_element(luck_branch)
        score = 0

        # 용신/희신/기신 텍스트 extraction
        y_text = ""
        h_text = ""
        g_text = ""

        if isinstance(yongshin_data, dict):
            y_info = yongshin_data.get("yongshin", {})
            if isinstance(y_info, dict):
                y_text = str(y_info.get("yongshin", ""))
                h_text = str(y_info.get("huishin", ""))
                g_text = str(y_info.get("gishin", ""))
            elif isinstance(y_info, str):
                y_text = y_info

        # 오행 적합도 체킹
        if luck_elem:
            if luck_elem in y_text:
                score += 2
            elif luck_elem in h_text:
                score += 1
            elif luck_elem in g_text:
                score -= 2

        # 십신 고유 성향 가산점
        if tg in ["식신", "정재", "정관", "정인"]:
            score += 1
        elif tg in ["편관", "상관", "겁재"]:
            score -= 1

        return score

    def _scan_interactions(self, formatted_bazi: dict, luck_branch: str) -> list:
        """ 원국 지지들과의 충(沖), 합(合) 반응을 정밀 스캔 """
        events = []

        for p_key, p_info in formatted_bazi.items():
            b_char = p_info["branch"]

            if self.chungs.get(luck_branch) == b_char:
                if p_key == "day":
                    events.append({"type": "bad", "title": f"⚡ 일지 정면 충({luck_branch}{b_char}沖)", "desc": "배우자궁과 본인 자리가 부딪히므로 신상 변동, 건강 주의, 배우자와의 언행 자제가 필요합니다."})
                elif p_key == "month":
                    events.append({"type": "bad", "title": f"⚡ 월지 사회궁 충({luck_branch}{b_char}沖)", "desc": "직장 환경, 사업체, 사회적 관계에 큰 변동수나 이동수가 강하게 들어옵니다."})
                elif p_key == "year":
                    events.append({"type": "bad", "title": f"⚡ 연지 환경 충({luck_branch}{b_char}沖)", "desc": "주거지 이동, 해외 출장, 대외 환경의 큰 변화가 일어나는 시기입니다."})
                elif p_key == "hour":
                    events.append({"type": "bad", "title": f"⚡ 시지 말년궁 충({luck_branch}{b_char}沖)", "desc": "자식 문제, 부하 직원과의 갈등, 비밀 프로젝트의 변동수가 발생할 수 있습니다."})

            elif self.habs.get(luck_branch) == b_char:
                if p_key == "day":
                    events.append({"type": "good", "title": f"✨ 일지 인연 육합({luck_branch}{b_char}合)", "desc": "마음이 잘 맞는 귀인을 만나거나 귀한 인연/협력 관계가 은밀하고 단단하게 성립됩니다."})
                elif p_key == "month":
                    events.append({"type": "good", "title": f"✨ 월지 사회궁 육합({luck_branch}{b_char}合)", "desc": "직장이나 비즈니스에서 뜻을 함께할 동업자나 든든한 조력자를 만나 계약이 성사됩니다."})

        return events

    def analyze_sewun(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ [1년 단위 - 세운] 거시적 인생의 큰 줄기와 대변동 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)
        events = self._scan_interactions(formatted_bazi, branch)

        if score >= 2:
            status = "🔥 대도약과 발복의 해"
            desc = f"올해는 수호신의 기운과 긍정적인 [{tg}]의 에너지가 결합하여 사업 성취, 승진, 재물 축적 등 인생의 큰 도약을 이루는 최고의 한 해입니다."
        elif score == 1:
            status = "✨ 성취와 발전의 해"
            desc = f"올해는 [{tg}] 기운의 순풍을 받아 무난히 목표를 달성하고 실속을 챙길 수 있는 건설적인 한 해가 됩니다."
        elif score == 0:
            status = "🌱 무난하고 평탄한 흐름"
            desc = f"올해는 큰 굴곡이나 흉액 없이 정직하게 흘린 땀만큼 결실을 얻는 평안한 해입니다. 일상을 충실히 유지하십시오."
        else:
            status = "⚠️ 수성(守城)과 내실의 해"
            desc = f"올해는 [{tg}]의 스트레스성 기운이 작용하므로 무리한 확장이나 투자는 자제하고 내실을 기하며 건강에 유의해야 하는 시기입니다."

        return {"overall_status": status, "overall_desc": desc, "events": events}

    def analyze_wolgeon(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ [1달 단위 - 월건] 한 달간의 단기 업무, 대인관계, 컨디션 흐름 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)

        if score >= 2:
            status = "🚀 도약과 결실의 한 달"
            desc = f"이번 달은 [{tg}]의 귀한 기운이 작용하여 진행 중인 프로젝트나 계약에서 큰 성과를 거두고 막혔던 일이 시원하게 풀립니다."
        elif score == 1:
            status = "🌿 활력 있고 보람찬 한 달"
            desc = f"이번 달은 [{tg}]의 유연한 기운 덕분에 대인관계가 원만해지고 성실히 노력한 만큼 깔끔한 결실을 얻게 됩니다."
        elif score == 0:
            status = "☕ 차분하고 평온한 한 달"
            desc = f"이번 달은 무탈하고 조용하게 일상이 유지되는 시기입니다. 마음의 여유를 갖고 차분히 고유의 페이스를 유지하세요."
        else:
            status = "🌧️ 감정 조율과 휴식이 필요한 한 달"
            desc = f"이번 달은 [{tg}]의 영향으로 다소 피로감이 쌓이거나 대인관계에서 사소한 마찰이 생길 수 있으니 감정 조율에 신경 쓰세요."

        return {"overall_status": status, "overall_desc": desc, "events": []}

    def analyze_iljin(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ [하루 단위 - 일진] 오늘 하루의 컨디션, 약속, 소소한 기운 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)

        if score >= 2:
            status = "☀️ 최고의 기운, 행운의 하루"
            desc = f"오늘 하루는 상쾌한 [{tg}]의 에너지가 솟구쳐 집중력이 높아지고 중요한 인연이나 호재를 만나기 아주 좋은 날입니다."
        elif score == 1:
            status = "🌸 기분 좋고 순조로운 하루"
            desc = f"오늘 하루는 [{tg}]의 온화한 흐름 덕분에 약속이나 업무가 무리 없이 일사천리로 진행됩니다."
        elif score == 0:
            status = "🍃 무탈하고 평온한 하루"
            desc = f"오늘 하루는 특별한 문제 없이 차분하게 흘러가는 잔잔한 날입니다. 편안한 마음으로 일과를 마치세요."
        else:
            status = "☔ 언행 자제, 쉬어가야 할 하루"
            desc = f"오늘 하루는 예민한 [{tg}]의 기운으로 몸이 조금 무거울 수 있습니다. 중요한 결정은 내일로 미루고 일찍 휴식을 취하세요."

        return {"overall_status": status, "overall_desc": desc, "events": []}